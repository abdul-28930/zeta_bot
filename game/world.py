"""
World helpers — fetch and mutate player state in the database.
"""
import json as _json
from datetime import datetime, timezone

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    DialogueTurn,
    NPCRelationship,
    Player,
    PlayerBank,
    PlayerCardCollection,
    PlayerDeck,
    PlayerFlag,
    PlayerInventory,
    PlayerProgression,
    PlayerStats,
    PlayerStoryletProgress,
)
from game.data import CLASSES, RACES, XP_THRESHOLDS, get_class, get_race

BAG_DEFAULT_CAPACITY = 20


# ---------------------------------------------------------------------------
# Player fetch
# ---------------------------------------------------------------------------

async def get_player(user_id: int, session: AsyncSession) -> Player | None:
    result = await session.execute(select(Player).where(Player.user_id == user_id))
    return result.scalar_one_or_none()


async def get_full_player(user_id: int, session: AsyncSession) -> Player | None:
    result = await session.execute(select(Player).where(Player.user_id == user_id))
    player = result.scalar_one_or_none()
    if player:
        _ = player.stats
        _ = player.progression
    return player


# ---------------------------------------------------------------------------
# Player creation
# ---------------------------------------------------------------------------

async def create_player(
    user_id: int,
    discord_name: str,
    character_name: str,
    race_id: str,
    class_id: str,
    session: AsyncSession,
) -> Player:
    race = RACES[race_id]
    cls  = CLASSES[class_id]

    base = cls["base_stats"].copy()
    for stat, bonus in race.get("base_stat_bonus", {}).items():
        key_map = {
            "strength": "strength", "defense": "defense", "agility": "agility",
            "intel": "intel", "vit": "vit", "lck": "lck",
            "str": "strength", "def": "defense", "agi": "agility", "int": "intel",
        }
        mapped = key_map.get(stat, stat)
        if mapped in base:
            base[mapped] = base[mapped] + bonus

    existing = await session.get(Player, user_id)
    if existing:
        existing.discord_name    = discord_name
        existing.character_name  = character_name
        existing.race_id         = race_id
        existing.class_id        = class_id
        existing.char_created    = True
        player = existing
    else:
        player = Player(
            user_id=user_id, discord_name=discord_name, character_name=character_name,
            race_id=race_id, class_id=class_id, char_created=True,
        )
        session.add(player)
    await session.flush()

    stats = PlayerStats(
        user_id=user_id,
        strength=base.get("strength", 5),
        defense=base.get("defense", 5),
        agility=base.get("agility", 5),
        intel=base.get("intel", 5),
        vit=base.get("vit", 5),
        lck=base.get("lck", 1),
    )
    session.add(stats)

    max_hp = stats.vit * 5
    progression = PlayerProgression(
        user_id=user_id, level=1, xp=0, zet_wallet=100,
        current_hp=max_hp, current_zone_id="town_square",
    )
    session.add(progression)

    bank = PlayerBank(user_id=user_id, zet_balance=0)
    session.add(bank)

    for card_id in cls["starter_deck"]:
        existing_col = await session.execute(
            select(PlayerCardCollection).where(
                PlayerCardCollection.user_id == user_id,
                PlayerCardCollection.card_id == card_id,
            )
        )
        existing_row = existing_col.scalar_one_or_none()
        if existing_row:
            existing_row.quantity += 1
        else:
            session.add(PlayerCardCollection(user_id=user_id, card_id=card_id, quantity=1, obtained_from="starter"))

        deck_existing = await session.execute(
            select(PlayerDeck).where(
                PlayerDeck.user_id == user_id,
                PlayerDeck.card_id == card_id,
            )
        )
        deck_row = deck_existing.scalar_one_or_none()
        if deck_row:
            deck_row.quantity += 1
        else:
            session.add(PlayerDeck(user_id=user_id, card_id=card_id, quantity=1))

    return player


# ---------------------------------------------------------------------------
# Zone movement
# ---------------------------------------------------------------------------

async def update_player_zone(user_id: int, zone_id: str, session: AsyncSession) -> None:
    await session.execute(
        update(PlayerProgression)
        .where(PlayerProgression.user_id == user_id)
        .values(current_zone_id=zone_id, current_building_id=None)
    )


# ---------------------------------------------------------------------------
# HP management
# ---------------------------------------------------------------------------

async def update_player_hp(user_id: int, new_hp: int, session: AsyncSession) -> None:
    await session.execute(
        update(PlayerProgression)
        .where(PlayerProgression.user_id == user_id)
        .values(current_hp=new_hp)
    )


async def full_heal_player(user_id: int, session: AsyncSession) -> None:
    result = await session.execute(select(PlayerStats).where(PlayerStats.user_id == user_id))
    stats = result.scalar_one_or_none()
    if stats:
        await session.execute(
            update(PlayerProgression)
            .where(PlayerProgression.user_id == user_id)
            .values(current_hp=stats.vit * 5)
        )


# ---------------------------------------------------------------------------
# Economy
# ---------------------------------------------------------------------------

async def deduct_zet(user_id: int, amount: int, session: AsyncSession) -> bool:
    result = await session.execute(select(PlayerProgression).where(PlayerProgression.user_id == user_id))
    prog = result.scalar_one_or_none()
    if not prog or prog.zet_wallet < amount:
        return False
    prog.zet_wallet -= amount
    return True


async def add_zet(user_id: int, amount: int, session: AsyncSession) -> None:
    result = await session.execute(select(PlayerProgression).where(PlayerProgression.user_id == user_id))
    prog = result.scalar_one_or_none()
    if prog:
        prog.zet_wallet += amount


# ---------------------------------------------------------------------------
# XP + leveling
# ---------------------------------------------------------------------------

async def add_xp(user_id: int, xp: int, session: AsyncSession) -> dict:
    result = await session.execute(select(PlayerProgression).where(PlayerProgression.user_id == user_id))
    prog = result.scalar_one_or_none()
    if not prog:
        return {"leveled_up": False, "new_level": 1, "xp_gained": xp, "upgraded_cards": []}

    stats_result = await session.execute(select(PlayerStats).where(PlayerStats.user_id == user_id))
    stats = stats_result.scalar_one_or_none()

    player_result = await session.execute(select(Player).where(Player.user_id == user_id))
    player = player_result.scalar_one_or_none()
    if player and player.race_id == "human":
        xp = int(xp * 1.15)

    prog.xp += xp
    leveled_up = False

    while True:
        threshold = _xp_threshold(prog.level)
        if prog.xp >= threshold and prog.level < 50:
            prog.xp     -= threshold
            prog.level  += 1
            leveled_up   = True
            if stats:
                stats.unspent_points += 2
                prog.current_hp = stats.vit * 5
        else:
            break

    # Auto-level cards when player levels up
    upgraded_cards = []
    if leveled_up:
        upgraded_cards = await level_up_cards(user_id, prog.level, session)

    return {
        "leveled_up":     leveled_up,
        "new_level":      prog.level,
        "xp_gained":      xp,
        "upgraded_cards": upgraded_cards,
    }


def _xp_threshold(level: int) -> int:
    if level <= len(XP_THRESHOLDS):
        return XP_THRESHOLDS[min(level - 1, len(XP_THRESHOLDS) - 1)]
    return 20000 + (level - 11) * 8000


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------

async def get_inventory(user_id: int, session: AsyncSession) -> list[dict]:
    result = await session.execute(
        select(PlayerInventory).where(PlayerInventory.user_id == user_id)
    )
    rows = result.scalars().all()
    return [{"item_id": r.item_id, "quantity": r.quantity, "id": r.id} for r in rows]


async def add_item(user_id: int, item_id: str, quantity: int, session: AsyncSession) -> None:
    """Add item regardless of capacity. Use safe_add_item for capacity-checked adds."""
    result = await session.execute(
        select(PlayerInventory).where(
            PlayerInventory.user_id == user_id,
            PlayerInventory.item_id == item_id,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.quantity += quantity
    else:
        session.add(PlayerInventory(user_id=user_id, item_id=item_id, quantity=quantity))


async def remove_item(user_id: int, item_id: str, quantity: int, session: AsyncSession) -> bool:
    """Remove qty of an item from inventory. Returns True if successful."""
    result = await session.execute(
        select(PlayerInventory).where(
            PlayerInventory.user_id == user_id,
            PlayerInventory.item_id == item_id,
        )
    )
    existing = result.scalar_one_or_none()
    if not existing or existing.quantity < quantity:
        return False
    existing.quantity -= quantity
    if existing.quantity <= 0:
        await session.delete(existing)
    return True


async def use_consumable(user_id: int, item_id: str, session: AsyncSession) -> dict:
    """
    Use a consumable item outside of battle.
    Returns {success: bool, message: str}

    Heal items: restore HP up to max.
    Cleanse/revive items: battle-only, returns error.
    """
    from game.data import get_item

    item = get_item(item_id)
    if not item or item.get("type") != "consumable":
        return {"success": False, "message": "That item can't be used from the bag."}

    # Verify player owns it
    result = await session.execute(
        select(PlayerInventory).where(
            PlayerInventory.user_id == user_id,
            PlayerInventory.item_id == item_id,
        )
    )
    if not result.scalar_one_or_none():
        return {"success": False, "message": f"You don't have **{item['name']}**."}

    effect      = item.get("effect") or {}
    effect_type = effect.get("type")
    player      = await get_full_player(user_id, session)
    max_hp      = player.stats.vit * 5
    current_hp  = player.progression.current_hp

    if effect_type == "heal":
        if current_hp >= max_hp:
            return {"success": False, "message": f"Already at full HP. ({current_hp}/{max_hp})"}
        heal_val  = effect.get("value", 0)
        new_hp    = min(max_hp, current_hp + heal_val)
        healed    = new_hp - current_hp
        await update_player_hp(user_id, new_hp, session)
        await remove_item(user_id, item_id, 1, session)
        return {
            "success": True,
            "message": (
                f"Used **{item['emoji']} {item['name']}**. "
                f"Restored **+{healed} HP**. ({new_hp}/{max_hp})"
            ),
        }

    elif effect_type in ("cleanse", "revive"):
        return {"success": False, "message": f"**{item['name']}** can only be used during battle."}

    else:
        return {"success": False, "message": f"**{item['name']}** can't be used here."}


# ---------------------------------------------------------------------------
# Bag capacity system
# ---------------------------------------------------------------------------

async def get_bag_capacity(user_id: int, session: AsyncSession) -> int:
    """Return the player's current bag capacity (slot count). Default 20."""
    result = await session.execute(
        select(PlayerFlag).where(
            PlayerFlag.user_id == user_id,
            PlayerFlag.key == "bag_capacity",
        )
    )
    flag = result.scalar_one_or_none()
    return int(flag.value) if flag else BAG_DEFAULT_CAPACITY


async def get_bag_slot_count(user_id: int, session: AsyncSession) -> int:
    """Return how many unique item slots are currently used."""
    result = await session.execute(
        select(func.count(PlayerInventory.item_id)).where(
            PlayerInventory.user_id == user_id
        )
    )
    return result.scalar() or 0


async def is_bag_full(user_id: int, session: AsyncSession) -> bool:
    capacity = await get_bag_capacity(user_id, session)
    slots    = await get_bag_slot_count(user_id, session)
    return slots >= capacity


async def upgrade_bag(user_id: int, new_capacity: int, session: AsyncSession) -> bool:
    """
    Upgrade bag to new_capacity. Never downgrades.
    Returns True if upgrade was applied.
    """
    current = await get_bag_capacity(user_id, session)
    if new_capacity <= current:
        return False
    await set_flag(user_id, "bag_capacity", str(new_capacity), session)
    return True


async def safe_add_item(
    user_id: int,
    item_id: str,
    quantity: int,
    session: AsyncSession,
) -> tuple[bool, str]:
    """
    Add item to bag with catalog check + capacity check.
    Returns (success: bool, message: str).
    """
    from game.data import get_item
    item = get_item(item_id)
    if not item:
        print(f"[Inventory] Item '{item_id}' not in catalog — skipping")
        return False, f"Unknown item: {item_id}"

    # Stacking — check if item already in bag (no new slot needed)
    result = await session.execute(
        select(PlayerInventory).where(
            PlayerInventory.user_id == user_id,
            PlayerInventory.item_id == item_id,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.quantity += quantity
        return True, f"+{quantity} {item['name']}"

    # New slot — check capacity
    if await is_bag_full(user_id, session):
        capacity = await get_bag_capacity(user_id, session)
        return False, f"Bag full! ({capacity}/{capacity} slots). Buy a bigger bag from the Market Quarter."

    session.add(PlayerInventory(user_id=user_id, item_id=item_id, quantity=quantity))
    return True, f"Found: {item['emoji']} {item['name']}"


async def use_bag_upgrade_item(
    user_id: int,
    item_id: str,
    session: AsyncSession,
) -> tuple[bool, str]:
    """
    Apply a bag upgrade item from inventory.
    Consumes the item and increases bag capacity.
    Returns (success, message).
    """
    from game.data import get_item
    item = get_item(item_id)
    if not item or item.get("type") != "bag_upgrade":
        return False, "That's not a bag upgrade item."

    new_capacity = item.get("capacity", 0)
    current      = await get_bag_capacity(user_id, session)

    if new_capacity <= current:
        return False, f"Your bag is already {current} slots. This upgrade would be a downgrade."

    result = await session.execute(
        select(PlayerInventory).where(
            PlayerInventory.user_id == user_id,
            PlayerInventory.item_id == item_id,
        )
    )
    inv_row = result.scalar_one_or_none()
    if not inv_row or inv_row.quantity < 1:
        return False, "You don't have that item."

    inv_row.quantity -= 1
    if inv_row.quantity <= 0:
        await session.delete(inv_row)

    await upgrade_bag(user_id, new_capacity, session)
    return True, f"🎒 Bag upgraded to **{new_capacity} slots**!"


# ---------------------------------------------------------------------------
# Cards
# ---------------------------------------------------------------------------

async def get_deck_list(user_id: int, session: AsyncSession) -> list[str]:
    result = await session.execute(select(PlayerDeck).where(PlayerDeck.user_id == user_id))
    rows = result.scalars().all()
    deck = []
    for row in rows:
        deck.extend([row.card_id] * row.quantity)
    return deck


async def add_card_to_collection(user_id: int, card_id: str, session: AsyncSession) -> None:
    result = await session.execute(
        select(PlayerCardCollection).where(
            PlayerCardCollection.user_id == user_id,
            PlayerCardCollection.card_id == card_id,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.quantity += 1
    else:
        session.add(PlayerCardCollection(user_id=user_id, card_id=card_id, quantity=1))


async def add_card_to_deck(user_id: int, card_id: str, session: AsyncSession) -> None:
    result = await session.execute(
        select(PlayerDeck).where(
            PlayerDeck.user_id == user_id,
            PlayerDeck.card_id == card_id,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.quantity += 1
    else:
        session.add(PlayerDeck(user_id=user_id, card_id=card_id, quantity=1))


async def get_card_collection(user_id: int, session: AsyncSession) -> list[dict]:
    """Return all cards in player's collection with level info."""
    result = await session.execute(
        select(PlayerCardCollection).where(PlayerCardCollection.user_id == user_id)
    )
    rows = result.scalars().all()
    return [
        {"card_id": r.card_id, "quantity": r.quantity, "level": r.level}
        for r in rows
    ]


async def get_card_collection_levels(user_id: int, session: AsyncSession) -> dict[str, int]:
    """Return {card_id: level} for all cards — used to populate battle state."""
    result = await session.execute(
        select(PlayerCardCollection).where(PlayerCardCollection.user_id == user_id)
    )
    rows = result.scalars().all()
    return {r.card_id: r.level for r in rows}


async def level_up_cards(
    user_id: int, new_player_level: int, session: AsyncSession
) -> list[str]:
    """
    Auto-level all cards in collection based on new player level.
    Returns list of card names that were upgraded (for display in level-up embed).

    Thresholds (from CARD_LEVEL_THRESHOLDS in data.py):
      Card Lv.1 → player Lv.0+   (always)
      Card Lv.2 → player Lv.5+
      Card Lv.3 → player Lv.10+
      Card Lv.4 → player Lv.20+
      Card Lv.5 → player Lv.35+
    """
    from game.data import CARD_LEVEL_THRESHOLDS, get_card

    # Find what card level this player should be at
    target_card_level = 1
    for card_lvl, player_lvl_req in sorted(CARD_LEVEL_THRESHOLDS.items()):
        if new_player_level >= player_lvl_req:
            target_card_level = card_lvl

    result = await session.execute(
        select(PlayerCardCollection).where(PlayerCardCollection.user_id == user_id)
    )
    rows = result.scalars().all()
    upgraded = []
    for row in rows:
        if target_card_level > row.level:
            row.level = target_card_level
            card = get_card(row.card_id)
            if card:
                upgraded.append(card["name"])
    return upgraded


# ---------------------------------------------------------------------------
# Flags
# ---------------------------------------------------------------------------

async def get_flag(user_id: int, key: str, session: AsyncSession) -> str | None:
    result = await session.execute(
        select(PlayerFlag).where(PlayerFlag.user_id == user_id, PlayerFlag.key == key)
    )
    row = result.scalar_one_or_none()
    return row.value if row else None


async def set_flag(user_id: int, key: str, value: str | None, session: AsyncSession) -> None:
    result = await session.execute(
        select(PlayerFlag).where(PlayerFlag.user_id == user_id, PlayerFlag.key == key)
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.value = value
    else:
        session.add(PlayerFlag(user_id=user_id, key=key, value=value))


# ---------------------------------------------------------------------------
# NPC Relationships
# ---------------------------------------------------------------------------

async def get_or_create_relationship(user_id: int, npc_id: str, session: AsyncSession) -> NPCRelationship:
    result = await session.execute(
        select(NPCRelationship).where(
            NPCRelationship.user_id == user_id,
            NPCRelationship.npc_id == npc_id,
        )
    )
    rel = result.scalar_one_or_none()
    if not rel:
        rel = NPCRelationship(user_id=user_id, npc_id=npc_id)
        session.add(rel)
        await session.flush()
    return rel


async def increment_npc_visit(user_id: int, npc_id: str, session: AsyncSession) -> NPCRelationship:
    rel = await get_or_create_relationship(user_id, npc_id, session)
    rel.visit_count       += 1
    rel.relationship_score = min(100, rel.relationship_score + 1)
    return rel


async def get_dialogue_history(user_id: int, npc_id: str, session: AsyncSession, limit: int = 10) -> list[DialogueTurn]:
    result = await session.execute(
        select(DialogueTurn)
        .where(DialogueTurn.user_id == user_id, DialogueTurn.npc_id == npc_id)
        .order_by(DialogueTurn.id.desc())
        .limit(limit)
    )
    rows = result.scalars().all()
    return list(reversed(rows))


async def save_dialogue_turn(user_id: int, npc_id: str, role: str, content: str, session: AsyncSession) -> None:
    session.add(DialogueTurn(user_id=user_id, npc_id=npc_id, role=role, content=content))


# ---------------------------------------------------------------------------
# Bank — deposit / withdraw
# PlayerBank model already exists (created in create_player).
# Deposit is free. Withdrawal costs 5% (Mercer's cut, lore-accurate).
# ---------------------------------------------------------------------------

async def get_bank_balance(user_id: int, session: AsyncSession) -> int:
    result = await session.execute(
        select(PlayerBank).where(PlayerBank.user_id == user_id)
    )
    bank = result.scalar_one_or_none()
    return bank.zet_balance if bank else 0


async def deposit_to_bank(user_id: int, amount: int, session: AsyncSession) -> tuple[bool, str]:
    if amount < 10:
        return False, "Minimum deposit is **10 Ƶ**."
    result = await session.execute(
        select(PlayerProgression).where(PlayerProgression.user_id == user_id)
    )
    prog = result.scalar_one_or_none()
    if not prog or prog.zet_wallet < amount:
        wallet = prog.zet_wallet if prog else 0
        return False, f"Not enough Ƶ. Wallet: **{wallet:,} Ƶ**."
    bank_result = await session.execute(
        select(PlayerBank).where(PlayerBank.user_id == user_id)
    )
    bank = bank_result.scalar_one_or_none()
    if not bank:
        bank = PlayerBank(user_id=user_id, zet_balance=0)
        session.add(bank)
        await session.flush()
    prog.zet_wallet  -= amount
    bank.zet_balance += amount
    return True, f"Deposited **{amount:,} Ƶ**. Bank balance: **{bank.zet_balance:,} Ƶ**."


async def withdraw_from_bank(user_id: int, amount: int, session: AsyncSession) -> tuple[bool, str]:
    if amount < 10:
        return False, "Minimum withdrawal is **10 Ƶ**."
    bank_result = await session.execute(
        select(PlayerBank).where(PlayerBank.user_id == user_id)
    )
    bank    = bank_result.scalar_one_or_none()
    balance = bank.zet_balance if bank else 0
    if balance < amount:
        return False, f"Not enough in the bank. Balance: **{balance:,} Ƶ**."
    fee    = max(1, int(amount * 0.05))
    payout = amount - fee
    bank.zet_balance -= amount
    result = await session.execute(
        select(PlayerProgression).where(PlayerProgression.user_id == user_id)
    )
    prog = result.scalar_one_or_none()
    if prog:
        prog.zet_wallet += payout
    return (
        True,
        f"Withdrew **{amount:,} Ƶ** — Mercer's fee: **{fee:,} Ƶ** (5%). "
        f"Received: **{payout:,} Ƶ**.",
    )


# ---------------------------------------------------------------------------
# Barn — item storage backed by a PlayerFlag JSON blob.
# Stores {item_id: quantity}. Max BARN_MAX_SLOTS unique item types.
# Blocked types: key_item, bag_upgrade, equipment, cosmetic, lore
# ---------------------------------------------------------------------------

BARN_MAX_SLOTS = 50
_BARN_BLOCKED  = {"key_item", "bag_upgrade", "equipment", "cosmetic", "lore"}


async def get_barn_inventory(user_id: int, session: AsyncSession) -> dict[str, int]:
    flag = await get_flag(user_id, "barn_inventory", session)
    if not flag:
        return {}
    try:
        return _json.loads(flag)
    except Exception:
        return {}


async def deposit_to_barn(user_id: int, item_id: str, session: AsyncSession) -> tuple[bool, str]:
    from game.data import get_item
    item = get_item(item_id)
    if not item:
        return False, "Unknown item."
    if item.get("type") in _BARN_BLOCKED:
        return False, f"**{item['name']}** can't be stored in the barn."

    inv_result = await session.execute(
        select(PlayerInventory).where(
            PlayerInventory.user_id == user_id,
            PlayerInventory.item_id == item_id,
        )
    )
    inv_row = inv_result.scalar_one_or_none()
    if not inv_row or inv_row.quantity <= 0:
        return False, f"You don't have **{item['name']}** in your bag."

    qty  = inv_row.quantity
    barn = await get_barn_inventory(user_id, session)

    if item_id not in barn and len(barn) >= BARN_MAX_SLOTS:
        return False, f"Barn is full! ({len(barn)}/{BARN_MAX_SLOTS} item types)."

    # Remove entire stack from bag
    if inv_row.quantity <= qty:
        await session.delete(inv_row)
    else:
        inv_row.quantity -= qty

    barn[item_id] = barn.get(item_id, 0) + qty
    await set_flag(user_id, "barn_inventory", _json.dumps(barn), session)
    return True, f"Stored **{qty}× {item['emoji']} {item['name']}** in the barn."


async def withdraw_from_barn(user_id: int, item_id: str, session: AsyncSession) -> tuple[bool, str]:
    from game.data import get_item
    item = get_item(item_id)
    if not item:
        return False, "Unknown item."

    barn = await get_barn_inventory(user_id, session)
    qty  = barn.get(item_id, 0)
    if qty <= 0:
        return False, f"**{item['name']}** isn't in the barn."

    if await is_bag_full(user_id, session):
        cap = await get_bag_capacity(user_id, session)
        return False, f"Bag full ({cap}/{cap} slots). Make room first."

    barn.pop(item_id, None)
    await set_flag(user_id, "barn_inventory", _json.dumps(barn), session)
    await add_item(user_id, item_id, qty, session)
    return True, f"Retrieved **{qty}× {item['emoji']} {item['name']}** from the barn."


# ---------------------------------------------------------------------------
# Fish Market — sell any item that has a sell_price > 0.
# No NPC intermediary. Direct Ƶ transfer.
# ---------------------------------------------------------------------------

async def get_fish_market_sellable(user_id: int, session: AsyncSession) -> list[dict]:
    from game.data import get_item
    inv = await get_inventory(user_id, session)
    out = []
    for entry in inv:
        item = get_item(entry["item_id"])
        if item and item.get("sell_price", 0) > 0:
            out.append({
                "item_id":    entry["item_id"],
                "quantity":   entry["quantity"],
                "sell_price": item["sell_price"],
            })
    return sorted(out, key=lambda x: x["sell_price"] * x["quantity"], reverse=True)


async def sell_at_fish_market(
    user_id: int, item_id: str, session: AsyncSession
) -> tuple[bool, str]:
    from game.data import get_item
    item = get_item(item_id)
    if not item or item.get("sell_price", 0) <= 0:
        return False, "Can't sell that here."

    inv_result = await session.execute(
        select(PlayerInventory).where(
            PlayerInventory.user_id == user_id,
            PlayerInventory.item_id == item_id,
        )
    )
    inv_row = inv_result.scalar_one_or_none()
    if not inv_row or inv_row.quantity <= 0:
        return False, f"You don't have any **{item['name']}**."

    qty   = inv_row.quantity
    total = item["sell_price"] * qty

    inv_row.quantity -= qty
    if inv_row.quantity <= 0:
        await session.delete(inv_row)

    prog_result = await session.execute(
        select(PlayerProgression).where(PlayerProgression.user_id == user_id)
    )
    prog = prog_result.scalar_one_or_none()
    if prog:
        prog.zet_wallet += total

    return (
        True,
        f"Sold **{qty}× {item['emoji']} {item['name']}** for **{total:,} Ƶ** "
        f"({item['sell_price']:,} each).",
    )