"""
game/market.py — Zeta Auction House + NPC Sell
Place in: game/market.py
"""
from datetime import datetime, timedelta, timezone
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

LISTING_FEE_PCT  = 0.05
LISTING_HOURS    = 48
MAX_LISTINGS     = 5
PAGE_SIZE        = 5   # listings per page
UNLISTED_ITEM_TYPES = {"bag_upgrade", "key_item", "cosmetic"}

NPC_SPECIALTY: dict[str, list[str]] = {
    "nurse_hana": ["crafting", "consumable"],
    "old_tomas":  ["material", "lore", "tool"],
    "old_grull":  ["crafting", "tool"],
    "vex":        ["lore"],
}


# ---------------------------------------------------------------------------
# Listings — with DB-level filter, sort, pagination
# ---------------------------------------------------------------------------

async def get_active_listings(
    session,
    item_type_filter: str = "all",
    sort: str = "recent",       # recent | cheapest | expensive | expiring
    page: int = 0,
) -> tuple[list, int]:
    """
    Returns (listings, total_count) with DB-level filtering and sorting.
    """
    from core.models import MarketListing
    now = datetime.now(timezone.utc)

    base = (
        select(MarketListing)
        .where(MarketListing.status == "active", MarketListing.expires_at > now)
    )

    # DB-level type filter — build item_id set from game data
    if item_type_filter and item_type_filter != "all":
        from game.data import ITEMS
        filtered_ids = [
            item_id for item_id, item in ITEMS.items()
            if item.get("type") == item_type_filter
        ]
        if not filtered_ids:
            return [], 0
        base = base.where(MarketListing.item_id.in_(filtered_ids))

    # Sort
    if sort == "cheapest":
        base = base.order_by(MarketListing.price.asc())
    elif sort == "expensive":
        base = base.order_by(MarketListing.price.desc())
    elif sort == "expiring":
        base = base.order_by(MarketListing.expires_at.asc())
    else:  # recent
        base = base.order_by(MarketListing.listed_at.desc())

    # Total count (for pagination display)
    count_q = select(func.count()).select_from(base.subquery())
    total   = (await session.execute(count_q)).scalar() or 0

    # Paginated page
    result   = await session.execute(base.offset(page * PAGE_SIZE).limit(PAGE_SIZE))
    listings = result.scalars().all()

    return listings, total


async def get_seller_names(listings: list, session) -> dict[int, str]:
    """Fetch character names for all sellers in a listing set."""
    from core.models import Player
    seller_ids = list({l.seller_id for l in listings})
    if not seller_ids:
        return {}
    result = await session.execute(
        select(Player.user_id, Player.character_name).where(Player.user_id.in_(seller_ids))
    )
    return {row.user_id: (row.character_name or "Unknown") for row in result}


async def get_player_listings(user_id: int, session) -> list:
    from core.models import MarketListing
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(MarketListing).where(
            MarketListing.seller_id == user_id,
            MarketListing.status    == "active",
            MarketListing.expires_at > now,
        )
    )
    return result.scalars().all()


async def create_listing(seller_id: int, item_id: str, quantity: int, price_per: int, session) -> tuple[bool, str]:
    from core.models import MarketListing
    from game.data import get_item
    from game.world import deduct_zet, get_inventory, remove_item

    item = get_item(item_id)
    if not item:
        return False, "Unknown item."
    if item.get("type") in UNLISTED_ITEM_TYPES:
        return False, f"**{item['name']}** cannot be listed on the market."
    if price_per < 1:
        return False, "Price must be at least 1 Ƶ."
    if quantity < 1:
        return False, "Quantity must be at least 1."

    active = await get_player_listings(seller_id, session)
    if len(active) >= MAX_LISTINGS:
        return False, f"You already have {MAX_LISTINGS} active listings. Cancel one first."

    inv = await get_inventory(seller_id, session)
    inv_entry = next((e for e in inv if e["item_id"] == item_id), None)
    if not inv_entry or inv_entry["quantity"] < quantity:
        has = inv_entry["quantity"] if inv_entry else 0
        return False, f"You only have {has}× {item['name']}."

    total_price = price_per * quantity
    fee = max(1, int(total_price * LISTING_FEE_PCT))
    if not await deduct_zet(seller_id, fee, session):
        return False, f"You need **{fee} Ƶ** for the listing fee (5%)."

    await remove_item(seller_id, item_id, quantity, session)

    session.add(MarketListing(
        seller_id       = seller_id,
        item_id         = item_id,
        card_id         = None,
        price           = total_price,
        quantity        = quantity,
        listing_fee_paid= fee,
        listed_at       = datetime.now(timezone.utc),
        expires_at      = datetime.now(timezone.utc) + timedelta(hours=LISTING_HOURS),
        status          = "active",
    ))
    return True, (
        f"Listed **{quantity}× {item['emoji']} {item['name']}** at **{price_per:,} Ƶ each**.\n"
        f"Total: {total_price:,} Ƶ · Fee charged: {fee} Ƶ · Expires in {LISTING_HOURS}h."
    )


async def buy_listing(buyer_id: int, listing_id: int, session) -> tuple[bool, str]:
    from core.models import MarketListing
    from game.data import get_item
    from game.world import add_zet, deduct_zet, safe_add_item

    result  = await session.execute(select(MarketListing).where(MarketListing.id == listing_id))
    listing = result.scalar_one_or_none()

    if not listing:
        return False, "Listing not found — it may have been sold already."
    if listing.status != "active":
        return False, "This listing is no longer available."
    if listing.expires_at and datetime.now(timezone.utc) >= listing.expires_at:
        listing.status = "expired"
        return False, "This listing has expired."
    if listing.seller_id == buyer_id:
        return False, "You cannot buy your own listing."

    item       = get_item(listing.item_id) if listing.item_id else None
    item_name  = item["name"]  if item else (listing.item_id or "Unknown")
    item_emoji = item["emoji"] if item else "📦"

    if not await deduct_zet(buyer_id, listing.price, session):
        return False, f"You need **{listing.price:,} Ƶ** but don't have enough."

    if listing.item_id:
        success, msg = await safe_add_item(buyer_id, listing.item_id, listing.quantity, session)
        if not success:
            await add_zet(buyer_id, listing.price, session)
            return False, f"Can't receive item: {msg}"

    await add_zet(listing.seller_id, listing.price, session)
    listing.status   = "sold"
    listing.buyer_id = buyer_id

    price_per = listing.price // max(listing.quantity, 1)
    return True, (
        f"Purchased **{listing.quantity}× {item_emoji} {item_name}** "
        f"for **{listing.price:,} Ƶ** ({price_per:,} Ƶ each)."
    )


async def cancel_listing(seller_id: int, listing_id: int, session) -> tuple[bool, str]:
    from core.models import MarketListing
    from game.data import get_item
    from game.world import add_item, safe_add_item

    result  = await session.execute(
        select(MarketListing).where(MarketListing.id == listing_id, MarketListing.seller_id == seller_id)
    )
    listing = result.scalar_one_or_none()

    if not listing:
        return False, "Listing not found."
    if listing.status != "active":
        return False, "This listing is already closed."

    listing.status = "cancelled"
    if listing.item_id:
        success, _ = await safe_add_item(seller_id, listing.item_id, listing.quantity, session)
        if not success:
            await add_item(seller_id, listing.item_id, listing.quantity, session)

    item = get_item(listing.item_id) if listing.item_id else None
    name = item["name"] if item else (listing.item_id or "item")
    return True, f"Cancelled. **{listing.quantity}× {name}** returned to your bag."


# ---------------------------------------------------------------------------
# NPC Sell
# ---------------------------------------------------------------------------

def get_npc_buy_price(item_id: str, npc_id: str | None = None) -> int:
    from game.data import get_item
    item = get_item(item_id)
    if not item:
        return 0
    sell_price = item.get("sell_price", 0)
    if sell_price == 0:
        return 0
    if npc_id and item.get("type") in NPC_SPECIALTY.get(npc_id, []):
        return sell_price
    return max(1, int(sell_price * 0.7))


async def sell_to_npc(user_id: int, item_id: str, quantity: int, npc_id: str | None, session) -> tuple[bool, str]:
    from game.data import get_item
    from game.world import add_zet, remove_item

    item = get_item(item_id)
    if not item:
        return False, "Unknown item."
    if item.get("type") in {"key_item", "bag_upgrade", "cosmetic"}:
        return False, f"**{item['name']}** cannot be sold."

    price = get_npc_buy_price(item_id, npc_id)
    if price == 0:
        return False, f"No one is buying **{item['name']}** right now."

    if not await remove_item(user_id, item_id, quantity, session):
        return False, f"You don't have {quantity}× {item['name']}."

    total = price * quantity
    await add_zet(user_id, total, session)
    return True, f"Sold **{quantity}× {item['emoji']} {item['name']}** for **{total:,} Ƶ** (+{price:,} each)."


async def get_sellable_inventory(user_id: int, npc_id: str | None, session) -> list[dict]:
    from game.world import get_inventory
    inv    = await get_inventory(user_id, session)
    return [{**e, "buy_price": p} for e in inv if (p := get_npc_buy_price(e["item_id"], npc_id)) > 0]