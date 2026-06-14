"""
Gathering System — Zeta

6 skills: Fishing, Mining, Herbalism, Scavenging, Woodcutting, Excavation
Each skill has: tool requirement, XP, nodes per zone, resources.

DB models required in core/models.py:
  PlayerGatheringSkill  (user_id, skill_type, level, xp)
  PlayerEquipment       (user_id, slot, item_id)

SQL to run in Supabase:
  CREATE TABLE player_gathering_skills (
      user_id    BIGINT REFERENCES players(user_id),
      skill_type VARCHAR(32),
      level      INTEGER DEFAULT 1,
      xp         INTEGER DEFAULT 0,
      PRIMARY KEY (user_id, skill_type)
  );
  CREATE TABLE player_equipment (
      user_id BIGINT REFERENCES players(user_id),
      slot    VARCHAR(32),
      item_id VARCHAR(64),
      PRIMARY KEY (user_id, slot)
  );
"""
import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# ---------------------------------------------------------------------------
# Skill XP thresholds — xp needed TO REACH each level
# ---------------------------------------------------------------------------

SKILL_XP_THRESHOLDS: list[int] = [
    0,     # Lv 1  — starting level
    100,   # Lv 2
    250,   # Lv 3
    500,   # Lv 4
    900,   # Lv 5
    1_500, # Lv 6
    2_500, # Lv 7
    4_000, # Lv 8
    6_000, # Lv 9
    9_000, # Lv 10 (cap for Island 1)
]

SKILL_MAX_LEVEL = 10


def skill_xp_to_next(level: int) -> int:
    idx = min(level, len(SKILL_XP_THRESHOLDS) - 1)
    return SKILL_XP_THRESHOLDS[idx]


# ---------------------------------------------------------------------------
# Skill definitions
# ---------------------------------------------------------------------------

GATHERING_SKILLS: dict[str, dict] = {
    "fishing": {
        "id":          "fishing",
        "name":        "Fishing",
        "emoji":       "🎣",
        "tool_slot":   "fishing_rod",   # must match PlayerEquipment.slot
        "verb":        "Catch",
        "verb_past":   "Caught",
        "xp_per_node": 8,
        "main_xp":     3,
        "description": "Catch fish in coastal and cave waters. Requires a fishing rod.",
    },
    "mining": {
        "id":          "mining",
        "name":        "Mining",
        "emoji":       "⛏️",
        "tool_slot":   "pickaxe",
        "verb":        "Mine",
        "verb_past":   "Mined",
        "xp_per_node": 10,
        "main_xp":     4,
        "description": "Extract ore and crystals from rock formations. Requires a pickaxe.",
    },
    "herbalism": {
        "id":          "herbalism",
        "name":        "Herbalism",
        "emoji":       "🌿",
        "tool_slot":   None,            # no tool required
        "verb":        "Forage",
        "verb_past":   "Foraged",
        "xp_per_node": 6,
        "main_xp":     2,
        "description": "Gather medicinal herbs and plants. No tool required.",
    },
    "scavenging": {
        "id":          "scavenging",
        "name":        "Scavenging",
        "emoji":       "🔍",
        "tool_slot":   None,
        "verb":        "Scavenge",
        "verb_past":   "Scavenged",
        "xp_per_node": 5,
        "main_xp":     2,
        "description": "Find useful items in debris and abandoned areas. No tool required.",
    },
    "woodcutting": {
        "id":          "woodcutting",
        "name":        "Woodcutting",
        "emoji":       "🪓",
        "tool_slot":   "axe",
        "verb":        "Chop",
        "verb_past":   "Chopped",
        "xp_per_node": 9,
        "main_xp":     3,
        "description": "Cut timber from trees. Requires an axe.",
    },
    "excavation": {
        "id":          "excavation",
        "name":        "Excavation",
        "emoji":       "🏺",
        "tool_slot":   "trowel",
        "verb":        "Excavate",
        "verb_past":   "Excavated",
        "xp_per_node": 12,
        "main_xp":     5,
        "description": "Uncover ancient artifacts from ruins and caves. Requires an excavation brush.",
    },
}

# Tool item IDs that satisfy each slot
TOOL_ITEMS: dict[str, list[str]] = {
    "fishing_rod": ["fishing_rod"],
    "pickaxe":     ["rusty_pickaxe", "iron_pickaxe"],
    "axe":         ["weak_axe", "iron_axe"],
    "trowel":      ["excavation_brush"],
}


# ---------------------------------------------------------------------------
# Node definitions
# ---------------------------------------------------------------------------

GATHERING_NODES: dict[str, dict] = {

    # ── Fishing ──────────────────────────────────────────────────────────────
    "goldfish_school": {
        "id":         "goldfish_school",
        "name":       "Goldfish",
        "skill":      "fishing",
        "emoji":      "🐟",
        "rarity":     "common",
        "item_id":    "goldfish",
        "tradable":   True,
        "level_req":  1,
        "weight":     60,
        "walk_text":  "A school of goldfish drifts near the surface, catching the light.",
        "gather_text": "You cast your line. A goldfish takes the bait.",
    },
    "bass_spot": {
        "id":         "bass_spot",
        "name":       "Large Bass",
        "skill":      "fishing",
        "emoji":      "🐠",
        "rarity":     "uncommon",
        "item_id":    "bass",
        "tradable":   True,
        "level_req":  3,
        "weight":     30,
        "walk_text":  "You spot a large bass lurking near the dock supports.",
        "gather_text": "It takes patience. The bass fights. You win.",
    },
    "cave_eel_pool": {
        "id":         "cave_eel_pool",
        "name":       "Cave Eel",
        "skill":      "fishing",
        "emoji":      "🐍",
        "rarity":     "rare",
        "item_id":    "cave_eel",
        "tradable":   True,
        "level_req":  5,
        "weight":     15,
        "walk_text":  "Something long and dark moves through the water channel. A cave eel.",
        "gather_text": "The line goes taut immediately. The cave eel is strong but you're stronger.",
    },

    # ── Mining ───────────────────────────────────────────────────────────────
    "copper_ore_vein": {
        "id":         "copper_ore_vein",
        "name":       "Copper Ore",
        "skill":      "mining",
        "emoji":      "🪨",
        "rarity":     "common",
        "item_id":    "black_ore_fragment",
        "tradable":   True,
        "level_req":  1,
        "weight":     50,
        "walk_text":  "A vein of dark ore is visible where the rock face has cracked open.",
        "gather_text": "The ore comes loose in chunks. It's warm to the touch.",
    },
    "cave_crystal_deposit": {
        "id":         "cave_crystal_deposit",
        "name":       "Cave Crystal",
        "skill":      "mining",
        "emoji":      "💠",
        "rarity":     "uncommon",
        "item_id":    "cave_crystal",
        "tradable":   True,
        "level_req":  4,
        "weight":     30,
        "walk_text":  "A cluster of cave crystals grows from the rock wall. Something dark at the center of each one.",
        "gather_text": "The crystal comes free with a clean tap. It's heavier than it looks.",
    },
    "salt_formation": {
        "id":         "salt_formation",
        "name":       "Salt Rock",
        "skill":      "mining",
        "emoji":      "⬜",
        "rarity":     "common",
        "item_id":    "salt_rock",
        "tradable":   True,
        "level_req":  1,
        "weight":     40,
        "walk_text":  "A natural salt formation on the cave wall. The mineral smell is unusual.",
        "gather_text": "You chip off a section. The smell doesn't match standard salt.",
    },
    "corrupted_ore_seam": {
        "id":         "corrupted_ore_seam",
        "name":       "Corrupted Ore",
        "skill":      "mining",
        "emoji":      "🖤",
        "rarity":     "uncommon",
        "item_id":    "black_ore_fragment",
        "tradable":   True,
        "level_req":  3,
        "weight":     35,
        "walk_text":  "A seam of black ore runs through the corrupted rock. Warm. Wrong.",
        "gather_text": "The ore breaks away from the seam. Whatever process formed it here, it's ongoing.",
    },

    # ── Herbalism ────────────────────────────────────────────────────────────
    "herb_patch": {
        "id":         "herb_patch",
        "name":       "Wild Herbs",
        "skill":      "herbalism",
        "emoji":      "🌿",
        "rarity":     "common",
        "item_id":    "wild_herbs",
        "tradable":   True,
        "level_req":  1,
        "weight":     60,
        "walk_text":  "A patch of wild herbs at the field edge. Medicinal, if you know what to do with them.",
        "gather_text": "You pick the best of the batch. Hana would approve of the selection.",
    },
    "wolfsbane_plant": {
        "id":         "wolfsbane_plant",
        "name":       "Wolfsbane",
        "skill":      "herbalism",
        "emoji":      "🌑",
        "rarity":     "rare",
        "item_id":    "wolfsbane",
        "tradable":   True,
        "level_req":  4,
        "weight":     20,
        "walk_text":  "Wolfsbane growing in the root shadow of a large oak. Hana specifically requests this. Handle carefully.",
        "gather_text": "You harvest it carefully, gloves on. It'll fetch a good price at the Potion Emporium.",
    },
    "kelp_bed": {
        "id":         "kelp_bed",
        "name":       "Kelp Bed",
        "skill":      "herbalism",
        "emoji":      "🌊",
        "rarity":     "common",
        "item_id":    "dried_kelp",
        "tradable":   True,
        "level_req":  1,
        "weight":     50,
        "walk_text":  "A bed of kelp washing against the dock pilings. High quality — probably Grull's preferred spot.",
        "gather_text": "You harvest the best fronds. They'll need to dry but the quality is good.",
    },
    "medicinal_root": {
        "id":         "medicinal_root",
        "name":       "Medicinal Root",
        "skill":      "herbalism",
        "emoji":      "🪴",
        "rarity":     "common",
        "item_id":    "bruised_herb",
        "tradable":   True,
        "level_req":  1,
        "weight":     45,
        "walk_text":  "Medicinal roots growing along the path edge. Slightly damaged but still useful.",
        "gather_text": "You pull them carefully. Bruised at the edges, but Hana can work with these.",
    },

    # ── Scavenging ───────────────────────────────────────────────────────────
    "debris_pile": {
        "id":         "debris_pile",
        "name":       "Debris Pile",
        "skill":      "scavenging",
        "emoji":      "🔍",
        "rarity":     "common",
        "item_id":    "copper_coin",
        "tradable":   True,
        "level_req":  1,
        "weight":     60,
        "walk_text":  "A pile of debris near the wall — someone cleared a doorstep in a hurry.",
        "gather_text": "You sort through it quickly. A coin, some scraps. Worth the minute.",
    },
    "dock_scrap": {
        "id":         "dock_scrap",
        "name":       "Dock Scrap",
        "skill":      "scavenging",
        "emoji":      "🔩",
        "rarity":     "common",
        "item_id":    "rope_scrap",
        "tradable":   True,
        "level_req":  1,
        "weight":     55,
        "walk_text":  "Rope scraps and iron bits left from a recent unloading. Still good material.",
        "gather_text": "Good rope, cut end clean. Someone left in a hurry.",
    },
    "abandoned_cargo": {
        "id":         "abandoned_cargo",
        "name":       "Abandoned Cargo",
        "skill":      "scavenging",
        "emoji":      "📦",
        "rarity":     "uncommon",
        "item_id":    "dropped_manifest",
        "tradable":   False,
        "level_req":  3,
        "weight":     30,
        "walk_text":  "A partially concealed crate in the brush. Someone abandoned it deliberately.",
        "gather_text": "Inside: documentation. The destination column has been crossed out and rewritten. Maren would want to see this.",
    },
    "ruins_debris": {
        "id":         "ruins_debris",
        "name":       "Ruins Debris",
        "skill":      "scavenging",
        "emoji":      "🏚️",
        "rarity":     "uncommon",
        "item_id":    "cracked_seal",
        "tradable":   True,
        "level_req":  2,
        "weight":     35,
        "walk_text":  "Debris at the ruins' edge — old documents, broken seals, scattered coins.",
        "gather_text": "A wax seal, already broken. The Sovereignty insignia. Already opened.",
    },

    # ── Woodcutting ──────────────────────────────────────────────────────────
    "common_tree": {
        "id":         "common_tree",
        "name":       "Common Tree",
        "skill":      "woodcutting",
        "emoji":      "🌳",
        "rarity":     "common",
        "item_id":    "common_wood",
        "tradable":   True,
        "level_req":  1,
        "weight":     60,
        "walk_text":  "A common tree at the field edge. Straight grain, good for general use.",
        "gather_text": "Clean cuts. The wood is solid. Standard timber.",
    },
    "ashwood_tree": {
        "id":         "ashwood_tree",
        "name":       "Ashwood Tree",
        "skill":      "woodcutting",
        "emoji":      "🌲",
        "rarity":     "uncommon",
        "item_id":    "ashwood_plank",
        "tradable":   True,
        "level_req":  3,
        "weight":     35,
        "walk_text":  "An ashwood tree, old and dense. The resin smell is strong here.",
        "gather_text": "The ashwood cuts harder than common timber. The plank is dense, quality material.",
    },
    "cursed_tree": {
        "id":         "cursed_tree",
        "name":       "Corrupted Tree",
        "skill":      "woodcutting",
        "emoji":      "🖤",
        "rarity":     "uncommon",
        "item_id":    "corrupted_bark",
        "tradable":   True,
        "level_req":  4,
        "weight":     25,
        "walk_text":  "A blackened tree at the grove's edge. The discoloration goes all the way through.",
        "gather_text": "The bark comes away in dark slabs. It smells like metal. Worth something to the right buyer.",
    },
    "pine_resin_tree": {
        "id":         "pine_resin_tree",
        "name":       "Pine Resin",
        "skill":      "woodcutting",
        "emoji":      "🫙",
        "rarity":     "common",
        "item_id":    "pine_resin",
        "tradable":   True,
        "level_req":  1,
        "weight":     40,
        "walk_text":  "A pine with a fresh resin bleed along its trunk. The sap is still running.",
        "gather_text": "You tap the resin carefully. Good yield, good quality.",
    },

    # ── Excavation ───────────────────────────────────────────────────────────
    "ancient_site": {
        "id":         "ancient_site",
        "name":       "Ancient Site",
        "skill":      "excavation",
        "emoji":      "🏺",
        "rarity":     "rare",
        "item_id":    "ancient_coin",
        "tradable":   True,
        "level_req":  1,
        "weight":     40,
        "walk_text":  "Disturbed earth near the ruins wall. Deliberate displacement — something was buried here.",
        "gather_text": "A coin pressed flat in the stonework. The markings predate anything in the city's records.",
    },
    "ruins_floor": {
        "id":         "ruins_floor",
        "name":       "Ruins Floor",
        "skill":      "excavation",
        "emoji":      "🗿",
        "rarity":     "uncommon",
        "item_id":    "carved_fragment",
        "tradable":   True,
        "level_req":  2,
        "weight":     35,
        "walk_text":  "A section of floor with carving beneath the grit. Worth brushing out.",
        "gather_text": "Part of the closed-eye symbol. It matches the full carving on the north wall.",
    },
    "cave_deposit": {
        "id":         "cave_deposit",
        "name":       "Cave Deposit",
        "skill":      "excavation",
        "emoji":      "💠",
        "rarity":     "uncommon",
        "item_id":    "cave_crystal",
        "tradable":   True,
        "level_req":  3,
        "weight":     30,
        "walk_text":  "A packed sediment deposit in the cave wall — crystals visible in cross-section.",
        "gather_text": "Careful brushwork. The crystal comes out intact, dark center and all.",
    },
}


# ---------------------------------------------------------------------------
# Zone → node pools
# ---------------------------------------------------------------------------

ZONE_NODE_POOLS: dict[str, list[str]] = {
    "town_square":      ["debris_pile"],
    "market_quarter":   ["debris_pile"],
    "residential_ward": ["debris_pile"],
    "port_district":    ["goldfish_school", "dock_scrap"],
    "harbour_docks":    ["goldfish_school", "bass_spot", "dock_scrap"],
    "farmlands":        ["herb_patch", "medicinal_root", "common_tree", "pine_resin_tree"],
    "fishermans_cove":  ["goldfish_school", "bass_spot", "kelp_bed"],
    "ashwood_forest":   ["copper_ore_vein", "wolfsbane_plant", "herb_patch", "ashwood_tree", "pine_resin_tree"],
    "smugglers_trail":  ["medicinal_root", "abandoned_cargo"],
    "cursed_grove":     ["wolfsbane_plant", "corrupted_ore_seam", "cursed_tree"],
    "ancient_ruins":    ["ancient_site", "ruins_floor", "ruins_debris"],
    "sea_caves":        ["cave_eel_pool", "cave_crystal_deposit", "salt_formation", "cave_deposit"],
    "shadow_den":       ["abandoned_cargo"],
}

# Gathering chance per zone (out of 100, applied after encounter roll)
ZONE_GATHERING_CHANCE: dict[str, int] = {
    "town_square":      4,
    "market_quarter":   4,
    "residential_ward": 5,
    "port_district":    10,
    "harbour_docks":    12,
    "farmlands":        15,
    "fishermans_cove":  18,
    "ashwood_forest":   16,
    "smugglers_trail":  12,
    "cursed_grove":     14,
    "ancient_ruins":    14,
    "sea_caves":        16,
    "shadow_den":       8,
}
DEFAULT_GATHERING_CHANCE = 10


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def get_skill(skill_id: str) -> dict | None:
    return GATHERING_SKILLS.get(skill_id)


def get_node(node_id: str) -> dict | None:
    return GATHERING_NODES.get(node_id)


def pick_gathering_node(zone_id: str) -> dict | None:
    """Pick a random gathering node for the zone, weighted."""
    node_ids = ZONE_NODE_POOLS.get(zone_id, [])
    if not node_ids:
        return None
    nodes = [GATHERING_NODES[nid] for nid in node_ids if nid in GATHERING_NODES]
    if not nodes:
        return None
    weights = [n.get("weight", 20) for n in nodes]
    return random.choices(nodes, weights=weights, k=1)[0]


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

async def get_or_create_skill(
    user_id: int,
    skill_type: str,
    session: AsyncSession,
):
    """Return PlayerGatheringSkill row, creating if it doesn't exist."""
    from core.models import PlayerGatheringSkill
    result = await session.execute(
        select(PlayerGatheringSkill).where(
            PlayerGatheringSkill.user_id  == user_id,
            PlayerGatheringSkill.skill_type == skill_type,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        row = PlayerGatheringSkill(user_id=user_id, skill_type=skill_type)
        session.add(row)
        await session.flush()
    return row


async def add_skill_xp(
    user_id: int,
    skill_type: str,
    xp: int,
    session: AsyncSession,
) -> dict:
    """
    Add skill XP and handle level-ups.
    Returns: {leveled_up: bool, new_level: int, skill_xp_gained: int}
    """
    row = await get_or_create_skill(user_id, skill_type, session)
    row.xp += xp
    leveled_up = False

    while row.level < SKILL_MAX_LEVEL:
        threshold = skill_xp_to_next(row.level)
        if row.xp >= threshold:
            row.xp    -= threshold
            row.level += 1
            leveled_up = True
        else:
            break

    return {
        "leveled_up":     leveled_up,
        "new_level":      row.level,
        "skill_xp_gained": xp,
        "skill_type":     skill_type,
    }


async def get_skill_level(
    user_id: int,
    skill_type: str,
    session: AsyncSession,
) -> tuple[int, int]:
    """Returns (level, xp) for the skill. Default (1, 0) if untracked."""
    from core.models import PlayerGatheringSkill
    result = await session.execute(
        select(PlayerGatheringSkill).where(
            PlayerGatheringSkill.user_id    == user_id,
            PlayerGatheringSkill.skill_type == skill_type,
        )
    )
    row = result.scalar_one_or_none()
    return (row.level, row.xp) if row else (1, 0)


async def get_equipped_tool(
    user_id: int,
    slot: str,
    session: AsyncSession,
) -> str | None:
    """Return equipped item_id for a slot, or None if nothing equipped."""
    from core.models import PlayerEquipment
    result = await session.execute(
        select(PlayerEquipment).where(
            PlayerEquipment.user_id == user_id,
            PlayerEquipment.slot    == slot,
        )
    )
    row = result.scalar_one_or_none()
    return row.item_id if row else None


async def equip_tool(
    user_id: int,
    slot: str,
    item_id: str,
    session: AsyncSession,
) -> tuple[bool, str]:
    """
    Equip an item to a slot. Checks inventory and tool_slot compatibility.
    Returns (success, message).
    """
    from core.models import PlayerEquipment, PlayerInventory
    from game.data import get_item

    item = get_item(item_id)
    if not item:
        return False, "Unknown item."
    if item.get("type") != "tool":
        return False, f"{item['name']} is not a tool."

    # Check player owns it
    inv_result = await session.execute(
        select(PlayerInventory).where(
            PlayerInventory.user_id == user_id,
            PlayerInventory.item_id == item_id,
        )
    )
    if not inv_result.scalar_one_or_none():
        return False, f"You don't have {item['name']} in your bag."

    # Upsert equipment row
    eq_result = await session.execute(
        select(PlayerEquipment).where(
            PlayerEquipment.user_id == user_id,
            PlayerEquipment.slot    == slot,
        )
    )
    row = eq_result.scalar_one_or_none()
    if row:
        row.item_id = item_id
    else:
        session.add(PlayerEquipment(user_id=user_id, slot=slot, item_id=item_id))

    return True, f"⚒️ **{item['name']}** equipped."


async def has_required_tool(
    user_id: int,
    skill_type: str,
    session: AsyncSession,
) -> tuple[bool, str | None]:
    """
    Check if player has the required tool equipped for a skill.
    Returns (has_tool: bool, equipped_item_id: str | None).
    Skills with tool_slot=None always return (True, None).
    """
    skill = get_skill(skill_type)
    if not skill:
        return False, None

    slot = skill.get("tool_slot")
    if not slot:
        return True, None  # no tool required

    item_id = await get_equipped_tool(user_id, slot, session)
    if not item_id:
        return False, None

    # Verify it's still in inventory (could have been sold)
    from core.models import PlayerInventory
    inv_result = await session.execute(
        select(PlayerInventory).where(
            PlayerInventory.user_id == user_id,
            PlayerInventory.item_id == item_id,
        )
    )
    if not inv_result.scalar_one_or_none():
        return False, None  # tool was sold / removed

    return True, item_id


# ---------------------------------------------------------------------------
# Core gather action
# ---------------------------------------------------------------------------

async def process_gather(
    user_id: int,
    node_id: str,
    session: AsyncSession,
) -> dict:
    """
    Attempt to gather from a node.

    Returns dict:
      success       bool
      message       str
      item_name     str | None
      item_emoji    str
      skill_result  dict (from add_skill_xp)
      main_xp       int
      need_tool     bool   — True if blocked by missing tool
      tool_slot     str | None
    """
    from game.data import get_item
    from game.world import safe_add_item, add_xp

    node = get_node(node_id)
    if not node:
        return {"success": False, "message": "Unknown node.", "need_tool": False, "tool_slot": None, "main_xp": 0, "skill_result": {}, "item_name": None, "item_emoji": "❓"}

    skill_id   = node["skill"]
    skill_def  = get_skill(skill_id)
    level_req  = node.get("level_req", 1)

    # Check tool requirement
    has_tool, equipped_id = await has_required_tool(user_id, skill_id, session)
    if not has_tool:
        slot = skill_def.get("tool_slot") if skill_def else None
        return {
            "success":     False,
            "message":     f"You need a **{slot.replace('_', ' ').title()}** equipped to {skill_def['verb'].lower()}.",
            "need_tool":   True,
            "tool_slot":   slot,
            "main_xp":     0,
            "skill_result":{},
            "item_name":   None,
            "item_emoji":  "❓",
        }

    # Check skill level requirement
    skill_level, _ = await get_skill_level(user_id, skill_id, session)
    if skill_level < level_req:
        return {
            "success":     False,
            "message":     f"Requires {skill_def['name']} level {level_req}. Your level: {skill_level}.",
            "need_tool":   False,
            "tool_slot":   None,
            "main_xp":     0,
            "skill_result":{},
            "item_name":   None,
            "item_emoji":  node["emoji"],
        }

    # Add item to bag
    item_id = node["item_id"]
    item    = get_item(item_id)
    if not item:
        return {"success": False, "message": f"Item {item_id} not found in catalog.", "need_tool": False, "tool_slot": None, "main_xp": 0, "skill_result": {}, "item_name": None, "item_emoji": "❓"}

    bag_success, bag_msg = await safe_add_item(user_id, item_id, 1, session)
    if not bag_success:
        return {
            "success":     False,
            "message":     bag_msg,
            "need_tool":   False,
            "tool_slot":   None,
            "main_xp":     0,
            "skill_result":{},
            "item_name":   item["name"],
            "item_emoji":  item["emoji"],
        }

    # Award skill XP
    skill_xp     = node.get("xp_per_node", skill_def["xp_per_node"] if skill_def else 5)
    # Scale skill XP slightly with level
    skill_xp     = int(skill_xp * (1 + (skill_level - 1) * 0.05))
    skill_result = await add_skill_xp(user_id, skill_id, skill_xp, session)

    # Award main XP (small, gathering is a grind activity)
    main_xp = node.get("main_xp", skill_def["main_xp"] if skill_def else 2)
    await add_xp(user_id, main_xp, session)

    verb_past = skill_def["verb_past"] if skill_def else "Gathered"

    return {
        "success":       True,
        "message":       f"{verb_past} **1× {item['emoji']} {item['name']}**.",
        "need_tool":     False,
        "tool_slot":     None,
        "main_xp":       main_xp,
        "skill_result":  skill_result,
        "item_name":     item["name"],
        "item_emoji":    item["emoji"],
        "gather_text":   node.get("gather_text", ""),
        "node_rarity":   node.get("rarity", "common"),
        "tradable":      node.get("tradable", True),
    }