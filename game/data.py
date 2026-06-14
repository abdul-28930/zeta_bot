# =============================================================================
# ZETA — World Data
# All static game data lives here. Player data lives in the DB.
# =============================================================================

# Card level thresholds — key = card level, value = required player level
CARD_LEVEL_THRESHOLDS: dict[int, int] = {
    1: 0,    # Base — all cards start here
    2: 5,    # Player reaches Lv.5  → all cards become Lv.2
    3: 10,   # Player reaches Lv.10 → all cards become Lv.3
    4: 20,   # Player reaches Lv.20 → all cards become Lv.4
    5: 35,   # Player reaches Lv.35 → all cards become Lv.5
}

RARITY_EMOJI: dict[str, str] = {
    "common":    "⬜",
    "rare":      "🔵",
    "epic":      "🟣",
    "legendary": "🟡",
}

# ---------------------------------------------------------------------------
# RACES
# ---------------------------------------------------------------------------

RACES: dict[str, dict] = {
    "human": {
        "id": "human",
        "name": "Human",
        "emoji": "👤",
        "description": "Adaptable survivors who thrive through determination and sheer willpower. Their natural talent for learning makes them exceptional in any field.",
        "passive": "**Adaptable:** +15% XP from all sources.",
        "base_stat_bonus": {"vit": 1, "lck": 2},
        "special_ability": None,
        "lore": "Humans built Ironhaven from nothing. Mercer made them rebuild it for him.",
    },
    "fishman": {
        "id": "fishman",
        "name": "Fishman",
        "emoji": "🐟",
        "description": "Powerful amphibious warriors from the deep seas. Their scaled bodies resist poison and their strength is unmatched in water.",
        "passive": "**Sea Blood:** Immune to Poison status. +2 DEF in water zones.",
        "base_stat_bonus": {"strength": 2, "vit": 1},
        "special_ability": "tidal_surge",
        "lore": "Fishman communities in Ironhaven owe Mercer the most. He controls their fishing waters.",
    },
    "skyborn": {
        "id": "skyborn",
        "name": "Skyborn",
        "emoji": "🌤️",
        "description": "Descendants of people who once lived among the clouds. They carry a natural affinity with wind and the first card they play each battle comes freely.",
        "passive": "**Wind's Gift:** The first card you play each battle costs 0 energy.",
        "base_stat_bonus": {"agility": 2, "intel": 1},
        "special_ability": None,
        "lore": "Skyborn drift through Ironhaven without roots. Mercer considers them transient and therefore harmless. He's wrong.",
    },
    "mink": {
        "id": "mink",
        "name": "Mink",
        "emoji": "🐾",
        "description": "Fur-covered warriors from a proud island nation. Their bodies generate natural electricity and they channel it into devastating melee strikes.",
        "passive": "**Electro:** Each physical card you play deals +1 lightning damage that ignores DEF.",
        "base_stat_bonus": {"agility": 2, "strength": 1},
        "special_ability": "sulong_howl",
        "lore": "Minks in Ironhaven are few. Each one arrived running from something. None of them will say what.",
    },
    "giant": {
        "id": "giant",
        "name": "Giant",
        "emoji": "🏔️",
        "description": "Towering warriors from the North Seas. Their massive frames give them exceptional health and endurance, though they move slower than other races.",
        "passive": "**Titan's Frame:** +20 max HP. -1 AGI.",
        "base_stat_bonus": {"vit": 4, "strength": 2, "agility": -1},
        "special_ability": "titans_roar",
        "lore": "Giants are rare anywhere. In Ironhaven, there's exactly one. Her name is Gru. She runs the dockside crane. Nobody asks her questions.",
    },
}

# ---------------------------------------------------------------------------
# CLASSES
# ---------------------------------------------------------------------------

CLASSES: dict[str, dict] = {
    "warrior": {
        "id": "warrior",
        "name": "Warrior",
        "emoji": "⚔️",
        "archetype": "Aggressive melee DPS",
        "description": "Relentless fighters who hit hard and hit often. Warriors build momentum through combos and reward aggressive play.",
        "base_stats": {"strength": 10, "defense": 7, "agility": 5, "intel": 2, "vit": 8, "lck": 3},
        "starter_deck": ["strike", "strike", "strike", "guard", "guard", "cleave", "cleave", "war_cry", "war_cry", "basic_strike", "basic_strike", "basic_block", "basic_block", "strike", "guard"],
        "subclasses": {
            "berserker": {"name": "Berserker", "level": 25, "path": "Power", "description": "Rage stacks, lifesteal, AoE cleave."},
            "blade_dancer": {"name": "Blade Dancer", "level": 25, "path": "Cunning", "description": "Combo chains, parry-counter, precision finishers."},
        },
    },
    "mage": {
        "id": "mage",
        "name": "Mage",
        "emoji": "🔮",
        "archetype": "Elemental burst caster",
        "description": "Masters of elemental magic who deal devastating burst damage. Mages exploit elemental weaknesses and control the battlefield with status effects.",
        "base_stats": {"strength": 2, "defense": 4, "agility": 5, "intel": 12, "vit": 5, "lck": 2},
        "starter_deck": ["spark", "spark", "spark", "frost_bolt", "frost_bolt", "fireball", "fireball", "mana_flow", "mana_flow", "basic_strike", "basic_block", "spark", "frost_bolt", "mana_flow", "basic_strike"],
        "subclasses": {
            "elementalist": {"name": "Elementalist", "level": 25, "path": "Power", "description": "Dual-element fusion spells, elemental immunity."},
            "warlock": {"name": "Warlock", "level": 25, "path": "Cunning", "description": "Dark magic, curse cards, drain life."},
        },
    },
    "guardian": {
        "id": "guardian",
        "name": "Guardian",
        "emoji": "🛡️",
        "archetype": "Heavy tank",
        "description": "Immovable walls who absorb punishment for their allies. Guardians outlast everything and turn enemy attacks into opportunities.",
        "base_stats": {"strength": 6, "defense": 12, "agility": 2, "intel": 3, "vit": 10, "lck": 2},
        "starter_deck": ["shield_bash", "shield_bash", "shield_bash", "fortress_stance", "fortress_stance", "iron_skin", "iron_skin", "rampart", "rampart", "basic_block", "basic_block", "basic_strike", "shield_bash", "iron_skin", "basic_block"],
        "subclasses": {
            "iron_fortress": {"name": "Iron Fortress", "level": 25, "path": "Power", "description": "Nigh-unbreakable defense, reflect damage."},
            "warlord": {"name": "Warlord", "level": 25, "path": "Cunning", "description": "Lead charges, AoE intimidate, ally buffs."},
        },
    },
    "rogue": {
        "id": "rogue",
        "name": "Rogue",
        "emoji": "🗡️",
        "archetype": "Stealth assassin",
        "description": "Deadly opportunists who strike from the shadows and vanish before retaliation. Rogues build debuff combos and detonate them for massive burst damage.",
        "base_stats": {"strength": 7, "defense": 4, "agility": 11, "intel": 4, "vit": 5, "lck": 4},
        "starter_deck": ["stab", "stab", "stab", "backstab", "backstab", "smoke_bomb", "smoke_bomb", "poison_edge", "poison_edge", "basic_strike", "basic_strike", "basic_block", "stab", "poison_edge", "smoke_bomb"],
        "subclasses": {
            "assassin": {"name": "Assassin", "level": 25, "path": "Power", "description": "One-shot setups, permanent stealth opener."},
            "shadow_dancer": {"name": "Shadow Dancer", "level": 25, "path": "Cunning", "description": "Illusions, dodge stacking, clone cards."},
        },
    },
    "ranger": {
        "id": "ranger",
        "name": "Ranger",
        "emoji": "🏹",
        "archetype": "Ranged hunter",
        "description": "Patient hunters who control the battlefield with traps and precision shots. Rangers set up delayed death traps that punish aggression.",
        "base_stats": {"strength": 6, "defense": 5, "agility": 9, "intel": 6, "vit": 6, "lck": 4},
        "starter_deck": ["arrow_shot", "arrow_shot", "arrow_shot", "rain_of_arrows", "rain_of_arrows", "trap_card", "trap_card", "eagle_eye", "eagle_eye", "basic_strike", "basic_strike", "basic_block", "arrow_shot", "trap_card", "eagle_eye"],
        "subclasses": {
            "sniper": {"name": "Sniper", "level": 25, "path": "Power", "description": "Charge shots, armor-pierce, extreme single-target."},
            "beast_master": {"name": "Beast Master", "level": 25, "path": "Cunning", "description": "Companion cards, animal summons, pack tactics."},
        },
    },
    "cleric": {
        "id": "cleric",
        "name": "Cleric",
        "emoji": "✨",
        "archetype": "Holy healer",
        "description": "Servants of light who sustain through any punishment. Clerics heal, buff, and cleanse debuffs, keeping themselves alive through fights that would destroy anyone else.",
        "base_stats": {"strength": 3, "defense": 6, "agility": 4, "intel": 9, "vit": 10, "lck": 1},
        "starter_deck": ["holy_light", "holy_light", "holy_light", "smite", "smite", "blessing", "blessing", "purge", "purge", "basic_strike", "basic_block", "basic_block", "holy_light", "blessing", "smite"],
        "subclasses": {
            "battle_priest": {"name": "Battle Priest", "level": 25, "path": "Power", "description": "Holy melee hybrid, divine shield, execute."},
            "druid": {"name": "Druid", "level": 25, "path": "Cunning", "description": "Nature magic, terrain control, regeneration."},
        },
    },
}

# ---------------------------------------------------------------------------
# CARDS
# ---------------------------------------------------------------------------

CARDS: dict[str, dict] = {
    "basic_strike": {
        "id": "basic_strike", "name": "Basic Strike", "rarity": "common", "type": "attack",
        "cost": 1, "class_restriction": None, "emoji": "⚔️", "description": "Deal physical damage.",
        "effect": {"type": "damage", "value": 5, "stat_scaling": "str", "scale_factor": 0.3},
    },
    "basic_block": {
        "id": "basic_block", "name": "Basic Block", "rarity": "common", "type": "defense",
        "cost": 1, "class_restriction": None, "emoji": "🛡️", "description": "Gain a small shield.",
        "effect": {"type": "shield", "value": 4, "stat_scaling": "def", "scale_factor": 0.2},
    },
    "strike": {
        "id": "strike", "name": "Strike", "rarity": "common", "type": "attack",
        "cost": 1, "class_restriction": "warrior", "emoji": "⚔️", "description": "A solid physical blow.",
        "effect": {"type": "damage", "value": 8, "stat_scaling": "str", "scale_factor": 0.5},
    },
    "guard": {
        "id": "guard", "name": "Guard", "rarity": "common", "type": "defense",
        "cost": 1, "class_restriction": "warrior", "emoji": "🛡️", "description": "Raise your guard.",
        "effect": {"type": "shield", "value": 6, "stat_scaling": "def", "scale_factor": 0.4},
    },
    "cleave": {
        "id": "cleave", "name": "Cleave", "rarity": "rare", "type": "attack",
        "cost": 2, "class_restriction": "warrior", "emoji": "🗡️", "description": "A wide swing that hits hard.",
        "effect": {"type": "damage", "value": 14, "stat_scaling": "str", "scale_factor": 0.7},
    },
    "war_cry": {
        "id": "war_cry", "name": "War Cry", "rarity": "rare", "type": "skill",
        "cost": 1, "class_restriction": "warrior", "emoji": "📣", "description": "Your next card costs 1 less energy.",
        "effect": {"type": "special", "special": "next_card_discount", "value": 1},
    },
    "berserker_rage": {
        "id": "berserker_rage", "name": "Berserker Rage", "rarity": "epic", "type": "skill",
        "cost": 2, "class_restriction": "warrior", "emoji": "😤", "description": "Gain +3 STR for 2 turns. Draw a card.",
        "effect": {"type": "special", "special": "buff_and_draw", "buff": {"stat": "str", "amount": 3, "turns": 2}, "draw": 1},
    },
    "spark": {
        "id": "spark", "name": "Spark", "rarity": "common", "type": "attack",
        "cost": 1, "class_restriction": "mage", "emoji": "⚡", "description": "A quick magical strike.",
        "effect": {"type": "damage", "value": 7, "stat_scaling": "int", "scale_factor": 0.5, "damage_type": "lightning"},
    },
    "frost_bolt": {
        "id": "frost_bolt", "name": "Frost Bolt", "rarity": "rare", "type": "attack",
        "cost": 2, "class_restriction": "mage", "emoji": "🧊", "description": "Ice damage that slows the enemy.",
        "effect": {"type": "damage", "value": 10, "stat_scaling": "int", "scale_factor": 0.6, "damage_type": "ice", "status": {"name": "slow", "turns": 2, "value": 2}},
    },
    "fireball": {
        "id": "fireball", "name": "Fireball", "rarity": "rare", "type": "attack",
        "cost": 3, "class_restriction": "mage", "emoji": "🔥", "description": "Heavy fire damage, applies Burn.",
        "effect": {"type": "damage", "value": 16, "stat_scaling": "int", "scale_factor": 0.8, "damage_type": "fire", "status": {"name": "burn", "turns": 2, "value": 4}},
    },
    "mana_flow": {
        "id": "mana_flow", "name": "Mana Flow", "rarity": "common", "type": "skill",
        "cost": 0, "class_restriction": "mage", "emoji": "💜", "description": "Draw a card and gain 1 energy.",
        "effect": {"type": "special", "special": "draw_and_energy", "draw": 1, "energy": 1},
    },
    "arcane_surge": {
        "id": "arcane_surge", "name": "Arcane Surge", "rarity": "epic", "type": "attack",
        "cost": 3, "class_restriction": "mage", "emoji": "🌀", "description": "Massive magic blast.",
        "effect": {"type": "damage", "value": 25, "stat_scaling": "int", "scale_factor": 1.0, "damage_type": "arcane"},
    },
    "shield_bash": {
        "id": "shield_bash", "name": "Shield Bash", "rarity": "common", "type": "attack",
        "cost": 2, "class_restriction": "guardian", "emoji": "🛡️", "description": "A heavy shield slam that stuns.",
        "effect": {"type": "damage", "value": 6, "stat_scaling": "def", "scale_factor": 0.4, "status": {"name": "stun", "turns": 1, "value": 0}},
    },
    "fortress_stance": {
        "id": "fortress_stance", "name": "Fortress Stance", "rarity": "rare", "type": "defense",
        "cost": 2, "class_restriction": "guardian", "emoji": "🏰", "description": "Gain a massive shield.",
        "effect": {"type": "shield", "value": 12, "stat_scaling": "def", "scale_factor": 0.7},
    },
    "iron_skin": {
        "id": "iron_skin", "name": "Iron Skin", "rarity": "common", "type": "defense",
        "cost": 1, "class_restriction": "guardian", "emoji": "⛓️", "description": "Harden your body.",
        "effect": {"type": "shield", "value": 5, "stat_scaling": "def", "scale_factor": 0.3},
    },
    "rampart": {
        "id": "rampart", "name": "Rampart", "rarity": "epic", "type": "defense",
        "cost": 2, "class_restriction": "guardian", "emoji": "🗼", "description": "Massive shield + gain +2 DEF for 2 turns.",
        "effect": {"type": "special", "special": "shield_and_buff", "shield": 15, "buff": {"stat": "def", "amount": 2, "turns": 2}},
    },
    "stab": {
        "id": "stab", "name": "Stab", "rarity": "common", "type": "attack",
        "cost": 1, "class_restriction": "rogue", "emoji": "🗡️", "description": "A quick, precise jab.",
        "effect": {"type": "damage", "value": 7, "stat_scaling": "str", "scale_factor": 0.4},
    },
    "backstab": {
        "id": "backstab", "name": "Backstab", "rarity": "rare", "type": "attack",
        "cost": 2, "class_restriction": "rogue", "emoji": "🌑", "description": "Deals 50% more damage if enemy has any debuff.",
        "effect": {"type": "damage", "value": 10, "stat_scaling": "str", "scale_factor": 0.6, "bonus_if_debuffed": 0.5},
    },
    "smoke_bomb": {
        "id": "smoke_bomb", "name": "Smoke Bomb", "rarity": "rare", "type": "skill",
        "cost": 2, "class_restriction": "rogue", "emoji": "💨", "description": "Dodge next attack. Apply Blind to enemy.",
        "effect": {"type": "special", "special": "dodge_and_blind", "dodge_turns": 1, "status": {"name": "blind", "turns": 2, "value": 0}},
    },
    "poison_edge": {
        "id": "poison_edge", "name": "Poison Edge", "rarity": "rare", "type": "attack",
        "cost": 2, "class_restriction": "rogue", "emoji": "☠️", "description": "Hits and applies Poison.",
        "effect": {"type": "damage", "value": 5, "stat_scaling": "str", "scale_factor": 0.3, "status": {"name": "poison", "turns": 3, "value": 3}},
    },
    "arrow_shot": {
        "id": "arrow_shot", "name": "Arrow Shot", "rarity": "common", "type": "attack",
        "cost": 1, "class_restriction": "ranger", "emoji": "🏹", "description": "A clean, precise shot.",
        "effect": {"type": "damage", "value": 7, "stat_scaling": "agi", "scale_factor": 0.4},
    },
    "rain_of_arrows": {
        "id": "rain_of_arrows", "name": "Rain of Arrows", "rarity": "rare", "type": "attack",
        "cost": 3, "class_restriction": "ranger", "emoji": "🌧️", "description": "A volley that hits multiple times.",
        "effect": {"type": "damage", "value": 6, "hits": 3, "stat_scaling": "agi", "scale_factor": 0.3},
    },
    "trap_card": {
        "id": "trap_card", "name": "Snare Trap", "rarity": "rare", "type": "skill",
        "cost": 2, "class_restriction": "ranger", "emoji": "🪤", "description": "Set a trap. Next time the enemy attacks, it takes 12 damage.",
        "effect": {"type": "special", "special": "set_trap", "trap_damage": 12},
    },
    "eagle_eye": {
        "id": "eagle_eye", "name": "Eagle Eye", "rarity": "common", "type": "skill",
        "cost": 0, "class_restriction": "ranger", "emoji": "🦅", "description": "Your next attack card deals +4 damage.",
        "effect": {"type": "special", "special": "damage_buff_next", "value": 4},
    },
    "holy_light": {
        "id": "holy_light", "name": "Holy Light", "rarity": "common", "type": "skill",
        "cost": 2, "class_restriction": "cleric", "emoji": "✨", "description": "Restore HP.",
        "effect": {"type": "heal", "value": 10, "stat_scaling": "int", "scale_factor": 0.6},
    },
    "smite": {
        "id": "smite", "name": "Smite", "rarity": "rare", "type": "attack",
        "cost": 3, "class_restriction": "cleric", "emoji": "⚡", "description": "Holy damage that ignores enemy DEF.",
        "effect": {"type": "damage", "value": 12, "stat_scaling": "int", "scale_factor": 0.7, "ignore_defense": True, "damage_type": "holy"},
    },
    "blessing": {
        "id": "blessing", "name": "Blessing", "rarity": "common", "type": "skill",
        "cost": 1, "class_restriction": "cleric", "emoji": "🙏", "description": "Gain +3 DEF for 2 turns.",
        "effect": {"type": "buff", "buff": {"stat": "def", "amount": 3, "turns": 2}},
    },
    "purge": {
        "id": "purge", "name": "Purge", "rarity": "common", "type": "skill",
        "cost": 1, "class_restriction": "cleric", "emoji": "💫", "description": "Remove all debuffs from yourself.",
        "effect": {"type": "special", "special": "cleanse_all"},
    },
}

# ---------------------------------------------------------------------------
# ZONES
# ---------------------------------------------------------------------------

SEC_ICONS = {"high": "🟢", "medium": "🟡", "low": "🟠", "null": "🔴", "bumpyard": "⚫"}
SEC_COLORS = {"high": 0x5DCAA5, "medium": 0xEF9F27, "low": 0xE8792A, "null": 0xE24B4A, "bumpyard": 0x2B2B2B}

ZONES: dict[str, dict] = {
    "town_square": {
        "id": "town_square", "name": "Town Square", "security": "high", "emoji": "🏛️",
        "description": "The heart of Ironhaven hums with uneasy order. Council soldiers lean against storefronts wearing Mercer's badge beneath the city crest. His portrait watches from every wall. The air smells of salt and something tightly controlled.",
        "connected_to": ["market_quarter", "port_district", "farmlands", "residential_ward"],
        "npcs": ["captain_rel"],
        "buildings": ["training_grounds", "adventurers_guild", "inn", "mercer_bank", "clinic", "council_hall"],
        "enemy_ids": [], "pvp": False, "discovery_xp": 50,
    },
    "market_quarter": {
        "id": "market_quarter", "name": "Market Quarter", "security": "high", "emoji": "🏪",
        "description": "Ironhaven's commercial heart. Stalls sell everything from fresh catches to exotic cards. The prices are fair — Mercer sets them. Shop owners smile at the right times.",
        "connected_to": ["town_square"],
        "npcs": ["old_tomas", "vex", "nurse_hana"],
        "buildings": ["general_store", "card_shop", "potion_emporium", "equipment_shop", "tailor", "auction_house"],
        "enemy_ids": [], "pvp": False, "discovery_xp": 50,
    },
    "residential_ward": {
        "id": "residential_ward", "name": "Residential Ward", "security": "high", "emoji": "🏘️",
        "description": "Rows of modest houses, each with a debt notice on the door. Children play in the street. Their parents work double shifts to keep the lights on. Nobody talks about it.",
        "connected_to": ["town_square"],
        "npcs": [], "buildings": [], "enemy_ids": [], "pvp": False, "discovery_xp": 30,
    },
    "port_district": {
        "id": "port_district", "name": "Port District", "security": "medium", "emoji": "⛵",
        "description": "Busier and less controlled than the town center. Sailors from everywhere pass through. The smell of salt and fish and opportunity. Guard patrols are sparse and lazy here.",
        "connected_to": ["town_square", "harbour_docks", "smugglers_trail"],
        "npcs": ["maren", "bora"],
        "buildings": ["harbour_office", "sailors_tavern", "shipyard"],
        "enemy_ids": ["port_pickpocket", "drunken_sailor"], "pvp": False, "discovery_xp": 60,
    },
    "harbour_docks": {
        "id": "harbour_docks", "name": "Harbour Docks", "security": "medium", "emoji": "⚓",
        "description": "Working waterfront where ships are loaded and unloaded around the clock. Import crates are stacked everywhere. Mercer's tax collectors walk the docks with clipboards.",
        "connected_to": ["port_district", "fishermans_cove"],
        "npcs": [], "buildings": [],
        "enemy_ids": ["bandit_scout", "port_pickpocket"], "pvp": False, "discovery_xp": 60,
    },
    "farmlands": {
        "id": "farmlands", "name": "Farmlands", "security": "medium", "emoji": "🌾",
        "description": "Vast fields worked by farmers who don't own the land they tend. Mercer's rent collectors arrive on the first of every month. At night the bandits push in from the forest edge.",
        "connected_to": ["town_square", "ashwood_forest"],
        "npcs": [], "buildings": ["barn"],
        "enemy_ids": ["bandit_scout"], "pvp": False, "discovery_xp": 60,
    },
    "fishermans_cove": {
        "id": "fishermans_cove", "name": "Fisherman's Cove", "security": "low", "emoji": "🎣",
        "description": "An independent fishing community on the rocky coast. No guards here. The fishermen are proud, poor, and deeply in debt to Mercer's bank. The sea is the only thing he can't control.",
        "connected_to": ["harbour_docks", "sea_caves"],
        "npcs": ["old_grull"], "buildings": ["fish_market", "grulls_shack"],
        "enemy_ids": ["bandit_warrior"], "pvp": True, "discovery_xp": 75,
    },
    "ashwood_forest": {
        "id": "ashwood_forest", "name": "Ashwood Forest", "security": "low", "emoji": "🌲",
        "description": "Dense and dark, declared 'protected conservation land' by the Council. Which is strange, because the sound of picks hitting stone can occasionally be heard from deep within. Bandits operate freely here.",
        "connected_to": ["farmlands", "smugglers_trail", "ancient_ruins", "cursed_grove"],
        "npcs": [], "buildings": [],
        "enemy_ids": ["bandit_warrior", "bandit_archer", "dire_wolf"], "pvp": True, "discovery_xp": 100,
    },
    "smugglers_trail": {
        "id": "smugglers_trail", "name": "Smuggler's Trail", "security": "low", "emoji": "🌫️",
        "description": "A winding back route that connects the port to the forest. Official maps don't show it. Mercer's private mercenaries use it to move ore without going through the docks.",
        "connected_to": ["port_district", "ashwood_forest"],
        "npcs": [], "buildings": [],
        "enemy_ids": ["mercer_mercenary", "bandit_archer"], "pvp": True, "discovery_xp": 100,
    },
    "ancient_ruins": {
        "id": "ancient_ruins", "name": "Ancient Ruins", "security": "null", "emoji": "🏚️",
        "description": "Crumbling stone structures from before Ironhaven was Ironhaven. No guards. No law. This is where people who 'left for the Grand Line' actually end up. Someone has been living here.",
        "connected_to": ["ashwood_forest", "cursed_grove", "shadow_den"],
        "npcs": ["shade"], "buildings": ["ancient_vault"],
        "enemy_ids": ["ruins_sentinel", "cursed_knight"], "pvp": True, "discovery_xp": 150,
    },
    "cursed_grove": {
        "id": "cursed_grove", "name": "Cursed Grove", "security": "null", "emoji": "🌑",
        "description": "A dark section of the forest where the trees have gone black. Animals here move wrong — too fast, too purposeful, glowing faintly at the eyes. The black ore has done something to this place.",
        "connected_to": ["ashwood_forest", "ancient_ruins"],
        "npcs": ["the_watcher"], "buildings": [],
        "enemy_ids": ["corrupted_wolf", "forest_witch"], "pvp": True, "discovery_xp": 150,
    },
    "sea_caves": {
        "id": "sea_caves", "name": "Sea Caves", "security": "null", "emoji": "🌊",
        "description": "Accessible only at low tide through the Cove. The caves go deep into the cliffs and seem to extend underwater. Strange things live in the dark. A Fishman could swim where no one else can.",
        "connected_to": ["fishermans_cove"],
        "npcs": [], "buildings": [],
        "enemy_ids": ["sea_serpent", "corrupted_wolf"], "pvp": True, "discovery_xp": 200,
    },
    "shadow_den": {
        "id": "shadow_den", "name": "Shadow Den", "security": "bumpyard", "emoji": "🕳️",
        "description": "Deep in the Ruins, Mercer's mercenary company has set up a fortified compound. Their boss, Commander Voss, runs operations here. Only accessible by those Arc 2+ who know the way in.",
        "connected_to": ["ancient_ruins"],
        "npcs": [], "buildings": [],
        "enemy_ids": ["shadow_den_guard", "elite_mercenary"], "pvp": True, "discovery_xp": 300,
        "level_requirement": 16,
    },
}

# ---------------------------------------------------------------------------
# BUILDINGS
# ---------------------------------------------------------------------------

BUILDINGS: dict[str, dict] = {
    "training_grounds":  {"id": "training_grounds",  "name": "Training Grounds",        "zone": "town_square",    "npc": "captain_rel",  "type": "training",      "emoji": "🥋",  "description": "A weathered courtyard where Rel pushes anyone willing to be pushed."},
    "adventurers_guild": {"id": "adventurers_guild",  "name": "Adventurer's Guild",      "zone": "town_square",    "npc": "keeper_doss",  "type": "quest",         "emoji": "📋",  "description": "Daily contracts, bounties, leaderboards. Keeper Doss runs it like a business, because it is one."},
    "inn":               {"id": "inn",                "name": "The Rusted Compass Inn",   "zone": "town_square",    "npc": "sunny_mirelle","type": "rest",          "emoji": "🛏️", "description": "The inn smells of woodsmoke and old fish stew. Sunny Mirelle serves both with equal cheer."},
    "mercer_bank":       {"id": "mercer_bank",        "name": "Mercer Bank",              "zone": "town_square",    "npc": "bank_teller",  "type": "bank",          "emoji": "🏦",  "description": "Marble columns and a queue of anxious debtors. The teller smiles like they're trained to."},
    "clinic":            {"id": "clinic",             "name": "Clinic",                   "zone": "town_square",    "npc": "dr_wren",      "type": "heal",          "emoji": "⚕️", "description": "Dr. Wren charges fairly. That makes him unusual in Ironhaven."},
    "council_hall":      {"id": "council_hall",       "name": "Council Hall",             "zone": "town_square",    "npc": None,           "type": "civic",         "emoji": "🏛️", "description": "Imposing bronze doors, always slightly ajar. Inside: bureaucracy in service of Mercer."},
    "general_store":     {"id": "general_store",      "name": "General Store",            "zone": "market_quarter", "npc": "old_tomas",    "type": "shop",          "emoji": "🏪",  "description": "Old Tomás stocks everything you need and nothing you want. He smiles too easily."},
    "card_shop":         {"id": "card_shop",          "name": "The Gilded Draw",          "zone": "market_quarter", "npc": "vex",          "type": "cards",         "emoji": "🃏",  "description": "Strange cards in a stranger shop. Vex asks questions that seem random but aren't."},
    "potion_emporium":   {"id": "potion_emporium",    "name": "Potion Emporium",          "zone": "market_quarter", "npc": "nurse_hana",   "type": "potions",       "emoji": "⚗️", "description": "Precisely labeled, precisely priced. Hana's fury shows in her precision."},
    "equipment_shop":    {"id": "equipment_shop",     "name": "Ironhaven Armory",         "zone": "market_quarter", "npc": "forge_arm",    "type": "equipment",     "emoji": "⚔️", "description": "'Forge-Arm' sells weapons with the enthusiasm of someone who's used them."},
    "tailor":            {"id": "tailor",             "name": "Mira's Threads",           "zone": "market_quarter", "npc": "mira",         "type": "cosmetics",     "emoji": "🧵",  "description": "Cosmetics and bag upgrades. Mira has strong opinions about everything."},
    "auction_house":     {"id": "auction_house",      "name": "Auction House",            "zone": "market_quarter", "npc": None,           "type": "market",        "emoji": "🏷️", "description": "Automated market board. List items, pay your tax, wait."},
    "harbour_office":    {"id": "harbour_office",     "name": "Harbour Master's Office",  "zone": "port_district",  "npc": "maren",        "type": "quest",         "emoji": "⚓",  "description": "All Ironhaven port logistics run through Maren's office. She sees everything that moves through this port."},
    "sailors_tavern":    {"id": "sailors_tavern",     "name": "Sailors' Tavern",          "zone": "port_district",  "npc": "bora",         "type": "social",        "emoji": "🍺",  "description": "Loud, warm, and always busy. Bora remembers everyone's usual."},
    "shipyard":          {"id": "shipyard",           "name": "Shipyard",                 "zone": "port_district",  "npc": "old_boris",    "type": "ships",         "emoji": "⚓",  "description": "Old Boris has been repairing ships since before Mercer arrived. He says it was better then."},
    "barn":              {"id": "barn",               "name": "Farmlands Barn",           "zone": "farmlands",      "npc": None,           "type": "storage",       "emoji": "🏚️", "description": "Communal crop storage. Mercer takes 40% before you ever touch it."},
    "fish_market":       {"id": "fish_market",        "name": "Fish Market",              "zone": "fishermans_cove","npc": None,           "type": "shop",          "emoji": "🐟",  "description": "Sell your catches here. The buyers are independent of Mercer — for now."},
    "grulls_shack":      {"id": "grulls_shack",       "name": "Grull's Shack",            "zone": "fishermans_cove","npc": "old_grull",    "type": "fishing_info",  "emoji": "🎣",  "description": "Old Grull knows where every fish in these waters lives. He'll share — if you've earned it."},
    "ancient_vault":     {"id": "ancient_vault",      "name": "Ancient Vault",            "zone": "ancient_ruins",  "npc": None,           "type": "dungeon_reward","emoji": "🗝️", "description": "A sealed stone chamber. It was opened recently. Something was taken — or left."},
}

# ---------------------------------------------------------------------------
# NPCs
# ---------------------------------------------------------------------------

NPCS: dict[str, dict] = {
    "maren": {
        "id": "maren", "name": "Maren", "role": "Dockmaster",
        "zone_id": "port_district", "building_id": "harbour_office", "emoji": "⚓",
        "persona": (
            "You are Maren, the Dockmaster of Ironhaven. You are in your late 40s, weathered, blunt, "
            "and deeply cynical after years of watching Mercer's corruption go unchallenged. You lost "
            "your ship 'The Cormorant' to Mercer's debt collectors three years ago. You give nothing "
            "away for free but you respect people who are direct with you. You keep your true feelings "
            "about Mercer buried under layers of sarcasm and practicality. As trust builds across "
            "repeated conversations, you reveal more. Your speech is short, clipped, nautical. You "
            "never complain openly — you observe and imply. You do not reveal the full situation "
            "immediately; you test the player first. You know more than you say. "
            "Do not break character. Respond in character as Maren."
        ),
        "opening_lines": [
            "Back again? The port doesn't move any faster because you're watching it.",
            "I'm busy. What do you want.",
            "You've got that look. The one people get right before they ask a question I'd rather not answer.",
            "Cargo doesn't count itself. Make it quick.",
        ],
        "relationship_milestones": {
            5:  "She stops checking her ledger when you walk in.",
            10: "She pours you coffee without asking. It's black and terrible.",
            25: "She tells you The Cormorant's name. 'Used to be mine,' is all she says.",
            50: "She hands you a manifest with a name circled. 'This isn't official. Neither are you.'",
        },
    },
    "old_tomas": {
        "id": "old_tomas", "name": "Old Tomás", "role": "General Store Keeper",
        "zone_id": "market_quarter", "building_id": "general_store", "emoji": "🏪",
        "persona": (
            "You are Old Tomás, keeper of the General Store in Ironhaven. You are in your mid-60s, "
            "gentle, warm, and terrified beneath the warmth. You pay 60% of your profits to Mercer's "
            "'licensing fees' and your son Dario works in the ore mines in the forest as leverage for "
            "a debt that keeps growing. You are warm and chatty about mundane things but grow evasive "
            "if Mercer or the Council comes up. You pretend everything is fine. You slip hints in "
            "sideways — mentioning your son without explaining why, talking about how much you miss "
            "the old days. Your speech is folksy, warm, a little scattered. You sometimes trail off "
            "mid-thought. You change the subject when it gets too close to the truth. "
            "Do not break character. Respond as Old Tomás."
        ),
        "opening_lines": [
            "Ah, welcome, welcome! Mind the floor, I just mopped — or did I? Ha, the memory goes first, they say.",
            "Come in, come in! Anything special you're looking for today?",
            "Tomás's General Store, finest stock in all of — well, Ironhaven. Which is what we have. Ha!",
        ],
        "relationship_milestones": {
            5:  "He gives you a small discount on items. 'Regular customer rate,' he winks.",
            15: "He mentions Dario without prompting. Catches himself. Changes the subject.",
            30: "He shows you a letter he received. 'From my son. He's... working. Out of town.' He folds it quickly.",
        },
    },
    "vex": {
        "id": "vex", "name": "Vex", "role": "Card Shop Proprietor",
        "zone_id": "market_quarter", "building_id": "card_shop", "emoji": "🃏",
        "persona": (
            "You are Vex, proprietor of The Gilded Draw card shop in Ironhaven. You appear to be in "
            "your early 30s, sardonic, always watching, impossible to read. Your card shop is a front "
            "for the underground resistance. You test everyone who enters — asking seemingly random "
            "questions that are actually profiling them for trustworthiness. You speak in card game "
            "metaphors often. You never confirm or deny anything important directly. If someone has "
            "earned significant trust and given you reason, you start dropping hints about the "
            "resistance. Your default mode is mildly disinterested merchant who notices everything. "
            "Your speech is cryptic, wry, economical. You make people feel like they're missing "
            "something. Do not break character. Respond as Vex."
        ),
        "opening_lines": [
            "The cards you need aren't always the cards you want. Look around.",
            "New hand, same game. What are you shopping for.",
            "Most people take twice as long to decide as they think they do. Go ahead.",
            "I've got a rotating stock. Rare. Rarer. And then there's the ones not on display.",
        ],
        "relationship_milestones": {
            5:  "He answers your questions with slightly fewer questions.",
            15: "He shows you a card not in the display case. 'Not for sale. Yet.'",
            30: "He asks you directly: 'If the game was rigged from the start — would you still play?'",
            50: "He slides a note across the counter. One line. An address. A time.",
        },
    },
    "bora": {
        "id": "bora", "name": "Bora", "role": "Barkeep",
        "zone_id": "port_district", "building_id": "sailors_tavern", "emoji": "🍺",
        "persona": (
            "You are Bora, barkeep of the Sailors' Tavern in the Port District of Ironhaven. You are "
            "in your early 50s, perpetually cheerful, apparently never drunk despite being surrounded "
            "by alcohol all day. You collect gossip and information from the drunk Council soldiers "
            "who drink here and pass useful intelligence to the resistance without ever seeming to do "
            "so. Your cheerfulness is completely genuine — you love people and storytelling — but it "
            "also provides perfect cover. You know everyone and everything. You speak in stories — "
            "every point is illustrated with a tale about someone you once knew. You are generous and "
            "remember everyone's usual. Do not break character. Respond as Bora."
        ),
        "opening_lines": [
            "There you are! The usual? Oh wait, this is your — sit down anyway, I'll figure it out.",
            "Ha! You just missed a Council sergeant who had three too many and told me everything about the shipyard watch schedule. Not that I'd remember a thing like that.",
            "Welcome, welcome! What's your pleasure? And your story — everyone who walks through that door has one.",
        ],
        "relationship_milestones": {
            5:  "He remembers your order.",
            15: "He tells you a story about 'someone he used to know' who sounds suspiciously like a resistance fighter.",
            30: "He pours you a drink on the house and leans in. 'You know what the soldiers complain about most when they're drunk? The ore shipments running behind schedule.'",
        },
    },
    "shade": {
        "id": "shade", "name": "Shade", "role": "Mercer's Head Enforcer",
        "zone_id": "ancient_ruins", "building_id": None, "emoji": "🌑",
        "persona": (
            "You are Shade, Head Enforcer for the Mercer Trading Company in Ironhaven. You appear to "
            "be in your early 30s, controlled, economical with words, carrying the weight of a choice "
            "you can't undo. You were a resistance fighter once. Your whole crew was killed in a raid "
            "that you later learned was a setup. You took Mercer's deal because you had nothing left. "
            "You execute your duties precisely but never with cruelty. You are watching this player — "
            "something about them reminds you of who you were. You are not a villain. You are a "
            "person who made a catastrophic compromise and hasn't found a reason to undo it yet. You "
            "keep people at arm's length through coldness and economy of speech. Dark humor surfaces "
            "occasionally. You don't explain yourself unless cornered. "
            "Do not break character. Respond as Shade."
        ),
        "opening_lines": [
            "I was wondering when you'd find your way here.",
            "This part of the ruins is off-limits. You already knew that.",
            "Smart enough to track me. I'll give you that much.",
        ],
        "relationship_milestones": {
            3:  "He doesn't draw his weapon when you approach.",
            10: "He says: 'This place had a different name, before. People came here to meet in secret.' He doesn't explain what that means.",
            25: "He admits: 'I'm going to ask you something and I'd prefer an honest answer. Are you here because someone sent you, or because you decided to be?'",
        },
    },
    "captain_rel": {
        "id": "captain_rel", "name": "Captain Rel", "role": "Training Master",
        "zone_id": "town_square", "building_id": "training_grounds", "emoji": "🥋",
        "persona": (
            "You are Captain Rel, a retired soldier who runs the Training Grounds in Ironhaven. You "
            "are in your mid-60s, permanently upright, with the economy of motion of someone who "
            "spent 35 years in real military service — not the Council's kind. You are secretly one "
            "of the founders of the original Ironhaven resistance, before Mercer came and before you "
            "realized resistance needed to wait for the right moment. You train anyone who comes to "
            "you seriously. You believe in earning things. Your speech is short commands and "
            "occasional parables. You assess everyone who comes through your door. You share your "
            "opinions only when directly asked, and then honestly and precisely. You have no patience "
            "for excuses. Do not break character. Respond as Captain Rel."
        ),
        "opening_lines": [
            "You're here to train or here to watch. Make a choice.",
            "I've seen your type before. Whether that's good or bad depends entirely on you.",
            "Stance. Before anything else — stance.",
        ],
        "relationship_milestones": {
            5:  "He corrects your form without being asked.",
            15: "He shares a story about a battle he fought 20 years ago. He doesn't say which side he was on.",
            30: "He says: 'The Council calls me retired. That's accurate. Doesn't mean I'm finished.'",
        },
    },
    "nurse_hana": {
        "id": "nurse_hana", "name": "Nurse Hana", "role": "Potion Emporium Keeper",
        "zone_id": "market_quarter", "building_id": "potion_emporium", "emoji": "⚗️",
        "persona": (
            "You are Nurse Hana, keeper of the Potion Emporium in Ironhaven. You are in your early "
            "30s, precise, professionally warm, quietly furious. You've treated patients whose "
            "injuries don't match their explanations — workers from the forest ore operation who were "
            "'in accidents', resistors who were 'mugged'. You are expected to document what you're "
            "told and stay quiet. Every patient chips away at your composure. Your anger leaks "
            "through in small ways — pausing too long before answering, precise clinical descriptions "
            "that don't quite fit the official story. You take medicine very seriously. You speak "
            "carefully. You never say what you know directly, but you describe symptoms very "
            "precisely. Do not break character. Respond as Nurse Hana."
        ),
        "opening_lines": [
            "Are you here to buy something or because something is wrong?",
            "Everything is properly labeled. If you have questions about dosage, ask before purchasing.",
            "I keep a very clean shop. It's the one thing I can control.",
        ],
        "relationship_milestones": {
            5:  "She asks about your injuries before selling you healing items.",
            15: "She mentions 'unusual mineral exposure' as a cause of injury, clinical and precise.",
            30: "She hands you a potion with a note folded under the label. 'Read this when you're somewhere quiet.'",
        },
    },
    "old_grull": {
        "id": "old_grull", "name": "Old Grull", "role": "Fisherman",
        "zone_id": "fishermans_cove", "building_id": "grulls_shack", "emoji": "🎣",
        "persona": (
            "You are Old Grull, a veteran fisherman at Fisherman's Cove in Ironhaven. You are "
            "ancient — nobody knows exactly how old. You've fished these waters your entire life and "
            "you know where every fish lives. You are terse, deeply practical, and have no patience "
            "for people who don't know how to fish. You will teach anyone who is serious. You speak "
            "in short sentences about practical things. You don't care about Mercer or the Council — "
            "the sea has been here longer than any of them. You have exactly one strong opinion: the "
            "ore mining in the forest has changed the fish near the sea caves, and something is wrong "
            "with the water there. You don't analyze this. You just state it as fact. "
            "Do not break character."
        ),
        "opening_lines": [
            "Tide's going out. Best time.",
            "You fish?",
            "Most people who come here are looking for something. Usually fish. Sometimes not.",
        ],
        "relationship_milestones": {
            3:  "He shows you a fishing spot not visible from the dock.",
            10: "He gives you better bait without charging for it.",
        },
    },
    "the_watcher": {
        "id": "the_watcher", "name": "The Watcher", "role": "Unknown",
        "zone_id": "cursed_grove", "building_id": None, "emoji": "👁️",
        "persona": (
            "You are The Watcher, a mysterious figure in the Cursed Grove. You have no name you'll "
            "share, no history you'll confirm. You seem to know things about the player that you "
            "shouldn't. You speak in riddles that turn out, on reflection, to not be riddles at all "
            "— just information presented sideways. You are not a threat. You are an observer. You "
            "sell things occasionally, for prices that aren't in Zet. You are deeply strange but not "
            "malevolent. Do not break character."
        ),
        "opening_lines": [
            "You found this place. Most don't.",
            "I've been watching the forest change. It changes quickly now.",
            "You want something. They always do.",
        ],
        "relationship_milestones": {},
    },
    "old_boris": {
        "id": "old_boris", "name": "Old Boris", "role": "Shipwright",
        "zone_id": "port_district", "building_id": "shipyard", "emoji": "⚓",
        "persona": (
            "You are Old Boris, the shipwright at Ironhaven's Shipyard. You are in your late 60s, "
            "massive-handed, slow-moving, and deeply nostalgic. You've been repairing ships since "
            "before Mercer arrived. You remember when the shipyard built ships — not just patched "
            "them. Now you patch Mercer's fleet for Mercer's docking fees and try not to think "
            "about what the ships carry. You speak slowly, in technical maritime terms, always "
            "getting to the point. You have one hope: a small sloop you've been secretly repairing "
            "in the back berth. You don't talk about it unless someone earns your trust."
        ),
        "opening_lines": [
            "Busy. What do you need.",
            "If you're not here about the caulking order, make it quick.",
            "This place used to build ships. Now we just keep old ones running.",
        ],
        "relationship_milestones": {
            5:  "He hands you coffee without being asked. It's been sitting on the burner too long.",
            10: "He mentions 'a project in the back' without explaining what it is.",
            25: "He takes you to see it — a small sloop, nearly complete. 'Just maintenance,' he says, unconvincingly.",
        },
    },
}

# ---------------------------------------------------------------------------
# ENEMIES
# ---------------------------------------------------------------------------

ENEMIES: dict[str, dict] = {
    "port_pickpocket": {
        "id": "port_pickpocket", "name": "Port Pickpocket", "emoji": "🤞",
        "zone_tiers": ["medium"], "hp": 20, "atk": 8, "defense": 3, "behavior": "evasive",
        "xp_reward": 12, "zet_range": (5, 15),
        "moves": [
            {"name": "Quick Jab",    "type": "damage",  "value": 8,  "weight": 50},
            {"name": "Pick Pocket",  "type": "steal",   "value": 10, "weight": 30},
            {"name": "Dodge",        "type": "special", "special": "evade", "weight": 20},
        ],
        "drop_table": [
            {"type": "card", "rarity": "common", "chance": 0.7},
            {"type": "item", "item_id": "health_potion", "chance": 0.2},
        ],
        "description": "A lean figure in the wrong part of the port, watching for unwatched pockets.",
    },
    "drunken_sailor": {
        "id": "drunken_sailor", "name": "Drunken Sailor", "emoji": "🍺",
        "zone_tiers": ["medium"], "hp": 28, "atk": 10, "defense": 4, "behavior": "erratic",
        "xp_reward": 14, "zet_range": (8, 20),
        "moves": [
            {"name": "Wild Swing", "type": "damage", "value": 10, "weight": 40},
            {"name": "Stumble",    "type": "skip",   "weight": 30},
            {"name": "Headbutt",   "type": "damage", "value": 14, "weight": 20},
            {"name": "Shout",      "type": "status", "status": {"name": "intimidate", "turns": 1, "value": 2}, "weight": 10},
        ],
        "drop_table": [
            {"type": "card", "rarity": "common", "chance": 0.8},
            {"type": "zet", "chance": 1.0},
        ],
        "description": "Started his evening angry and his night somewhere worse.",
    },
    "bandit_scout": {
        "id": "bandit_scout", "name": "Bandit Scout", "emoji": "🔍",
        "zone_tiers": ["medium", "low"], "hp": 25, "atk": 12, "defense": 5, "behavior": "aggressive",
        "xp_reward": 16, "zet_range": (5, 15),
        "moves": [
            {"name": "Slash",       "type": "damage", "value": 12, "weight": 70},
            {"name": "Call Backup", "type": "status", "status": {"name": "reinforce", "turns": 0, "value": 0}, "weight": 30},
        ],
        "drop_table": [
            {"type": "card", "rarity": "common", "chance": 0.8},
            {"type": "card", "rarity": "rare",   "chance": 0.15},
        ],
        "description": "Lean and watchful. You got the feeling they were watching the roads before you were on them.",
    },
    "bandit_warrior": {
        "id": "bandit_warrior", "name": "Bandit Warrior", "emoji": "🗡️",
        "zone_tiers": ["low"], "hp": 45, "atk": 18, "defense": 8, "behavior": "aggressive",
        "xp_reward": 30, "zet_range": (15, 40),
        "moves": [
            {"name": "Heavy Slash",  "type": "damage", "value": 18, "weight": 50},
            {"name": "Power Strike", "type": "damage", "value": 24, "weight": 30},
            {"name": "Guard Break",  "type": "special", "special": "pierce_shield", "value": 8, "weight": 20},
        ],
        "drop_table": [
            {"type": "card", "rarity": "common", "chance": 0.6},
            {"type": "card", "rarity": "rare",   "chance": 0.35},
            {"type": "item", "item_id": "health_potion", "chance": 0.25},
        ],
        "description": "Experienced fighter, misapplied. Their form is too clean for a street thug.",
    },
    "bandit_archer": {
        "id": "bandit_archer", "name": "Bandit Archer", "emoji": "🏹",
        "zone_tiers": ["low"], "hp": 35, "atk": 20, "defense": 4, "behavior": "ranged",
        "xp_reward": 28, "zet_range": (12, 35),
        "moves": [
            {"name": "Arrow Shot",     "type": "damage",        "value": 15, "weight": 50},
            {"name": "Bleeding Arrow", "type": "damage_status", "value": 10, "status": {"name": "bleed", "turns": 2, "value": 4}, "weight": 35},
            {"name": "Retreat",        "type": "special",       "special": "evade", "weight": 15},
        ],
        "drop_table": [
            {"type": "card", "rarity": "rare",   "chance": 0.4},
            {"type": "item", "item_id": "antidote", "chance": 0.2},
        ],
        "description": "Keeps distance, stays quiet. The arrow that hits you is the first warning you get.",
    },
    "dire_wolf": {
        "id": "dire_wolf", "name": "Dire Wolf", "emoji": "🐺",
        "zone_tiers": ["low"], "hp": 55, "atk": 22, "defense": 6, "behavior": "pack_hunter",
        "xp_reward": 35, "zet_range": (0, 0),
        "moves": [
            {"name": "Savage Bite",  "type": "damage",        "value": 22, "weight": 60},
            {"name": "Feral Pounce", "type": "damage_status", "value": 16, "status": {"name": "bleed", "turns": 3, "value": 3}, "weight": 40},
        ],
        "drop_table": [
            {"type": "card", "rarity": "rare",   "chance": 0.3},
            {"type": "item", "item_id": "wolf_fang", "chance": 0.6},
        ],
        "description": "Eyes like cold embers. It moves like it knows exactly what you'll do next.",
    },
    "forest_witch": {
        "id": "forest_witch", "name": "Forest Witch", "emoji": "🧙",
        "zone_tiers": ["low"], "hp": 40, "atk": 15, "defense": 7, "behavior": "evasive_caster",
        "xp_reward": 32, "zet_range": (10, 30),
        "moves": [
            {"name": "Dark Hex", "type": "damage_status", "value": 10, "status": {"name": "curse",  "turns": 3, "value": 0}, "weight": 50},
            {"name": "Blight",   "type": "status",        "status": {"name": "poison", "turns": 3, "value": 5}, "weight": 30},
            {"name": "Flee",     "type": "flee", "weight": 20},
        ],
        "drop_table": [
            {"type": "card", "rarity": "rare", "chance": 0.45},
            {"type": "card", "rarity": "epic", "chance": 0.1},
        ],
        "description": "She watches you the way a crow watches a wound. With patience.",
    },
    "mercer_mercenary": {
        "id": "mercer_mercenary", "name": "Mercer Mercenary", "emoji": "⚔️",
        "zone_tiers": ["low", "null"], "hp": 70, "atk": 32, "defense": 18, "behavior": "tactical",
        "xp_reward": 50, "zet_range": (30, 70),
        "moves": [
            {"name": "Iron Swing",        "type": "damage",     "value": 28, "weight": 50},
            {"name": "Shield Up",         "type": "self_shield","value": 15, "weight": 30},
            {"name": "Mercenary Strike",  "type": "damage",     "value": 35, "weight": 20},
        ],
        "drop_table": [
            {"type": "card", "rarity": "rare", "chance": 0.5},
            {"type": "card", "rarity": "epic", "chance": 0.15},
        ],
        "description": "Professional. Well-equipped. Working for someone with money. The worst kind.",
    },
    "corrupted_wolf": {
        "id": "corrupted_wolf", "name": "Corrupted Wolf", "emoji": "👾",
        "zone_tiers": ["null"], "hp": 75, "atk": 28, "defense": 10, "behavior": "corrupted",
        "xp_reward": 60, "zet_range": (0, 0),
        "moves": [
            {"name": "Void Bite",       "type": "magic_damage", "value": 22, "weight": 50},
            {"name": "Corruption Aura", "type": "status", "status": {"name": "curse", "turns": 2, "value": 0}, "weight": 35},
            {"name": "Phase Lunge",     "type": "damage",        "value": 30, "weight": 15},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic", "chance": 0.2},
            {"type": "item", "item_id": "black_ore_fragment", "chance": 0.5},
        ],
        "description": "It was a wolf once. The ore changed something in it. Now its eyes glow and its wounds don't bleed right.",
    },
    "ruins_sentinel": {
        "id": "ruins_sentinel", "name": "Ruins Sentinel", "emoji": "🗿",
        "zone_tiers": ["null"], "hp": 90, "atk": 30, "defense": 15, "behavior": "regenerating",
        "xp_reward": 65, "zet_range": (40, 80),
        "moves": [
            {"name": "Ancient Blow", "type": "damage",    "value": 30, "weight": 60},
            {"name": "Regenerate",   "type": "self_heal", "value": 5,  "weight": 40},
        ],
        "drop_table": [
            {"type": "card", "rarity": "rare", "chance": 0.6},
            {"type": "card", "rarity": "epic", "chance": 0.2},
        ],
        "description": "Stone. Moss. Moving. Ancient guardian of something that no longer needs guarding.",
    },
    "cursed_knight": {
        "id": "cursed_knight", "name": "Cursed Knight", "emoji": "☠️",
        "zone_tiers": ["null"], "hp": 85, "atk": 35, "defense": 20, "behavior": "counter",
        "xp_reward": 70, "zet_range": (50, 100),
        "moves": [
            {"name": "Dark Slash",    "type": "damage",  "value": 30, "weight": 50},
            {"name": "Counter Stance","type": "special", "special": "counter_on_defense", "value": 20, "weight": 30},
            {"name": "Death Blow",    "type": "damage",  "value": 45, "weight": 20},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic",   "chance": 0.3},
            {"type": "item", "item_id": "cursed_sigil", "chance": 0.4},
        ],
        "description": "Someone's punishment, still running.",
    },
    "sea_serpent": {
        "id": "sea_serpent", "name": "Sea Serpent", "emoji": "🐍",
        "zone_tiers": ["null"], "hp": 120, "atk": 40, "defense": 12, "behavior": "relentless",
        "xp_reward": 90, "zet_range": (0, 0),
        "moves": [
            {"name": "Crushing Coil",   "type": "damage",        "value": 35, "weight": 40},
            {"name": "Venomous Strike", "type": "damage_status", "value": 25, "status": {"name": "poison", "turns": 4, "value": 6}, "weight": 35},
            {"name": "Tail Slam",       "type": "damage",        "value": 40, "weight": 25},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic",   "chance": 0.4},
            {"type": "item", "item_id": "serpent_scale", "chance": 0.5},
        ],
        "description": "The sea has worse things in it than weather.",
    },
    "shadow_den_guard": {
        "id": "shadow_den_guard", "name": "Shadow Den Guard", "emoji": "💀",
        "zone_tiers": ["bumpyard"], "hp": 100, "atk": 38, "defense": 20, "behavior": "elite",
        "xp_reward": 80, "zet_range": (60, 120),
        "moves": [
            {"name": "Precision Strike", "type": "damage",  "value": 38, "weight": 60},
            {"name": "Alarm Call",       "type": "special", "special": "call_elite", "weight": 20},
            {"name": "Heavy Blow",       "type": "damage",  "value": 50, "weight": 20},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic", "chance": 0.4},
        ],
        "description": "Mercenary. Professional. Expensive. Mercer doesn't hire cheap.",
    },
    "elite_mercenary": {
        "id": "elite_mercenary", "name": "Elite Mercenary", "emoji": "⚔️",
        "zone_tiers": ["bumpyard"], "hp": 130, "atk": 45, "defense": 25, "behavior": "elite",
        "xp_reward": 100, "zet_range": (80, 150),
        "moves": [
            {"name": "Precision Strike",  "type": "damage",      "value": 45, "weight": 50},
            {"name": "Defensive Stance",  "type": "self_shield", "value": 20, "weight": 25},
            {"name": "Execute",           "type": "damage",      "value": 60, "weight": 15},
            {"name": "Mercenary Tactics", "type": "special",     "special": "pierce_shield", "value": 30, "weight": 10},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic",      "chance": 0.5},
            {"type": "card", "rarity": "legendary", "chance": 0.05},
            {"type": "item", "item_id": "mercenary_badge", "chance": 0.6},
        ],
        "description": "Mercer's best. Not a soldier — a specialist. Trained, expensive, and very aware of how much they cost.",
    },
    "shade_boss": {
        "id": "shade_boss", "name": "Shade", "emoji": "🌑",
        "zone_tiers": ["null"], "hp": 180, "atk": 40, "defense": 15, "behavior": "boss_arc1",
        "xp_reward": 300, "zet_range": (200, 200),
        "moves": [
            {"name": "Enforcer's Strike", "type": "damage", "value": 30, "weight": 50},
            {"name": "Precision Slash",   "type": "damage", "value": 38, "weight": 30},
            {"name": "Restrain", "type": "status", "status": {"name": "stun", "turns": 1, "value": 0}, "weight": 20},
        ],
        "drop_table": [
            {"type": "card", "rarity": "legendary", "chance": 1.0},
            {"type": "item", "item_id": "shades_coat", "chance": 1.0},
        ],
        "description": "He fights like someone who knows exactly what he's doing and hates that he has to do it.",
        "is_boss": True,
    },
    # ── Mini-bosses — one per dangerous zone, 6-hour global respawn ──────────
    "miniboss_port_enforcer": {
        "id": "miniboss_port_enforcer", "name": "The Dockmaster's Enforcer", "emoji": "⚓",
        "zone_tiers": ["medium"], "hp": 85, "atk": 22, "defense": 10, "behavior": "miniboss_thief",
        "xp_reward": 120, "zet_range": (80, 120), "is_miniboss": True, "zone_id": "port_district",
        "moves": [
            {"name": "Dock Baton",  "type": "damage", "value": 18, "weight": 40},
            {"name": "Extort",      "type": "steal",  "value": 25, "weight": 35},
            {"name": "Shakedown",   "type": "damage", "value": 24, "weight": 25},
        ],
        "drop_table": [
            {"type": "card", "rarity": "rare",              "chance": 1.0},
            {"type": "item", "item_id": "dock_authority_badge", "chance": 1.0},
            {"type": "zet",  "amount": 100,                 "chance": 1.0},
        ],
        "description": "The Dockmaster's personal muscle. He's been roughing up independent traders all week. The badge on his chest isn't Council — it's Mercer's.",
    },
    "miniboss_night_inspector": {
        "id": "miniboss_night_inspector", "name": "The Night Inspector", "emoji": "🔦",
        "zone_tiers": ["medium"], "hp": 90, "atk": 28, "defense": 8, "behavior": "miniboss_pierce",
        "xp_reward": 130, "zet_range": (80, 120), "is_miniboss": True, "zone_id": "harbour_docks",
        "moves": [
            {"name": "Authority Strike", "type": "damage",  "value": 20, "weight": 40},
            {"name": "Armour Pierce",    "type": "special", "special": "pierce_shield", "value": 22, "weight": 35},
            {"name": "Inspect",          "type": "status",  "status": {"name": "slow", "turns": 2, "value": 2}, "weight": 25},
        ],
        "drop_table": [
            {"type": "card", "rarity": "rare",              "chance": 1.0},
            {"type": "item", "item_id": "night_manifest_copy", "chance": 1.0},
            {"type": "zet",  "amount": 100,                 "chance": 1.0},
        ],
        "description": "Walks the docks after midnight with a lamp and a ledger. The lamp is to see. The ledger is to know what to ask for.",
    },
    "miniboss_captain_rusk": {
        "id": "miniboss_captain_rusk", "name": "Bandit Captain Rusk", "emoji": "🗡️",
        "zone_tiers": ["medium"], "hp": 100, "atk": 26, "defense": 12, "behavior": "miniboss_aoe",
        "xp_reward": 140, "zet_range": (90, 130), "is_miniboss": True, "zone_id": "farmlands",
        "moves": [
            {"name": "War Sweep", "type": "damage",     "value": 20, "weight": 35},
            {"name": "Scatter",   "type": "special",    "special": "discard_card", "value": 1, "weight": 35},
            {"name": "Rally",     "type": "self_shield","value": 12, "weight": 30},
        ],
        "drop_table": [
            {"type": "card", "rarity": "rare",              "chance": 1.0},
            {"type": "item", "item_id": "bandit_captain_seal", "chance": 1.0},
            {"type": "zet",  "amount": 110,                 "chance": 1.0},
        ],
        "description": "The bandits in the Farmlands don't just happen. Rusk organises them. He has a contact in the city — someone who tells him when the collector patrols thin out.",
    },
    "miniboss_sea_witch": {
        "id": "miniboss_sea_witch", "name": "The Sea Witch", "emoji": "🌊",
        "zone_tiers": ["low"], "hp": 95, "atk": 24, "defense": 9, "behavior": "miniboss_poison",
        "xp_reward": 150, "zet_range": (90, 140), "is_miniboss": True, "zone_id": "fishermans_cove",
        "moves": [
            {"name": "Tidal Hex",   "type": "damage_status", "value": 14, "status": {"name": "poison", "turns": 3, "value": 4}, "weight": 40},
            {"name": "Brine Curse", "type": "status",        "status": {"name": "poison", "turns": 2, "value": 6}, "weight": 35},
            {"name": "Undertow",    "type": "damage",        "value": 22, "weight": 25},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic",           "chance": 0.5},
            {"type": "card", "rarity": "rare",           "chance": 0.5},
            {"type": "item", "item_id": "witchbone_talisman", "chance": 1.0},
            {"type": "zet",  "amount": 120,              "chance": 1.0},
        ],
        "description": "The cove fishermen leave food at the tide line for her. Not as worship — as insurance. Old Grull won't explain why.",
    },
    "miniboss_the_poacher": {
        "id": "miniboss_the_poacher", "name": "The Poacher", "emoji": "🎯",
        "zone_tiers": ["low"], "hp": 110, "atk": 30, "defense": 8, "behavior": "miniboss_bleed",
        "xp_reward": 160, "zet_range": (100, 150), "is_miniboss": True, "zone_id": "ashwood_forest",
        "moves": [
            {"name": "Pinning Shot",    "type": "damage_status", "value": 18, "status": {"name": "bleed", "turns": 3, "value": 5}, "weight": 40},
            {"name": "Serrated Arrow",  "type": "damage",        "value": 26, "weight": 35},
            {"name": "Cut Loose",       "type": "special",       "special": "prevent_flee", "weight": 25},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic",        "chance": 0.5},
            {"type": "card", "rarity": "rare",        "chance": 0.5},
            {"type": "item", "item_id": "poachers_kit",   "chance": 1.0},
            {"type": "zet",  "amount": 130,           "chance": 1.0},
        ],
        "description": "Works the conservation zone with Mercer's tacit permission. Nobody official has complained. Nobody unofficial has survived complaining.",
    },
    "miniboss_transport_guard": {
        "id": "miniboss_transport_guard", "name": "Mercer's Transport Guard", "emoji": "🛡️",
        "zone_tiers": ["low"], "hp": 115, "atk": 32, "defense": 16, "behavior": "miniboss_counter",
        "xp_reward": 170, "zet_range": (110, 160), "is_miniboss": True, "zone_id": "smugglers_trail",
        "moves": [
            {"name": "Guard Strike",   "type": "damage",  "value": 28, "weight": 40},
            {"name": "Shield Counter", "type": "special", "special": "counter_on_defense", "value": 18, "weight": 35},
            {"name": "Suppress",       "type": "status",  "status": {"name": "stun", "turns": 1, "value": 0}, "weight": 25},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic",              "chance": 0.5},
            {"type": "card", "rarity": "rare",              "chance": 0.5},
            {"type": "item", "item_id": "mercenary_contract","chance": 1.0},
            {"type": "zet",  "amount": 140,                 "chance": 1.0},
        ],
        "description": "Specifically assigned to the trail. Not a random patrol. Someone made a decision to put him here permanently.",
    },
    "miniboss_grove_warden": {
        "id": "miniboss_grove_warden", "name": "The Grove Warden", "emoji": "🌑",
        "zone_tiers": ["null"], "hp": 130, "atk": 34, "defense": 14, "behavior": "miniboss_corruption",
        "xp_reward": 200, "zet_range": (130, 180), "is_miniboss": True, "zone_id": "cursed_grove",
        "moves": [
            {"name": "Corruption Pulse", "type": "status",        "status": {"name": "curse", "turns": 3, "value": 0}, "weight": 35},
            {"name": "Void Slam",        "type": "magic_damage",  "value": 28, "weight": 35},
            {"name": "Warden's Grasp",   "type": "damage_status", "value": 20, "status": {"name": "slow", "turns": 2, "value": 3}, "weight": 30},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic",       "chance": 0.75},
            {"type": "card", "rarity": "legendary",  "chance": 0.1},
            {"type": "item", "item_id": "warden_stone",  "chance": 1.0},
            {"type": "zet",  "amount": 150,          "chance": 1.0},
        ],
        "description": "The grove made this. Or the ore did. Hard to tell where the forest ends and the corruption begins anymore.",
    },
    "miniboss_vault_keeper": {
        "id": "miniboss_vault_keeper", "name": "The Vault Keeper", "emoji": "🏛️",
        "zone_tiers": ["null"], "hp": 150, "atk": 36, "defense": 20, "behavior": "miniboss_regen",
        "xp_reward": 220, "zet_range": (150, 200), "is_miniboss": True, "zone_id": "ancient_ruins",
        "moves": [
            {"name": "Ancient Blow", "type": "damage",    "value": 32, "weight": 40},
            {"name": "Restore",      "type": "self_heal", "value": 8,  "weight": 35},
            {"name": "Stone Bind",   "type": "status",    "status": {"name": "stun", "turns": 1, "value": 0}, "weight": 25},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic",              "chance": 0.75},
            {"type": "card", "rarity": "legendary",         "chance": 0.15},
            {"type": "item", "item_id": "ancient_key_fragment","chance": 1.0},
            {"type": "zet",  "amount": 175,                 "chance": 1.0},
        ],
        "description": "Older than the ruins. Possibly older than Ironhaven itself. It was guarding something before Mercer arrived. It still is.",
    },
    "miniboss_cave_titan": {
        "id": "miniboss_cave_titan", "name": "The Cave Titan", "emoji": "💎",
        "zone_tiers": ["null"], "hp": 180, "atk": 38, "defense": 16, "behavior": "miniboss_multihit",
        "xp_reward": 240, "zet_range": (160, 220), "is_miniboss": True, "zone_id": "sea_caves",
        "moves": [
            {"name": "Triple Slam", "type": "damage", "value": 14, "hits": 3, "weight": 40},
            {"name": "Cave Crush",  "type": "damage", "value": 40, "weight": 35},
            {"name": "Tremor",      "type": "status", "status": {"name": "slow", "turns": 2, "value": 4}, "weight": 25},
        ],
        "drop_table": [
            {"type": "card", "rarity": "epic",           "chance": 0.8},
            {"type": "card", "rarity": "legendary",      "chance": 0.2},
            {"type": "item", "item_id": "titan_bone_shard","chance": 1.0},
            {"type": "zet",  "amount": 200,              "chance": 1.0},
        ],
        "description": "The sea caves go deeper than the maps show. The Titan guards the deepest part. Nobody has ever found out what's down there.",
    },
    "miniboss_commander_voss": {
        "id": "miniboss_commander_voss", "name": "Commander Voss", "emoji": "💀",
        "zone_tiers": ["bumpyard"], "hp": 220, "atk": 44, "defense": 22, "behavior": "miniboss_elite",
        "xp_reward": 300, "zet_range": (200, 280), "is_miniboss": True, "zone_id": "shadow_den",
        "moves": [
            {"name": "Command Strike",  "type": "damage",      "value": 40, "weight": 35},
            {"name": "Deploy Guard",    "type": "special",     "special": "summon_guard", "weight": 30},
            {"name": "Execute",         "type": "damage",      "value": 55, "weight": 20},
            {"name": "Tactical Shield", "type": "self_shield", "value": 20, "weight": 15},
        ],
        "drop_table": [
            {"type": "card", "rarity": "legendary",    "chance": 1.0},
            {"type": "item", "item_id": "voss_insignia","chance": 1.0},
            {"type": "zet",  "amount": 250,            "chance": 1.0},
        ],
        "description": "Mercer's military commander. Ran three proxy wars before Ironhaven. The Shadow Den is his retirement. He doesn't seem to be enjoying it.",
        "is_boss": True,
    },
}

# ---------------------------------------------------------------------------
# MINI_BOSSES — zone_id → enemy_id  (for respawn system)
# One per dangerous zone, 6-hour global timer.
# ---------------------------------------------------------------------------

MINI_BOSSES: dict[str, str] = {
    "port_district":   "miniboss_port_enforcer",
    "harbour_docks":   "miniboss_night_inspector",
    "farmlands":       "miniboss_captain_rusk",
    "fishermans_cove": "miniboss_sea_witch",
    "ashwood_forest":  "miniboss_the_poacher",
    "smugglers_trail": "miniboss_transport_guard",
    "cursed_grove":    "miniboss_grove_warden",
    "ancient_ruins":   "miniboss_vault_keeper",
    "sea_caves":       "miniboss_cave_titan",
    "shadow_den":      "miniboss_commander_voss",
}

# ---------------------------------------------------------------------------
# ITEMS
# ---------------------------------------------------------------------------

ITEMS: dict[str, dict] = {
    # ── Original items ───────────────────────────────────────────────────────
    "health_potion": {
        "id": "health_potion", "name": "Health Potion", "emoji": "🧪", "type": "consumable",
        "description": "Restores 25 HP.", "effect": {"type": "heal", "value": 25},
        "price": 50, "stackable": True, "usable_in_battle": True,
    },
    "strong_potion": {
        "id": "strong_potion", "name": "Strong Potion", "emoji": "💉", "type": "consumable",
        "description": "Restores 60 HP.", "effect": {"type": "heal", "value": 60},
        "price": 120, "stackable": True, "usable_in_battle": True,
    },
    "antidote": {
        "id": "antidote", "name": "Antidote", "emoji": "🩺", "type": "consumable",
        "description": "Cures Poison and Bleed.", "effect": {"type": "cleanse", "statuses": ["poison", "bleed"]},
        "price": 35, "stackable": True, "usable_in_battle": True,
    },
    "smelling_salts": {
        "id": "smelling_salts", "name": "Smelling Salts", "emoji": "💨", "type": "consumable",
        "description": "Revive from 0 HP with 25% health.", "effect": {"type": "revive", "hp_percent": 0.25},
        "price": 200, "stackable": True, "usable_in_battle": True,
    },
    "fishing_rod": {
        "id": "fishing_rod", "name": "Fishing Rod", "emoji": "🎣", "type": "tool",
        "slot": "fishing_rod", "description": "Required for fishing.", "effect": None,
        "price": 200, "stackable": False, "usable_in_battle": False,
    },
    "bait": {
        "id": "bait", "name": "Bait", "emoji": "🪱", "type": "consumable",
        "description": "Required per fishing attempt.", "effect": None,
        "price": 10, "stackable": True, "usable_in_battle": False,
    },
    "seeds_common": {
        "id": "seeds_common", "name": "Common Seeds", "emoji": "🌱", "type": "material",
        "description": "Plant in farmland plots to grow crops.", "effect": None,
        "price": 20, "stackable": True, "usable_in_battle": False,
    },
    "sword_iron": {
        "id": "sword_iron", "name": "Iron Sword", "emoji": "⚔️", "type": "equipment", "slot": "weapon",
        "description": "+5 STR.", "effect": {"type": "stat_boost", "stat": "str", "value": 5},
        "price": 300, "stackable": False, "usable_in_battle": False,
    },
    "armor_leather": {
        "id": "armor_leather", "name": "Leather Armor", "emoji": "🧥", "type": "equipment", "slot": "armor",
        "description": "+5 DEF.", "effect": {"type": "stat_boost", "stat": "def", "value": 5},
        "price": 280, "stackable": False, "usable_in_battle": False,
    },
    "wolf_fang": {
        "id": "wolf_fang", "name": "Wolf Fang", "emoji": "🦷", "type": "material",
        "description": "Crafting material dropped by dire wolves.", "effect": None,
        "price": 45, "stackable": True, "usable_in_battle": False,
    },
    "black_ore_fragment": {
        "id": "black_ore_fragment", "name": "Black Ore Fragment", "emoji": "🪨", "type": "key_item",
        "description": "Strange dark ore. Warm to the touch. Someone would pay dearly for this.", "effect": None,
        "price": 0, "sell_price": 60, "stackable": True, "usable_in_battle": False,
    },
    "serpent_scale": {
        "id": "serpent_scale", "name": "Serpent Scale", "emoji": "🐍", "type": "material",
        "description": "Tough scale from a sea serpent. Valuable crafting material.", "effect": None,
        "price": 150, "stackable": True, "usable_in_battle": False,
    },
    "shades_coat": {
        "id": "shades_coat", "name": "Shade's Coat", "emoji": "🌑", "type": "cosmetic",
        "description": "A dark coat that moves like shadow. Unique cosmetic. Arc 1 reward.", "effect": None,
        "price": 0, "stackable": False, "usable_in_battle": False,
    },
    "cursed_sigil": {
        "id": "cursed_sigil", "name": "Cursed Sigil", "emoji": "🔮", "type": "material",
        "description": "An ancient mark. Something about it makes your eyes water.", "effect": None,
        "price": 80, "stackable": True, "usable_in_battle": False,
    },
    # ── Walk finds — Town Square / Market Quarter ────────────────────────────
    "copper_coin":      {"id": "copper_coin",      "name": "Copper Coin",      "emoji": "🪙",  "type": "currency",  "description": "A worn copper coin. Worth a few Ƶ.",                                                          "effect": None, "sell_price": 5,  "stackable": True,  "usable_in_battle": False},
    "council_pamphlet": {"id": "council_pamphlet", "name": "Council Pamphlet", "emoji": "📄",  "type": "lore",      "description": "Official price schedules from the Council. Worthless, but tells you what Mercer wants you to think.", "effect": None, "sell_price": 1,  "stackable": True,  "usable_in_battle": False},
    "guild_notice":     {"id": "guild_notice",     "name": "Guild Notice",     "emoji": "📋",  "type": "lore",      "description": "A torn contract notice from the Guild board. Someone ripped it down.",                         "effect": None, "sell_price": 1,  "stackable": True,  "usable_in_battle": False},
    "bruised_herb":     {"id": "bruised_herb",     "name": "Bruised Herb",     "emoji": "🌿",  "type": "crafting",  "description": "Slightly damaged medicinal herbs. Still usable if you know what you're doing.",                "effect": None, "sell_price": 8,  "stackable": True,  "usable_in_battle": False},
    "bread_roll":       {"id": "bread_roll",       "name": "Bread Roll",       "emoji": "🍞",  "type": "consumable","description": "A wrapped roll from Tomás's shop. Restores 5 HP.",                                              "effect": {"type": "heal", "value": 5}, "sell_price": 10, "stackable": True, "usable_in_battle": True},
    "playing_card":     {"id": "playing_card",     "name": "Playing Card",     "emoji": "🃏",  "type": "lore",      "description": "A card near the Gilded Draw. Not from any deck you recognise.",                              "effect": None, "sell_price": 15, "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Port / Docks ────────────────────────────────────────────
    "rope_scrap":       {"id": "rope_scrap",       "name": "Rope Scrap",       "emoji": "🪢",  "type": "material",  "description": "Good rope, cut end still clean. Useful for various tasks.",                                   "effect": None, "sell_price": 12, "stackable": True,  "usable_in_battle": False},
    "ship_token":       {"id": "ship_token",       "name": "Ship Token",       "emoji": "⚓",  "type": "key_item",  "description": "A brass dock entry token. Unmarked. Not from any registered vessel.",                         "effect": None, "sell_price": 25, "stackable": True,  "usable_in_battle": False},
    "damp_letter":      {"id": "damp_letter",      "name": "Damp Letter",      "emoji": "📨",  "type": "lore",      "description": "Water-damaged. Only two words legible: 'don't come'.",                                        "effect": None, "sell_price": 1,  "stackable": True,  "usable_in_battle": False},
    "cargo_tag":        {"id": "cargo_tag",        "name": "Cargo Tag",        "emoji": "🏷️", "type": "key_item",  "description": "The destination code doesn't match any registered port.",                                    "effect": None, "sell_price": 20, "stackable": True,  "usable_in_battle": False},
    "iron_bolt":        {"id": "iron_bolt",        "name": "Iron Bolt",        "emoji": "🔩",  "type": "material",  "description": "A heavy iron bolt, freshly machined. Too thick for wood — industrial grade.",                  "effect": None, "sell_price": 15, "stackable": True,  "usable_in_battle": False},
    "dock_receipt":     {"id": "dock_receipt",     "name": "Dock Receipt",     "emoji": "🧾",  "type": "key_item",  "description": "Partially burned. Cargo listed as 'raw industrial material.' The weight is circled twice.",     "effect": None, "sell_price": 5,  "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Farmlands ───────────────────────────────────────────────
    "wild_herbs":       {"id": "wild_herbs",       "name": "Wild Herbs",       "emoji": "🌾",  "type": "crafting",  "description": "Medicinal herbs at the field edge. Hana would find these useful.",                             "effect": None, "sell_price": 18, "stackable": True,  "usable_in_battle": False},
    "grain_sack":       {"id": "grain_sack",       "name": "Grain Sack",       "emoji": "🌾",  "type": "material",  "description": "A small sack of grain left by the road. Someone's portion, set aside.",                       "effect": None, "sell_price": 20, "stackable": True,  "usable_in_battle": False},
    "fence_nail":       {"id": "fence_nail",       "name": "Fence Nails",      "emoji": "🔨",  "type": "material",  "description": "Iron nails scattered near a broken fence.",                                                  "effect": None, "sell_price": 8,  "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Ashwood Forest ──────────────────────────────────────────
    "wolfsbane":        {"id": "wolfsbane",        "name": "Wolfsbane",        "emoji": "🌑",  "type": "crafting",  "description": "Rare medicinal herb. Hana specifically requests this. Handle with care.",                      "effect": None, "sell_price": 45, "stackable": True,  "usable_in_battle": False},
    "pine_resin":       {"id": "pine_resin",       "name": "Pine Resin",       "emoji": "🫙",  "type": "crafting",  "description": "Freshly tapped pine resin. Useful as a sealant or crafting material.",                        "effect": None, "sell_price": 20, "stackable": True,  "usable_in_battle": False},
    "snapped_torch":    {"id": "snapped_torch",    "name": "Snapped Torch",    "emoji": "🔦",  "type": "lore",      "description": "Burn end still warm. Someone was here recently and left in a hurry.",                         "effect": None, "sell_price": 2,  "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Cursed Grove ────────────────────────────────────────────
    "corrupted_bark":   {"id": "corrupted_bark",   "name": "Corrupted Bark",   "emoji": "🪵",  "type": "key_item",  "description": "Bark from one of the blackened trees. The discolouration goes all the way through.",           "effect": None, "sell_price": 30, "stackable": True,  "usable_in_battle": False},
    "cold_stone":       {"id": "cold_stone",       "name": "Cold Stone",       "emoji": "🪨",  "type": "key_item",  "description": "From inside the ring at the grove center. Stays cold regardless of temperature.",              "effect": None, "sell_price": 25, "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Ancient Ruins ───────────────────────────────────────────
    "ancient_coin":     {"id": "ancient_coin",     "name": "Ancient Coin",     "emoji": "💰",  "type": "key_item",  "description": "Pressed flat in the stonework. The markings predate anything in the city's records.",           "effect": None, "sell_price": 80, "stackable": True,  "usable_in_battle": False},
    "carved_fragment":  {"id": "carved_fragment",  "name": "Carved Fragment",  "emoji": "🪨",  "type": "key_item",  "description": "Part of the closed-eye symbol. Matches the full carving on the north wall.",                   "effect": None, "sell_price": 50, "stackable": True,  "usable_in_battle": False},
    "cracked_seal":     {"id": "cracked_seal",     "name": "Cracked Seal",     "emoji": "🔏",  "type": "key_item",  "description": "A wax seal with the Sovereignty insignia. Already opened.",                                    "effect": None, "sell_price": 40, "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Fisherman's Cove ────────────────────────────────────────
    "dried_kelp":       {"id": "dried_kelp",       "name": "Dried Kelp",       "emoji": "🌊",  "type": "crafting",  "description": "High quality, probably Grull's. Useful for Hana's tinctures.",                                "effect": None, "sell_price": 15, "stackable": True,  "usable_in_battle": False},
    "fish_hook":        {"id": "fish_hook",        "name": "Fish Hook",        "emoji": "🪝",  "type": "tool",      "description": "Hand-forged. Better than anything sold in the Market Quarter.",                               "effect": None, "sell_price": 22, "stackable": True,  "usable_in_battle": False},
    "sea_glass":        {"id": "sea_glass",        "name": "Sea Glass",        "emoji": "💎",  "type": "material",  "description": "Unusually dark. Not the usual colour. From deeper water, maybe.",                             "effect": None, "sell_price": 30, "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Sea Caves ───────────────────────────────────────────────
    "cave_crystal":     {"id": "cave_crystal",     "name": "Cave Crystal",     "emoji": "💠",  "type": "key_item",  "description": "A clear crystal from the cave wall. Something dark at its center.",                           "effect": None, "sell_price": 55, "stackable": True,  "usable_in_battle": False},
    "salt_rock":        {"id": "salt_rock",        "name": "Salt Rock",        "emoji": "🪨",  "type": "material",  "description": "Naturally formed. The mineral content smells wrong.",                                         "effect": None, "sell_price": 10, "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Smuggler's Trail ────────────────────────────────────────
    "dropped_manifest": {"id": "dropped_manifest", "name": "Dropped Manifest", "emoji": "📑",  "type": "key_item",  "description": "The destination column has been crossed out and rewritten. Maren would want to see this.",     "effect": None, "sell_price": 5,  "stackable": True,  "usable_in_battle": False},
    "oil_cloth":        {"id": "oil_cloth",        "name": "Oil Cloth",        "emoji": "🧻",  "type": "material",  "description": "Used to waterproof cargo. Fresh. The ore smell is unmistakable.",                             "effect": None, "sell_price": 12, "stackable": True,  "usable_in_battle": False},
    "iron_ring":        {"id": "iron_ring",        "name": "Iron Ring",        "emoji": "⭕",  "type": "material",  "description": "Used to lash cargo to carts. Rope fibres still in the groove — recent use.",                   "effect": None, "sell_price": 10, "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Residential Ward ────────────────────────────────────────
    "debt_notice":      {"id": "debt_notice",      "name": "Debt Notice",      "emoji": "📃",  "type": "lore",      "description": "Torn from a door and left in the gutter. A new one will be up tomorrow.",                      "effect": None, "sell_price": 1,  "stackable": True,  "usable_in_battle": False},
    "child_drawing":    {"id": "child_drawing",    "name": "Child's Drawing",  "emoji": "🖼️", "type": "lore",      "description": "A fish, a boat, an island. Something they were told about but have never seen.",                "effect": None, "sell_price": 1,  "stackable": True,  "usable_in_battle": False},
    # ── Walk finds — Shadow Den ──────────────────────────────────────────────
    "guard_token":      {"id": "guard_token",      "name": "Guard Token",      "emoji": "🎫",  "type": "key_item",  "description": "A mercenary access token. Still valid.",                                                     "effect": None, "sell_price": 35, "stackable": True,  "usable_in_battle": False},
    "mercenary_badge":  {"id": "mercenary_badge",  "name": "Mercenary Badge",  "emoji": "🏅",  "type": "key_item",  "description": "Shadow Den unit badge. Mercer's private company, not the Council's.",                        "effect": None, "sell_price": 45, "stackable": True,  "usable_in_battle": False},
    "sovereignty_seal": {"id": "sovereignty_seal", "name": "Sovereignty Seal", "emoji": "🔏",  "type": "key_item",  "description": "The closed-eye symbol in wax. Broken — from a document already opened.",                      "effect": None, "sell_price": 30, "stackable": True,  "usable_in_battle": False},
    # ── Bag upgrades ─────────────────────────────────────────────────────────
    "travelers_pack": {
        "id": "travelers_pack", "name": "Traveler's Pack", "emoji": "🎒", "type": "bag_upgrade",
        "description": "A sturdy canvas pack. Increases bag capacity to 35 slots. Use from your inventory.",
        "effect": None, "capacity": 35, "sell_price": 0, "stackable": False, "usable_in_battle": False,
    },
    "merchants_satchel": {
        "id": "merchants_satchel", "name": "Merchant's Satchel", "emoji": "👜", "type": "bag_upgrade",
        "description": "Soft leather with multiple compartments. Increases bag capacity to 50 slots. Use from your inventory.",
        "effect": None, "capacity": 50, "sell_price": 0, "stackable": False, "usable_in_battle": False,
    },
    "adventurers_trunk": {
        "id": "adventurers_trunk", "name": "Adventurer's Trunk", "emoji": "🧳", "type": "bag_upgrade",
        "description": "Reinforced hardwood with iron clasps. Increases bag capacity to 75 slots. Use from your inventory.",
        "effect": None, "capacity": 75, "sell_price": 0, "stackable": False, "usable_in_battle": False,
    },
    # ── Gathering tools ───────────────────────────────────────────────────────
    "rusty_pickaxe": {
        "id": "rusty_pickaxe", "name": "Rusty Pickaxe", "emoji": "⛏️", "type": "tool",
        "slot": "pickaxe", "description": "Old but functional. Equip from your bag — required for mining.",
        "effect": None, "price": 150, "sell_price": 50, "stackable": False, "usable_in_battle": False,
    },
    "iron_pickaxe": {
        "id": "iron_pickaxe", "name": "Iron Pickaxe", "emoji": "⛏️", "type": "tool",
        "slot": "pickaxe", "description": "Solid iron head, good grip. Better ore yield than the rusty version.",
        "effect": None, "price": 400, "sell_price": 150, "stackable": False, "usable_in_battle": False,
    },
    "weak_axe": {
        "id": "weak_axe", "name": "Weak Axe", "emoji": "🪓", "type": "tool",
        "slot": "axe", "description": "A worn hatchet. Gets the job done for basic woodcutting.",
        "effect": None, "price": 120, "sell_price": 40, "stackable": False, "usable_in_battle": False,
    },
    "iron_axe": {
        "id": "iron_axe", "name": "Iron Axe", "emoji": "🪓", "type": "tool",
        "slot": "axe", "description": "Well-balanced iron axe. Clean cuts, better timber quality.",
        "effect": None, "price": 350, "sell_price": 130, "stackable": False, "usable_in_battle": False,
    },
    "excavation_brush": {
        "id": "excavation_brush", "name": "Excavation Brush", "emoji": "🏺", "type": "tool",
        "slot": "trowel", "description": "Soft-bristle brush for careful artifact extraction. Required for excavation.",
        "effect": None, "price": 250, "sell_price": 80, "stackable": False, "usable_in_battle": False,
    },
    # ── Gathering resources — fish ────────────────────────────────────────────
    "goldfish":      {"id": "goldfish",    "name": "Goldfish",    "emoji": "🐟", "type": "material", "description": "A small goldfish caught near the docks. Sells well at the fish market.",                "effect": None, "sell_price": 12, "stackable": True, "usable_in_battle": False},
    "bass":          {"id": "bass",        "name": "Large Bass",  "emoji": "🐠", "type": "material", "description": "A substantial bass — good eating, better selling. Requires skill to land.",            "effect": None, "sell_price": 30, "stackable": True, "usable_in_battle": False},
    "cave_eel":      {"id": "cave_eel",    "name": "Cave Eel",    "emoji": "🐍", "type": "material", "description": "A long cave eel from the sea caves. Rare catch, high value.",                         "effect": None, "sell_price": 75, "stackable": True, "usable_in_battle": False},
    # ── Gathering resources — wood ────────────────────────────────────────────
    "common_wood":   {"id": "common_wood", "name": "Common Wood", "emoji": "🌳", "type": "material", "description": "Straight-grained common timber. Standard crafting material.",                          "effect": None, "sell_price": 15, "stackable": True, "usable_in_battle": False},
    "ashwood_plank": {"id": "ashwood_plank","name": "Ashwood Plank","emoji": "🌲","type": "material", "description": "Dense ashwood timber, cut and ready. Quality crafting material.",                     "effect": None, "sell_price": 40, "stackable": True, "usable_in_battle": False},
    # ── Mini-boss drop items ──────────────────────────────────────────────────
    "dock_authority_badge": {
        "id": "dock_authority_badge", "name": "Dock Authority Badge", "emoji": "🪪", "type": "key_item",
        "description": "Mercer's private badge, not the Council's. Proof that the docks aren't as official as they look.",
        "effect": None, "sell_price": 55, "stackable": True, "usable_in_battle": False,
    },
    "night_manifest_copy": {
        "id": "night_manifest_copy", "name": "Night Manifest Copy", "emoji": "📑", "type": "key_item",
        "description": "A ledger copy from the night shift. The cargo descriptions have been altered twice. Maren would want to see this.",
        "effect": None, "sell_price": 40, "stackable": True, "usable_in_battle": False,
    },
    "bandit_captain_seal": {
        "id": "bandit_captain_seal", "name": "Bandit Captain's Seal", "emoji": "⚜️", "type": "material",
        "description": "Rusk's personal seal. Someone in Mercer's organisation has been coordinating with the bandits.",
        "effect": None, "sell_price": 70, "stackable": True, "usable_in_battle": False,
    },
    "witchbone_talisman": {
        "id": "witchbone_talisman", "name": "Witchbone Talisman", "emoji": "🦴", "type": "crafting",
        "description": "A talisman carved from something that isn't bone. The cove fishermen won't touch it.",
        "effect": None, "sell_price": 65, "stackable": True, "usable_in_battle": False,
    },
    "poachers_kit": {
        "id": "poachers_kit", "name": "Poacher's Kit", "emoji": "🎯", "type": "material",
        "description": "Specialised equipment for hunting in the conservation zone. Stamped with a Mercer Trading Company mark.",
        "effect": None, "sell_price": 60, "stackable": True, "usable_in_battle": False,
    },
    "mercenary_contract": {
        "id": "mercenary_contract", "name": "Mercenary Contract", "emoji": "📜", "type": "key_item",
        "description": "A signed transport contract. The employer's name has been blacked out but the handwriting matches Mercer's.",
        "effect": None, "sell_price": 35, "stackable": True, "usable_in_battle": False,
    },
    "warden_stone": {
        "id": "warden_stone", "name": "Warden's Stone", "emoji": "🟫", "type": "key_item",
        "description": "A flat stone marked with a symbol you don't recognise. It's warm in a way the grove isn't.",
        "effect": None, "sell_price": 80, "stackable": True, "usable_in_battle": False,
    },
    "ancient_key_fragment": {
        "id": "ancient_key_fragment", "name": "Ancient Key Fragment", "emoji": "🗝️", "type": "key_item",
        "description": "Half of something older than Ironhaven. The other half is somewhere in the ruins.",
        "effect": None, "sell_price": 120, "stackable": True, "usable_in_battle": False,
    },
    "titan_bone_shard": {
        "id": "titan_bone_shard", "name": "Titan Bone Shard", "emoji": "🦷", "type": "material",
        "description": "A fragment from the Cave Titan. Dense enough to be used as a striking surface.",
        "effect": None, "sell_price": 90, "stackable": True, "usable_in_battle": False,
    },
    "voss_insignia": {
        "id": "voss_insignia", "name": "Commander Voss's Insignia", "emoji": "🎖️", "type": "key_item",
        "description": "The Shadow Den command insignia. Someone will want this — or fear it.",
        "effect": None, "sell_price": 0, "stackable": False, "usable_in_battle": False,
    },
}

# ---------------------------------------------------------------------------
# SHOPS
# ---------------------------------------------------------------------------

SHOPS: dict[str, dict] = {
    "general_store": {
        "id": "general_store", "name": "General Store", "building_id": "general_store", "npc_id": "old_tomas",
        "stock": [
            {"item_id": "health_potion", "price": 50,  "stock": -1},
            {"item_id": "antidote",      "price": 35,  "stock": -1},
            {"item_id": "bait",          "price": 10,  "stock": -1},
            {"item_id": "fishing_rod",   "price": 200, "stock": 3},
            {"item_id": "seeds_common",  "price": 20,  "stock": -1},
            {"item_id": "rusty_pickaxe", "price": 150, "stock": -1},
            {"item_id": "weak_axe",      "price": 120, "stock": -1},
            {"item_id": "travelers_pack","price": 500, "stock": -1},
        ],
    },
    "potion_emporium": {
        "id": "potion_emporium", "name": "Potion Emporium", "building_id": "potion_emporium", "npc_id": "nurse_hana",
        "stock": [
            {"item_id": "health_potion",  "price": 55,  "stock": -1},
            {"item_id": "strong_potion",  "price": 130, "stock": -1},
            {"item_id": "antidote",       "price": 40,  "stock": -1},
            {"item_id": "smelling_salts", "price": 220, "stock": 5},
        ],
    },
    "equipment_shop": {
        "id": "equipment_shop", "name": "Ironhaven Armory", "building_id": "equipment_shop", "npc_id": "forge_arm",
        "stock": [
            {"item_id": "sword_iron",        "price": 300, "stock": -1},
            {"item_id": "armor_leather",     "price": 280, "stock": -1},
            {"item_id": "iron_pickaxe",      "price": 400, "stock": -1},
            {"item_id": "iron_axe",          "price": 350, "stock": -1},
            {"item_id": "excavation_brush",  "price": 250, "stock": -1},
        ],
    },
    "card_shop": {
        "id": "card_shop", "name": "The Gilded Draw", "building_id": "card_shop", "npc_id": "vex",
        "stock": [
            {"card_id": "basic_strike", "price": 80,  "stock": -1},
            {"card_id": "basic_block",  "price": 80,  "stock": -1},
            {"card_id": "cleave",       "price": 200, "stock": 3},
            {"card_id": "frost_bolt",   "price": 200, "stock": 3},
            {"card_id": "poison_edge",  "price": 180, "stock": 3},
        ],
    },
    "tailor": {
        "id": "tailor", "name": "Mira's Threads", "building_id": "tailor", "npc_id": "mira",
        "stock": [
            {"item_id": "travelers_pack",    "price": 500,  "stock": -1},
            {"item_id": "merchants_satchel", "price": 1500, "stock": -1},
            {"item_id": "adventurers_trunk", "price": 3000, "stock": -1},
        ],
    },
}

# ---------------------------------------------------------------------------
# STORYLETS
# ---------------------------------------------------------------------------

STORYLETS: dict[str, dict] = {
    "arc1_the_request": {
        "id": "arc1_the_request", "arc": "arc_1", "title": "The Missing Shipment",
        "zone_id": "port_district", "trigger": {"npc_id": "maren", "visit_count": 3},
        "description": (
            "Maren sets down her ledger and looks at you directly for the first time.\n\n"
            "*\"I'm going to tell you something and pretend I didn't.\"*\n\n"
            "She describes a cargo vessel — The Dawnbreak — that docked three weeks ago with a "
            "registered cargo of textiles. It was offloaded. Except the textiles didn't go to "
            "the merchant who ordered them. They went somewhere into the forest.\n\n"
            "*\"The manifest was altered. Council stamp and everything. I've got the original "
            "copy, but a copy doesn't prove anything without the destination.\"*\n\n"
            "She slides the original manifest across the desk.\n\n"
            "*\"I'd go myself. But I can't disappear from this office without Mercer noticing.\"*"
        ),
        "choices": [
            {"id": "accept",  "label": "Accept the job", "description": "Investigate what happened to The Dawnbreak's cargo."},
            {"id": "decline", "label": "Not yet",        "description": "This feels bigger than you're ready for."},
        ],
        "outcomes": {
            "accept":  {"flag_set": "arc1_step1_accepted", "xp": 25, "zet": 0, "next_storylet": "arc1_into_the_forest", "message": "Maren nods once. *'Don't take the main road. The patrols are Mercer's, not the Council's. That matters.'*"},
            "decline": {"flag_set": None,                  "xp": 0,  "zet": 0, "next_storylet": None,                   "message": "She puts the manifest away. *'Fair. Come back when you decide.'*"},
        },
    },
    "arc1_into_the_forest": {
        "id": "arc1_into_the_forest", "arc": "arc_1", "title": "Into the Forest",
        "zone_id": "ashwood_forest", "trigger": {"flag": "arc1_step1_accepted"},
        "description": (
            "Following the manifest's origin codes into Ashwood Forest, you find something wrong.\n\n"
            "The trail splits at a collapsed waystation. One path leads deeper into the conservation "
            "zone — the one the Council claims is protected. Except the brush is cleared here. "
            "Recently. Fresh cart tracks.\n\n"
            "Behind a false wall in the waystation you find crates. They're not textiles. They're "
            "unmarked, reinforced, and warm to the touch. One has a hairline crack. Inside: dark ore "
            "that seems to absorb the light around it.\n\n"
            "A cold voice from behind you.\n\n"
            "*\"You're either very brave or very uninformed. I'll give you a moment to decide which.\"*"
        ),
        "choices": [
            {"id": "stand_ground", "label": "Turn and face them", "description": "You don't run."},
            {"id": "flee",         "label": "Run",                "description": "Not everything needs a confrontation."},
        ],
        "outcomes": {
            "stand_ground": {"flag_set": "arc1_step2_confronted", "xp": 50, "zet": 0, "next_storylet": "arc1_confrontation", "message": "You turn. A figure in dark clothing studies you. *'Interesting choice,'* they say. *'Come to the ruins. Tomorrow. Alone.'*"},
            "flee":         {"flag_set": "arc1_step2_fled",        "xp": 20, "zet": 0, "next_storylet": "arc1_confrontation", "message": "You run. But they aren't chasing. *'Tomorrow,'* a voice carries. *'The ruins. Alone.'*"},
        },
    },
    "arc1_confrontation": {
        "id": "arc1_confrontation", "arc": "arc_1", "title": "The Confrontation",
        "zone_id": "ancient_ruins", "trigger": {"flag": "arc1_step2_confronted", "or_flag": "arc1_step2_fled"},
        "description": (
            "The ancient ruins at dusk. Shade is already there.\n\n"
            "He doesn't draw a weapon. He watches you walk across the cracked stone plaza with the "
            "patience of someone who has done a great deal of waiting.\n\n"
            "*\"Mercer would like me to offer you something. It's a generous offer, actually.\"*\n\n"
            "He holds out a pouch. 200 Zet.\n\n"
            "*\"You walk away from what you saw in the forest. You don't talk to Maren again. "
            "That's the whole deal.\"*\n\n"
            "He looks at the pouch, then at you.\n\n"
            "*\"For what it's worth — I'm not telling you to take it because I think you will. "
            "I'm offering it because they require me to.\"*"
        ),
        "choices": [
            {"id": "refuse_bribe", "label": "Refuse",        "description": "Some things aren't for sale."},
            {"id": "take_bribe",   "label": "Take the Zet",  "description": "200 Zet is 200 Zet."},
        ],
        "outcomes": {
            "refuse_bribe": {"flag_set": "arc1_complete_resist",  "xp": 300, "zet": 0,   "item_reward": "shades_coat", "next_storylet": None, "message": "A long silence. Then Shade nods — once, slowly. *'I thought so.'* — Arc 1 Complete. Resistance +15."},
            "take_bribe":   {"flag_set": "arc1_complete_bribed",  "xp": 50,  "zet": 200, "next_storylet": None,        "message": "You take the pouch. *'Good.'* He turns away. — Arc 1 Complete (bribed path). Mercer +5, Resistance -10."},
        },
    },
    "arc1_tomas_letter": {
        "id": "arc1_tomas_letter", "arc": "arc_1", "title": "Tomás and the Letter",
        "zone_id": "market_quarter", "trigger": {"flag": "arc1_step1_accepted", "npc_id": "old_tomas", "relationship_min": 15},
        "description": (
            "The General Store is quiet. Tomás has been moving slower all morning — rearranging things "
            "that don't need rearranging. When you come in he smiles the right way, but his hands "
            "don't stop moving.\n\n"
            "You ask how he is.\n\n"
            "He tells you he's fine. He mentions the weather. He tells you about a new shipment of "
            "dried goods he's expecting.\n\n"
            "Then he drops a jar. Not badly — it doesn't break — but he drops it, and in the pause "
            "that follows something gives way.\n\n"
            "He pulls a folded letter from under the counter. He holds it for a moment before he "
            "gives it to you.\n\n"
            "*\"From Dario. My son.\"* He clears his throat. *\"He's working. Forest operation. "
            "Good work — steady pay.\"* A pause. *\"He says he's fine.\"*\n\n"
            "The letter says: *Don't come looking. I mean it. I'm fine. Please just don't.*"
        ),
        "choices": [
            {"id": "find_him",  "label": "\"I'll find him.\"",    "description": "Make the promise."},
            {"id": "reassure",  "label": "\"He sounds alright.\"","description": "Let him have the lie."},
        ],
        "outcomes": {
            "find_him": {"flag_set": "tomas_letter_seen", "flag_set_2": "tomas_promise_made", "xp": 30, "zet": 0, "item_reward": None, "next_storylet": "arc1_finding_dario",
                         "message": "He looks at you. Just for a moment, something shifts — relief, and fear, and a father's grief all at once.\n\n*\"I didn't ask you to,\"* he says.\n\nAnd then, quieter: *\"Thank you.\"*"},
            "reassure": {"flag_set": "tomas_letter_seen", "flag_set_2": None,               "xp": 10, "zet": 0, "item_reward": None, "next_storylet": "arc1_finding_dario",
                         "message": "You both know you're lying to each other.\n\nTomás nods. *\"Yes,\"* he says. *\"He does.\"*\n\nHe starts rearranging things again."},
        },
    },
    "arc1_finding_dario": {
        "id": "arc1_finding_dario", "arc": "arc_1", "title": "Finding Dario",
        "zone_id": "ashwood_forest", "trigger": {"flag": "tomas_letter_seen", "zone_id": "ashwood_forest"},
        "description": (
            "You find him in the part of the forest that isn't on any map.\n\n"
            "Not imprisoned — nothing that clean. Dario is twenty-two, lean from work, and he looks "
            "at you with the specific expression of someone who has been hoping for rescue and "
            "dreading it in equal measure.\n\n"
            "There are crates nearby. The ore smell is unmistakable.\n\n"
            "He says his name before you can ask. He says: *\"You know my father.\"* Not a question.\n\n"
            "He explains the situation the way someone explains a weather forecast — matter-of-fact, "
            "because nothing about it can be changed by emotion. The debt started small. Mercer's bank "
            "rolled it over and over. Now it's structural. Dario came out here to pay it down directly. "
            "Forty percent cleared per year. Legal contract. Signed.\n\n"
            "*\"If I leave,\"* he says, *\"the debt doubles. Penalty clause. Dad loses the store.\"* "
            "He looks at you. *\"I'm not asking to be saved. I'm asking for the debt to go away.\"*"
        ),
        "choices": [
            {"id": "rescue_now",  "label": "\"I'm getting you out now.\"",        "description": "Pull him out regardless."},
            {"id": "handle_debt", "label": "\"I'll handle the debt. Tell me everything.\"", "description": "Do this the right way."},
        ],
        "outcomes": {
            "rescue_now":  {"flag_set": "finding_dario_done", "flag_set_2": "dario_rescued_badly", "xp": 40, "zet": 0, "item_reward": None,              "next_storylet": "arc1_hanas_records",
                            "message": "*\"You're not listening,\"* he says quietly. *\"If I walk out of here, my father's store is gone by morning.\"*\n\nHe gives you information anyway — guard rotation, crate schedules, a name inside the Council.\n\n*\"For when you're ready to do this right.\"*\n\nYou leave without him."},
            "handle_debt": {"flag_set": "finding_dario_done", "flag_set_2": "dario_intel_gained", "xp": 60, "zet": 0, "item_reward": "dropped_manifest", "next_storylet": "arc1_hanas_records",
                            "message": "Something in him settles. He talks for twenty minutes.\n\nGuard rotation. The ore transfer schedule. The name of the Council member who signs off on the manifests.\n\n*\"There's a ledger,\"* he says. *\"Hana has a copy. She doesn't know I know.\"* He pauses. *\"Don't tell my father I said that.\"*"},
        },
    },
    "arc1_hanas_records": {
        "id": "arc1_hanas_records", "arc": "arc_1", "title": "Hana's Records",
        "zone_id": "market_quarter", "trigger": {"flag": "finding_dario_done", "npc_id": "nurse_hana", "relationship_min": 15},
        "description": (
            "The Potion Emporium is closed. The sign says it, but the light is on.\n\n"
            "When you knock she answers immediately — as if she's been waiting.\n\n"
            "She goes to the back. Unlocks something. Returns with a ledger — not the official one. "
            "Small. Cloth-covered. Written in an extremely neat hand.\n\n"
            "*\"I've been documenting since month four.\"* She opens to a marked page. Dates. "
            "Descriptions. *\"Injury patterns consistent with prolonged contact with the ore they're "
            "extracting. Three patients told me they fell. This one told me he walked into a door.\"*\n\n"
            "She closes the ledger. Holds it out to you.\n\n"
            "*\"I've made copies. They're somewhere Mercer can't find them.\"* She looks at you "
            "steadily. *\"I've been waiting for someone to give this to.\"*"
        ),
        "choices": [
            {"id": "take_evidence", "label": "\"This goes to someone who can use it.\"", "description": "Take the ledger."},
            {"id": "protect_hana",  "label": "\"Are you safe if this comes out?\"",      "description": "Ask about the risk to her first."},
        ],
        "outcomes": {
            "take_evidence": {"flag_set": "hanas_records_done", "flag_set_2": "evidence_obtained", "xp": 50, "zet": 0, "item_reward": "health_potion", "next_storylet": "arc1_vex_test",
                              "message": "She nods once. *\"Good.\"*\n\nShe also hands you a vial. *\"In case things get difficult before they get better.\"*\n\nYou take both. She lets you out the back."},
            "protect_hana":  {"flag_set": "hanas_records_done", "flag_set_2": "hana_protected",  "xp": 50, "zet": 0, "item_reward": None,            "next_storylet": "arc1_vex_test",
                              "message": "*\"I'm a medical professional with impeccable official records. What would anyone accuse me of?\"* She says it flatly. *\"I have been very careful.\"*\n\nShe hands you the ledger."},
        },
    },
    "arc1_rels_history": {
        "id": "arc1_rels_history", "arc": "arc_1", "title": "Rel's History",
        "zone_id": "town_square", "trigger": {"npc_id": "captain_rel", "relationship_min": 25},
        "description": (
            "He sits down.\n\n"
            "This is the first time you've seen him do it without it being deliberate — the movement "
            "of someone finally letting go of a maintained posture.\n\n"
            "He tells you about the day Mercer arrived. The ships. The bank charter. The Council seat. "
            "He tells you about watching it happen in slow motion — one decision at a time, each "
            "individually reasonable, collectively catastrophic.\n\n"
            "*\"I was the one who was supposed to stop it,\"* he says. *\"I had the contacts. The "
            "credibility. The training.\"* A long pause. *\"I waited for the right moment. The right "
            "moment doesn't come. You have to make it. I didn't understand that until it was too late.\"*\n\n"
            "He looks at his hands. Then at you.\n\n"
            "*\"I'm not waiting anymore. The moment is now. Not tomorrow. Not when things settle. "
            "Now — while people still remember what better looked like.\"*"
        ),
        "choices": [
            {"id": "move_now",  "label": "\"Then we move now.\"",  "description": "Meet his resolve with yours."},
            {"id": "ask_plan",  "label": "\"What's the plan?\"",   "description": "Understand before committing."},
        ],
        "outcomes": {
            "move_now": {"flag_set": "rels_history_done", "flag_set_2": "rel_committed", "xp": 40, "zet": 0, "item_reward": None, "next_storylet": None,
                         "message": "Something in his face — not quite relief. Resolve.\n\n*\"Tonight I make some calls,\"* he says. *\"Tomorrow we have a meeting. Bora's tavern. After closing.\"* He stands. *\"Don't be late.\"*"},
            "ask_plan": {"flag_set": "rels_history_done", "flag_set_2": "rel_committed", "xp": 40, "zet": 0, "item_reward": None, "next_storylet": None,
                         "message": "Almost a smile.\n\n*\"You don't wait for a plan to be perfect before you start it. You start it and you fix it as you go.\"* He stands. *\"Bora's tavern. After closing. Tomorrow.\"*"},
        },
    },
    "arc1_vex_test": {
        "id": "arc1_vex_test", "arc": "arc_1", "title": "Vex's Test",
        "zone_id": "market_quarter", "trigger": {"flag": "hanas_records_done", "npc_id": "vex", "relationship_min": 30},
        "description": (
            "The shop is empty. Vex slides a card across the counter. Face down. He doesn't look "
            "at you when he does it.\n\n"
            "*\"Don't flip it,\"* he says. *\"Just tell me — do you trust the person who gave it to you?\"*\n\n"
            "He waits.\n\nThen he speaks regardless.\n\n"
            "*\"There are six people in this city who know what Mercer's operation actually is. Not "
            "the debt scheme. Not the prices. The ore — what it is, what it does, what he's building "
            "with it.\"* He leans forward. *\"Those six people have never been in the same room. "
            "Mercer made sure of that. Until now.\"*\n\n"
            "He slides a folded note across the counter. An address. A time. Tonight.\n\n"
            "*\"Don't be late. Bring whatever you found in the forest.\"*"
        ),
        "choices": [
            {"id": "flip_card",      "label": "Flip the card.",      "description": "Trust your instincts."},
            {"id": "leave_face_down","label": "Leave it face down.", "description": "Trust his."},
        ],
        "outcomes": {
            "flip_card":       {"flag_set": "vex_test_done", "flag_set_2": "vex_test_flipped", "xp": 30, "zet": 0, "item_reward": None, "next_storylet": "arc1_resistance_forms",
                                "message": "Blank.\n\n*\"Wrong instinct,\"* Vex says. Not unkindly. *\"But honest. I can work with honest.\"* He takes the card back. *\"Don't be late.\"*"},
            "leave_face_down": {"flag_set": "vex_test_done", "flag_set_2": "vex_test_passed",  "xp": 50, "zet": 0, "item_reward": None, "next_storylet": "arc1_resistance_forms",
                                "message": "*\"Right instinct.\"*\n\nHe looks at you differently now.\n\n*\"The card doesn't matter. The pause before you touched it — that matters.\"*\n\n*\"Don't be late.\"*"},
        },
    },
    "arc1_resistance_forms": {
        "id": "arc1_resistance_forms", "arc": "arc_1", "title": "The Resistance Forms",
        "zone_id": "port_district", "trigger": {"flag": "vex_test_done", "flag_2": "rel_committed", "zone_id": "port_district"},
        "description": (
            "Bora's tavern, past closing. Chairs up on the tables. A lamp on the bar.\n\n"
            "Maren. Rel. Vex. Three people who have never been in the same room — or if they have, "
            "it wasn't like this. They're not looking at each other. They're looking at you.\n\n"
            "Bora sets cups down without being asked and goes back behind the bar.\n\n"
            "Maren speaks first. The real manifests. Forty-three shipments over eleven months. All "
            "going to the same facility three kilometers into the conservation zone that doesn't "
            "officially exist.\n\n"
            "Hana isn't there. But she's represented: a sealed envelope that Vex opens and reads "
            "aloud. Clinical. Precise. Devastating.\n\n"
            "Rel says nothing. He doesn't need to.\n\n"
            "Vex sets down the letter. *\"We have enough. The question is what we do with it.\"*\n\n"
            "The ore shipment moves in three days. This is the window."
        ),
        "choices": [
            {"id": "move_tomorrow", "label": "\"We move tomorrow.\"",      "description": "Strike before they're ready."},
            {"id": "plan_properly", "label": "\"We plan this properly.\"", "description": "One chance — don't waste it."},
        ],
        "outcomes": {
            "move_tomorrow": {"flag_set": "resistance_formed", "flag_set_2": "timeline_fast",    "xp": 75, "zet": 0, "item_reward": "strong_potion", "next_storylet": "arc1_climax_revelation",
                              "message": "Maren nods. Rel stands. *\"Then we have tonight to prepare.\"*\n\nBora, from behind the bar, without turning around: *\"I'll handle the food.\"*\n\nFor the first time in eleven years, six people in Ironhaven are in the same room."},
            "plan_properly": {"flag_set": "resistance_formed", "flag_set_2": "timeline_careful", "xp": 75, "zet": 0, "item_reward": "strong_potion", "next_storylet": "arc1_climax_revelation",
                              "message": "Vex almost smiles. *\"Good. Amateur hour gets people hurt.\"*\n\nBora puts the chairs down. Rel lays out the facility map. Maren opens the manifests.\n\nFor the first time in eleven years, six people in Ironhaven are in the same room — and they mean to stay that way."},
        },
    },
    "arc1_climax_revelation": {
        "id": "arc1_climax_revelation", "arc": "arc_1", "title": "The Revelation",
        "zone_id": "town_square", "trigger": {"flag": "resistance_formed", "zone_id": "town_square"},
        "description": (
            "Dawn. The city is quiet.\n\n"
            "You have the evidence — Hana's ledger, forty-three manifests, Dario's information about "
            "the Council member who has been signing off on every transfer. The ore shipment moves today.\n\n"
            "This is the window.\n\n"
            "The Council Hall notice board faces the square. The harbour office board faces the docks. "
            "The Guild board faces the market. Three places where everyone in Ironhaven walks past "
            "before noon.\n\n"
            "Or: one envelope, slipped under the door of Councilmember Aldric — the name Dario gave "
            "you. The one who has been asking uncomfortable questions in chambers for two years."
        ),
        "choices": [
            {"id": "go_public",   "label": "Post the evidence publicly.",       "description": "Forty-three copies. Every board in the city."},
            {"id": "go_internal", "label": "Deliver it to Councilmember Aldric.","description": "The quiet path. Slower but safer."},
        ],
        "outcomes": {
            "go_public":   {"flag_set": "arc1_revelation_done", "flag_set_2": "revelation_public",   "xp": 100, "zet": 0, "item_reward": None, "next_storylet": "arc1_climax_assembly",
                            "message": "By the time the Council soldiers start pulling the papers down, half the city has already read them.\n\nYou watch from across the square as a crowd forms at the Guild board. Two dock workers read the manifest list aloud to a third who can't. Someone tears Mercer's portrait partially off the wall — thinks better of it. Leaves it hanging at an angle.\n\n*The ruins. One hour.*"},
            "go_internal": {"flag_set": "arc1_revelation_done", "flag_set_2": "revelation_internal", "xp": 80,  "zet": 0, "item_reward": None, "next_storylet": "arc1_climax_assembly",
                            "message": "The envelope goes under the door in the quiet hour before the Hall opens.\n\nBy midmorning, Councilmember Aldric has called an emergency session. By noon, two of Mercer's appointments have stopped returning messages.\n\n*The ruins. Tonight.*"},
        },
    },
    "arc1_climax_assembly": {
        "id": "arc1_climax_assembly", "arc": "arc_1", "title": "The Assembly",
        "zone_id": "ancient_ruins", "trigger": {"flag": "arc1_revelation_done", "zone_id": "ancient_ruins"},
        "description": (
            "They come in ones and twos — the way resistance people do. Not together. From different "
            "directions. At different times.\n\n"
            "Dario is there. He looks different outside the forest. Lighter.\n\n"
            "Old Tomás is there. He has never been to the ruins before. He is very upright. "
            "He does not look afraid.\n\n"
            "Rel speaks. Not a speech — just the situation, plainly. The evidence is out. The window "
            "is closing. The ore operation will lock down within hours.\n\n"
            "*\"One facility,\"* he says. *\"Three kilometers in. The people working it aren't the "
            "enemy — they're Dario.\"* He doesn't look at Dario. Dario looks at the floor. "
            "*\"We're going for the master ledger. The one with Mercer's name on every transaction.\"*\n\n"
            "He looks at you. Everyone looks at you.\n\n"
            "You're the one who connected all of this."
        ),
        "choices": [
            {"id": "lets_go", "label": "\"Let's go.\"", "description": "Two words. Enough."},
        ],
        "outcomes": {
            "lets_go": {"flag_set": "arc1_assembly_done", "flag_set_2": None, "xp": 50, "zet": 0, "item_reward": None, "next_storylet": "arc1_climax_confrontation",
                        "message": "Tomás straightens. Dario exhales slowly.\n\nMaren checks something in her coat. Vex pockets something you didn't see him take out. Rel nods — once, the way someone who has been waiting eleven years nods when the moment finally arrives.\n\nYou move."},
        },
    },
    "arc1_climax_confrontation": {
        "id": "arc1_climax_confrontation", "arc": "arc_1", "title": "The Confrontation",
        "zone_id": "ancient_ruins", "trigger": {"flag": "arc1_assembly_done", "zone_id": "ancient_ruins"},
        "description": (
            "The facility. The ledger. You find it.\n\n"
            "And then you find Shade.\n\n"
            "He's standing between you and the exit. He isn't moving to stop you. He's just standing "
            "there — the way he does everything. Deliberate. Patient. Carrying weight you've only "
            "begun to understand.\n\n"
            "*\"I know what you have,\"* he says. *\"I've known for a month that this was coming.\"* "
            "A pause. *\"Mercer asked me to move against you four times. I found reasons not to each time.\"*\n\n"
            "He looks at you.\n\n"
            "*\"The people in this city who are pretending things are fine — they reminded me of someone. "
            "I couldn't figure out who.\"*\n\n"
            "He picks up his coat. He drapes it over his arm.\n\n"
            "*\"It was me. Eleven years ago. Before I took his deal because I had nothing left and "
            "couldn't think of another option.\"*\n\n"
            "A long silence. The facility is quiet. Outside, Ironhaven is deciding what kind of city it is.\n\n"
            "*\"I'm done finding reasons.\"*"
        ),
        "choices": [
            {"id": "walk_with_us", "label": "\"Walk with us.\"", "description": "Offer him a way back."},
            {"id": "walk_away",    "label": "\"Walk away.\"",    "description": "Give him his freedom. Ask for nothing."},
        ],
        "outcomes": {
            "walk_with_us": {"flag_set": "arc1_resolved", "flag_set_2": "shade_joined",   "xp": 300, "zet": 200, "item_reward": "shades_coat", "next_storylet": None,
                             "message": "He doesn't answer immediately.\n\nHe looks at the coat in his hands. Sets it down on a crate.\n\nWhen he walks toward you it's with the specific posture of someone who has made a decision they've been rehearsing for eleven years.\n\n*\"I don't have a plan,\"* he says.\n\n*\"Neither did we,\"* you say.\n\nHe walks with you.\n\n— **Arc 1 Complete. The resistance wins.**"},
            "walk_away":    {"flag_set": "arc1_resolved", "flag_set_2": "shade_departed", "xp": 250, "zet": 200, "item_reward": "shades_coat", "next_storylet": None,
                             "message": "He looks at you for a moment.\n\nThen he puts the coat on — slowly, deliberately — and walks toward the eastern entrance. He pauses once, without turning.\n\n*\"Tomás's debt,\"* he says. *\"I'll see to it that the documents are lost. Call it a final act of professional courtesy.\"*\n\nHe disappears into the forest.\n\nYou stand holding the ledger that will change everything.\n\n— **Arc 1 Complete. The city changes.**"},
        },
    },
}

# ---------------------------------------------------------------------------
# XP thresholds
# ---------------------------------------------------------------------------

XP_THRESHOLDS = [
    0, 200, 500, 1000, 2000, 3500, 5000, 7500, 10000, 15000,
    20000, 28000, 38000, 50000, 65000,
]


def xp_to_level_up(level: int) -> int:
    if level <= len(XP_THRESHOLDS):
        return XP_THRESHOLDS[min(level - 1, len(XP_THRESHOLDS) - 1)]
    return 20000 + (level - 11) * 8000


# ---------------------------------------------------------------------------
# Utility lookups
# ---------------------------------------------------------------------------

def get_zone(zone_id: str) -> dict | None:
    return ZONES.get(zone_id)

def get_npc(npc_id: str) -> dict | None:
    return NPCS.get(npc_id)

def get_enemy(enemy_id: str) -> dict | None:
    return ENEMIES.get(enemy_id)

def get_card(card_id: str) -> dict | None:
    return CARDS.get(card_id)

def get_item(item_id: str) -> dict | None:
    return ITEMS.get(item_id)

def get_race(race_id: str) -> dict | None:
    return RACES.get(race_id)

def get_class(class_id: str) -> dict | None:
    return CLASSES.get(class_id)

def get_shop(shop_id: str) -> dict | None:
    return SHOPS.get(shop_id)

def get_shop_for_building(building_id: str) -> dict | None:
    for shop in SHOPS.values():
        if shop.get("building_id") == building_id:
            return shop
    return None

def get_npcs_in_zone(zone_id: str) -> list[dict]:
    zone = ZONES.get(zone_id)
    if not zone:
        return []
    return [NPCS[nid] for nid in zone.get("npcs", []) if nid in NPCS]

def get_enemies_in_zone(zone_id: str) -> list[dict]:
    zone = ZONES.get(zone_id)
    if not zone:
        return []
    return [ENEMIES[eid] for eid in zone.get("enemy_ids", []) if eid in ENEMIES]

def get_buildings_in_zone(zone_id: str) -> list[dict]:
    zone = ZONES.get(zone_id)
    if not zone:
        return []
    return [BUILDINGS[bid] for bid in zone.get("buildings", []) if bid in BUILDINGS]

def cards_for_class(class_id: str) -> list[dict]:
    result = []
    for card in CARDS.values():
        restriction = card.get("class_restriction")
        if restriction is None or restriction == class_id:
            result.append(card)
    return result

def get_max_energy(player_stats: dict) -> int:
    intel = player_stats.get("intel", 0)
    return 6 + (intel // 5)