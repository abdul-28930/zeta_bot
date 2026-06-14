"""
Walk Engine — Zeta

9 event types. All zone-specific. No repeat until full cycle.
Gathering nodes added as event type 9.

Save this as: game/walk.py
"""
import random

from game.walk_data import get_walk_data, get_travel_line
from game.data import get_zone
from game.gathering import (
    ZONE_GATHERING_CHANCE,
    DEFAULT_GATHERING_CHANCE,
    ZONE_NODE_POOLS,
    pick_gathering_node,
)

# ---------------------------------------------------------------------------
# XP
# ---------------------------------------------------------------------------
STEP_XP_FULL   = 3
STEP_XP_HALF   = 1
STEP_XP_MIN    = 1
NPC_MOMENT_XP  = 2
DISCOVERY_XP   = 8
ITEM_FIND_XP   = 5
OVERHEARD_XP   = 3
RUMOUR_XP      = 3
LORE_XP        = 2
GATHERING_XP   = 2   # small bonus just for discovering the node


def calc_step_xp(daily_steps: int) -> int:
    if daily_steps <= 20:   return STEP_XP_FULL
    elif daily_steps <= 40: return STEP_XP_HALF
    return STEP_XP_MIN


# ---------------------------------------------------------------------------
# Event weights — encounter rate scales with zone danger
# ---------------------------------------------------------------------------

ZONE_ENCOUNTER_CHANCE = {
    "town_square":      5,
    "market_quarter":   5,
    "residential_ward": 5,
    "fishermans_cove":  8,
    "farmlands":        10,
    "harbour_docks":    12,
    "port_district":    15,
    "ashwood_forest":   22,
    "smugglers_trail":  25,
    "ancient_ruins":    25,
    "cursed_grove":     30,
    "sea_caves":        30,
    "shadow_den":       35,
}
DEFAULT_ENCOUNTER_CHANCE = 15


def _build_weights(zone_id: str, zone_data: dict, walk_data: dict, zone_cleared: bool = False) -> dict:
    enc_chance = ZONE_ENCOUNTER_CHANCE.get(zone_id, DEFAULT_ENCOUNTER_CHANCE)

    # Phase 3: zone cleared by player — suppress encounters, redirect weight to quiet
    if zone_cleared:
        enc_chance = 0

    # Gathering chance — only in zones that have node pools
    has_nodes  = bool(ZONE_NODE_POOLS.get(zone_id))
    g_chance   = ZONE_GATHERING_CHANCE.get(zone_id, DEFAULT_GATHERING_CHANCE) if has_nodes else 0

    remaining  = 100 - enc_chance - g_chance

    w = {
        "quiet":          int(remaining * 0.30),
        "encounter":      enc_chance,
        "gathering_node": g_chance,
        "npc_moment":     int(remaining * 0.12),
        "discovery":      int(remaining * 0.09),
        "item_find":      int(remaining * 0.14),
        "overheard":      int(remaining * 0.14),
        "rumour":         int(remaining * 0.11),
        "lore_fragment":  int(remaining * 0.10),
    }

    def spill(key: str, fallback: str = "quiet"):
        amt = w.pop(key, 0)
        w[fallback] = w.get(fallback, 0) + amt

    if not zone_data.get("enemy_ids"):          spill("encounter")
    if not has_nodes:                            spill("gathering_node")
    if not walk_data.get("npc_moments"):         spill("npc_moment")
    if not walk_data.get("discoveries"):         spill("discovery")
    if not walk_data.get("item_finds"):          spill("item_find")
    if not walk_data.get("overheard"):           spill("overheard")
    if not walk_data.get("rumours"):             spill("rumour")
    if not (walk_data.get("lore_fragments") or walk_data.get("lore")):
        spill("lore_fragment")

    return w


def roll_event(zone_data: dict, walk_data: dict, zone_id: str = "", zone_cleared: bool = False) -> str:
    w       = _build_weights(zone_id, zone_data, walk_data, zone_cleared=zone_cleared)
    events  = [e for e, v in w.items() if v > 0]
    weights = [w[e] for e in events]
    return random.choices(events, weights=weights, k=1)[0]


# ---------------------------------------------------------------------------
# No-repeat picker
# ---------------------------------------------------------------------------
async def pick_unique(pool: list, user_id: int, zone_id: str, content_type: str):
    if not pool:
        return None, -1
    from core.cache import get_seen_indices, mark_seen
    seen      = await get_seen_indices(user_id, zone_id, content_type)
    available = [i for i in range(len(pool)) if i not in seen]
    if not available:
        available = list(range(len(pool)))
    idx = random.choice(available)
    await mark_seen(user_id, zone_id, content_type, idx, len(pool))
    return pool[idx], idx


# ---------------------------------------------------------------------------
# Content pickers
# ---------------------------------------------------------------------------
async def pick_atmosphere(walk_data: dict, user_id: int, zone_id: str) -> str:
    pool    = walk_data.get("atmosphere", ["You move through the area."])
    item, _ = await pick_unique(pool, user_id, zone_id, "atmosphere")
    return item or pool[0]


async def pick_quote(walk_data: dict, user_id: int, zone_id: str):
    pool = []
    if walk_data.get("quotes"):
        pool.extend([("quote", q) for q in walk_data["quotes"]])
    if walk_data.get("lore"):
        pool.extend([("lore", l) for l in walk_data["lore"]])
    if not pool: return None
    item, _ = await pick_unique(pool, user_id, zone_id, "quotes")
    if not item: return None
    kind, content = item
    return content if kind == "quote" else (content, "")


async def pick_overheard(walk_data: dict, user_id: int, zone_id: str) -> str | None:
    pool    = walk_data.get("overheard", [])
    item, _ = await pick_unique(pool, user_id, zone_id, "overheard")
    return item


async def pick_rumour(walk_data: dict, user_id: int, zone_id: str) -> str | None:
    pool    = walk_data.get("rumours", [])
    item, _ = await pick_unique(pool, user_id, zone_id, "rumours")
    return item


async def pick_lore_fragment(walk_data: dict, user_id: int, zone_id: str) -> str | None:
    pool    = walk_data.get("lore_fragments", []) or walk_data.get("lore", [])
    item, _ = await pick_unique(pool, user_id, zone_id, "lore_fragments")
    return item


async def pick_item_find(walk_data: dict, user_id: int, zone_id: str) -> dict | None:
    items = walk_data.get("item_finds", [])
    if not items: return None
    weights = [i.get("weight", 10) for i in items]
    return random.choices(items, weights=weights, k=1)[0]


def pick_npc_moment(walk_data: dict) -> dict | None:
    moments = walk_data.get("npc_moments", [])
    return random.choice(moments) if moments else None


def pick_discovery(walk_data: dict) -> dict | None:
    items = walk_data.get("discoveries", [])
    return random.choice(items) if items else None


def pick_enemy(zone_data: dict) -> str | None:
    enemies = zone_data.get("enemy_ids", [])
    return random.choice(enemies) if enemies else None


# ---------------------------------------------------------------------------
# Main walk handler
# ---------------------------------------------------------------------------
async def process_walk_step(
    user_id:      int,
    zone_id:      str,
    daily_steps:  int,
    total_steps:  int,
    zone_cleared: bool = False,   # Phase 3: suppress encounters when zone is cleared
) -> dict:
    zone_data = get_zone(zone_id) or {}
    walk_data = get_walk_data(zone_id)

    new_daily = daily_steps + 1
    new_total = total_steps + 1
    xp        = calc_step_xp(new_daily)
    event     = roll_event(zone_data, walk_data, zone_id, zone_cleared=zone_cleared)

    result = {
        "event_type":            event,
        "atmosphere":            await pick_atmosphere(walk_data, user_id, zone_id),
        "xp_gained":             xp,
        "daily_steps":           new_daily,
        "total_steps":           new_total,
        "quote":                 await pick_quote(walk_data, user_id, zone_id),
        "npc_moment":            None,
        "discovery":             None,
        "enemy_id":              None,
        "item_find":             None,
        "overheard":             None,
        "rumour":                None,
        "lore_fragment":         None,
        "gathering_node":        None,
        "mastery_milestone":     None,
        "xp_cap_warning":        new_daily == 21,
        "relationship_npc_name": None,
    }

    if event == "npc_moment":
        result["npc_moment"]  = pick_npc_moment(walk_data)
        result["xp_gained"]  += NPC_MOMENT_XP

    elif event == "discovery":
        result["discovery"]   = pick_discovery(walk_data)
        result["xp_gained"]  += DISCOVERY_XP

    elif event == "encounter":
        result["enemy_id"]    = pick_enemy(zone_data)

    elif event == "item_find":
        result["item_find"]   = await pick_item_find(walk_data, user_id, zone_id)
        result["xp_gained"]  += ITEM_FIND_XP

    elif event == "overheard":
        result["overheard"]   = await pick_overheard(walk_data, user_id, zone_id)
        result["xp_gained"]  += OVERHEARD_XP

    elif event == "rumour":
        result["rumour"]      = await pick_rumour(walk_data, user_id, zone_id)
        result["xp_gained"]  += RUMOUR_XP

    elif event == "lore_fragment":
        result["lore_fragment"] = await pick_lore_fragment(walk_data, user_id, zone_id)
        result["xp_gained"]    += LORE_XP

    elif event == "gathering_node":
        node = pick_gathering_node(zone_id)
        if node:
            result["gathering_node"] = node
            result["xp_gained"]     += GATHERING_XP
        else:
            result["event_type"] = "quiet"

    # Zet drop — 20% chance per step
    import random as _rng
    zet_range = walk_data.get("zet_drop_range", (1, 10))
    if _rng.random() < 0.20:
        result["zet_dropped"] = _rng.randint(zet_range[0], zet_range[1])
    else:
        result["zet_dropped"] = 0

    # Zone mastery milestones
    from core.cache import check_mastery_milestone
    from game.walk_data import MASTERY_TIERS, ZONE_MASTERY_LORE

    milestone_data = None
    milestone_steps = await check_mastery_milestone(user_id, zone_id, new_total)
    if milestone_steps:
        tier = MASTERY_TIERS.get(milestone_steps, {})
        lore = ZONE_MASTERY_LORE.get(zone_id, {}).get(milestone_steps, "")
        result["xp_gained"] += tier.get("xp", 0)
        milestone_data = {
            "steps": milestone_steps,
            "label": tier.get("label", "Zone Mastery"),
            "emoji": tier.get("emoji", "🏔"),
            "xp":    tier.get("xp", 0),
            "lore":  lore,
        }

    result["mastery_milestone"] = milestone_data
    return result