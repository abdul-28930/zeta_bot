"""
Battle Engine — Zeta

Manages card-based combat state entirely in Redis.
All state is serializable to/from dicts.
"""
import math
import random
from typing import Any

from game.data import CARDS, ENEMIES, get_card, get_enemy


# ---------------------------------------------------------------------------
# Status tick values (damage per turn)
# ---------------------------------------------------------------------------

DOT_STATUSES = {"burn", "poison", "bleed"}
DEBUFF_STATUSES = {"slow", "blind", "curse", "stun"}
BUFF_STATUSES = {"str", "def", "agi", "int", "vit"}


def build_initial_battle_state(
    user_id: int,
    enemy_id: str,
    player_stats: dict,
    player_deck: list[str],
    player_hp: int,
    player_max_hp: int,
    card_levels: dict[str, int] | None = None,
) -> dict:
    """Create a fresh battle state dict ready to store in Redis."""
    deck = player_deck.copy()
    random.shuffle(deck)

    # Draw starting hand of 4
    hand = []
    for _ in range(4):
        if deck:
            hand.append(deck.pop(0))

    enemy = ENEMIES[enemy_id]
    return {
        "user_id": user_id,
        "enemy_id": enemy_id,
        "enemy_name": enemy["name"],
        "enemy_hp": enemy["hp"],
        "enemy_max_hp": enemy["hp"],
        "enemy_atk": enemy["atk"],
        "enemy_defense": enemy["defense"],
        "enemy_shield": 0,
        "player_hp": player_hp,
        "player_max_hp": player_max_hp,
        "player_stats": player_stats,
        "player_shield": 0,
        "energy": 6,              # full energy on turn 1
        "max_energy": 6,
        "card_levels": card_levels or {},
        "hand": hand,
        "deck": deck,
        "discard": [],
        "turn": 1,
        "player_statuses": {},   # {status_name: {turns, value}}
        "enemy_statuses": {},
        "player_buffs": {},      # {stat: {amount, turns}}
        "next_card_discount": 0,
        "damage_buff_next": 0,
        "trap_damage": 0,        # Trap set: next enemy attack triggers this
        "dodge_turns": 0,
        "phase": "player",       # "player" | "enemy" | "end"
        "log": [],               # Last few actions for display
    }


# ---------------------------------------------------------------------------
# Effect resolution
# ---------------------------------------------------------------------------

def calc_damage(base: int, stat_val: int, scale: float, is_magic: bool = False) -> int:
    return max(1, int(base + stat_val * scale))


def resolve_card(card_id: str, state: dict, hand_index: int) -> dict:
    """
    Apply a card effect to the battle state.
    Returns updated state + result info dict.
    """
    card = get_card(card_id)
    if not card:
        return state

    # Remove from hand
    if hand_index < len(state["hand"]):
        state["hand"].pop(hand_index)
    state["discard"].append(card_id)

    # Deduct energy (with discount)
    cost = max(0, card["cost"] - state.get("next_card_discount", 0))
    state["energy"] = max(0, state["energy"] - cost)
    state["next_card_discount"] = 0  # Reset discount after use

    # Card level scaling: +15% to base effect values per level above 1
    card_level = state.get("card_levels", {}).get(card_id, 1)
    level_mult = 1.0 + (card_level - 1) * 0.15

    effect = card.get("effect", {})
    etype = effect.get("type", "damage")
    stats = state["player_stats"]
    result_msg = ""
    result_type = etype

    # --- Apply active buffs to stats temporarily ---
    effective_stats = stats.copy()
    for stat, buff in state.get("player_buffs", {}).items():
        if stat in effective_stats:
            effective_stats[stat] += buff.get("amount", 0)

    if etype == "damage":
        stat_key = effect.get("stat_scaling", "str")
        stat_val = effective_stats.get(stat_key, stats.get("str", 5))
        scale = effect.get("scale_factor", 0.5)
        base = int(effect.get("value", 5) * level_mult)
        hits = effect.get("hits", 1)
        total_dmg = 0

        for _ in range(hits):
            raw = calc_damage(base, stat_val, scale)
            raw += state.get("damage_buff_next", 0)

            # Apply bonus for backstab-style
            if effect.get("bonus_if_debuffed") and state["enemy_statuses"]:
                raw = int(raw * (1 + effect["bonus_if_debuffed"]))

            # Ignore defense flag
            if not effect.get("ignore_defense"):
                enemy_def = state["enemy_defense"]
                # DEF is reduced if enemy has slow/blind
                if "slow" in state["enemy_statuses"] or "blind" in state["enemy_statuses"]:
                    enemy_def = max(0, enemy_def - 3)
                raw = max(1, raw - enemy_def)

            # Apply to shield first
            if state["enemy_shield"] > 0:
                overflow = max(0, raw - state["enemy_shield"])
                state["enemy_shield"] = max(0, state["enemy_shield"] - raw)
                raw = overflow

            state["enemy_hp"] -= raw
            total_dmg += raw

        state["damage_buff_next"] = 0
        result_msg = f"Dealt **{total_dmg}** damage!"

        # Apply status from card
        if "status" in effect:
            s = effect["status"]
            state["enemy_statuses"][s["name"]] = {"turns": s["turns"], "value": s["value"]}
            result_msg += f" Applied **{s['name'].title()}**!"

        result_type = "damage"

    elif etype == "magic_damage":
        stat_val = effective_stats.get("int", 5)
        raw = calc_damage(int(effect.get("value", 8) * level_mult), stat_val, effect.get("scale_factor", 0.6))
        raw = max(1, raw)  # Magic ignores physical DEF by default
        if state["enemy_shield"] > 0:
            overflow = max(0, raw - state["enemy_shield"])
            state["enemy_shield"] = max(0, state["enemy_shield"] - raw)
            raw = overflow
        state["enemy_hp"] -= raw
        result_msg = f"Dealt **{raw}** magic damage!"
        result_type = "damage"

    elif etype == "heal":
        stat_val = effective_stats.get("int", 5)
        scale = effect.get("scale_factor", 0.5)
        heal_amt = calc_damage(int(effect.get("value", 10) * level_mult), stat_val, scale)
        actual_heal = min(heal_amt, state["player_max_hp"] - state["player_hp"])
        state["player_hp"] += actual_heal
        result_msg = f"Restored **{actual_heal}** HP!"
        result_type = "heal"

    elif etype == "shield":
        stat_val = effective_stats.get("def", 5)
        shield_val = calc_damage(int(effect.get("value", 5) * level_mult), stat_val, effect.get("scale_factor", 0.3))
        state["player_shield"] = state.get("player_shield", 0) + shield_val
        result_msg = f"Gained **{shield_val}** shield!"
        result_type = "shield"

    elif etype == "buff":
        b = effect["buff"]
        state["player_buffs"][b["stat"]] = {"amount": b["amount"], "turns": b["turns"]}
        result_msg = f"Gained **+{b['amount']} {b['stat'].upper()}** for {b['turns']} turns!"
        result_type = "buff"

    elif etype == "status":
        s = effect["status"]
        state["enemy_statuses"][s["name"]] = {"turns": s["turns"], "value": s["value"]}
        result_msg = f"Applied **{s['name'].title()}** to enemy!"
        result_type = "status"

    elif etype == "special":
        special = effect.get("special", "")

        if special == "next_card_discount":
            state["next_card_discount"] = effect.get("value", 1)
            result_msg = f"Next card costs {effect['value']} less energy!"

        elif special == "draw_and_energy":
            drawn = _draw_card(state)
            en = effect.get("energy", 1)
            state["energy"] = min(state["max_energy"], state["energy"] + en)
            result_msg = f"Drew 1 card & gained {en} energy!"

        elif special == "buff_and_draw":
            b = effect.get("buff", {})
            if b:
                state["player_buffs"][b["stat"]] = {"amount": b["amount"], "turns": b["turns"]}
            draws = effect.get("draw", 1)
            for _ in range(draws):
                _draw_card(state)
            result_msg = f"Buffed +{b.get('amount', 0)} {b.get('stat', '').upper()} & drew {draws} card!"

        elif special == "shield_and_buff":
            sv = effect.get("shield", 10)
            state["player_shield"] = state.get("player_shield", 0) + sv
            b = effect.get("buff", {})
            if b:
                state["player_buffs"][b["stat"]] = {"amount": b["amount"], "turns": b["turns"]}
            result_msg = f"Gained **{sv}** shield & +{b.get('amount',0)} {b.get('stat','').upper()}!"

        elif special == "dodge_and_blind":
            state["dodge_turns"] = effect.get("dodge_turns", 1)
            s = effect.get("status", {})
            if s:
                state["enemy_statuses"][s["name"]] = {"turns": s["turns"], "value": s["value"]}
            result_msg = "You'll dodge the next attack! Enemy is Blinded!"

        elif special == "set_trap":
            state["trap_damage"] = effect.get("trap_damage", 12)
            result_msg = f"Trap set! Deals **{state['trap_damage']}** damage on enemy's next attack!"

        elif special == "damage_buff_next":
            state["damage_buff_next"] = effect.get("value", 4)
            result_msg = f"Your next attack deals +{effect['value']} bonus damage!"

        elif special == "cleanse_all":
            cleared = list(state["player_statuses"].keys())
            state["player_statuses"] = {}
            result_msg = f"Cleansed all debuffs! ({', '.join(cleared) if cleared else 'none'})"

        result_type = "special"

    state["log"].append(f"▸ {card['name']}: {result_msg}")
    state["log"] = state["log"][-5:]  # Keep last 5 log entries
    return state


def resolve_enemy_turn(state: dict) -> dict:
    """Execute the enemy's turn: pick a move, apply it."""
    enemy = get_enemy(state["enemy_id"])
    if not enemy:
        return state

    # Check stun — skip turn
    if "stun" in state["enemy_statuses"]:
        _tick_status(state["enemy_statuses"], "stun")
        state["log"].append(f"▸ {enemy['name']} is stunned and loses their turn!")
        state["log"] = state["log"][-5:]
        return state

    # Pick a move (weighted random)
    moves = enemy.get("moves", [])
    if not moves:
        return state

    weights = [m.get("weight", 50) for m in moves]
    move = random.choices(moves, weights=weights, k=1)[0]

    move_type = move.get("type", "damage")

    if move_type == "damage":
        dmg = move.get("value", 10)
        # Dodge check
        if state.get("dodge_turns", 0) > 0:
            state["dodge_turns"] -= 1
            state["log"].append(f"▸ {enemy['name']} uses {move['name']} — you dodge it!")
        else:
            # Apply trap
            if state.get("trap_damage", 0) > 0:
                trap = state["trap_damage"]
                state["enemy_hp"] -= trap
                state["trap_damage"] = 0
                state["log"].append(f"▸ TRAP triggered! Deals {trap} damage to {enemy['name']}!")

            # Reduce dmg by player shield + defense
            pdef = state["player_stats"].get("def", 5)
            net = max(1, dmg - pdef)
            if state["player_shield"] > 0:
                overflow = max(0, net - state["player_shield"])
                state["player_shield"] = max(0, state["player_shield"] - net)
                net = overflow
            state["player_hp"] -= net
            state["log"].append(f"▸ {enemy['name']} uses {move['name']} — you take **{net}** damage!")

    elif move_type == "damage_status":
        dmg = move.get("value", 10)
        if state.get("dodge_turns", 0) > 0:
            state["dodge_turns"] -= 1
            state["log"].append(f"▸ {enemy['name']} uses {move['name']} — you dodge it!")
        else:
            pdef = state["player_stats"].get("def", 5)
            net = max(1, dmg - pdef)
            if state["player_shield"] > 0:
                overflow = max(0, net - state["player_shield"])
                state["player_shield"] = max(0, state["player_shield"] - net)
                net = overflow
            state["player_hp"] -= net
            s = move.get("status", {})
            if s:
                state["player_statuses"][s["name"]] = {"turns": s["turns"], "value": s["value"]}
            state["log"].append(f"▸ {enemy['name']} uses {move['name']} — {net} dmg! Applied {s.get('name','')}")

    elif move_type == "magic_damage":
        dmg = move.get("value", 10)
        net = max(1, dmg)  # Ignores DEF
        state["player_hp"] -= net
        state["log"].append(f"▸ {enemy['name']} uses {move['name']} — you take **{net}** magic damage!")

    elif move_type == "self_shield":
        sv = move.get("value", 10)
        state["enemy_shield"] = state.get("enemy_shield", 0) + sv
        state["log"].append(f"▸ {enemy['name']} raises their guard! (+{sv} shield)")

    elif move_type == "self_heal":
        heal = move.get("value", 5)
        state["enemy_hp"] = min(state["enemy_max_hp"], state["enemy_hp"] + heal)
        state["log"].append(f"▸ {enemy['name']} regenerates {heal} HP!")

    elif move_type == "status":
        s = move.get("status", {})
        if s:
            state["player_statuses"][s["name"]] = {"turns": s["turns"], "value": s["value"]}
        state["log"].append(f"▸ {enemy['name']} applies {s.get('name', '')} to you!")

    elif move_type == "flee":
        # Enemy flees — treat as enemy defeat
        state["enemy_hp"] = 0
        state["log"].append(f"▸ {enemy['name']} fled the battle!")

    elif move_type == "skip":
        state["log"].append(f"▸ {enemy['name']} stumbles and does nothing.")

    state["log"] = state["log"][-5:]
    return state


# ---------------------------------------------------------------------------
# Status tick & regen
# ---------------------------------------------------------------------------

def tick_start_of_player_turn(state: dict) -> dict:
    """Called at the start of each player turn: regen energy, tick statuses."""
    # Energy regen
    state["energy"] = min(state["max_energy"], state["energy"] + 2)

    # Draw card
    _draw_card(state)

    # Tick player DOT statuses
    for status_name in list(state["player_statuses"].keys()):
        info = state["player_statuses"][status_name]
        if status_name in DOT_STATUSES:
            dmg = info.get("value", 2)
            state["player_hp"] -= dmg
            state["log"].append(f"▸ {status_name.title()} deals {dmg} damage to you!")
        _tick_status(state["player_statuses"], status_name)

    # Tick enemy DOT statuses
    for status_name in list(state["enemy_statuses"].keys()):
        info = state["enemy_statuses"][status_name]
        if status_name in DOT_STATUSES:
            dmg = info.get("value", 2)
            state["enemy_hp"] -= dmg
            state["log"].append(f"▸ {status_name.title()} deals {dmg} damage to enemy!")
        _tick_status(state["enemy_statuses"], status_name)

    # Tick player buffs
    for stat in list(state.get("player_buffs", {}).keys()):
        state["player_buffs"][stat]["turns"] -= 1
        if state["player_buffs"][stat]["turns"] <= 0:
            del state["player_buffs"][stat]

    state["turn"] += 1
    state["log"] = state["log"][-5:]
    return state


def _tick_status(statuses: dict, name: str) -> None:
    if name in statuses:
        statuses[name]["turns"] -= 1
        if statuses[name]["turns"] <= 0:
            del statuses[name]


def _draw_card(state: dict) -> str | None:
    """Draw 1 card from deck into hand. Reshuffles discard if deck empty."""
    if not state["deck"]:
        if not state["discard"]:
            return None
        state["deck"] = state["discard"].copy()
        random.shuffle(state["deck"])
        state["discard"] = []

    if state["deck"]:
        card_id = state["deck"].pop(0)
        state["hand"].append(card_id)
        return card_id
    return None


# ---------------------------------------------------------------------------
# Win / loss check
# ---------------------------------------------------------------------------

def check_battle_outcome(state: dict) -> str:
    """Returns 'win', 'lose', or 'continue'."""
    if state["enemy_hp"] <= 0:
        return "win"
    if state["player_hp"] <= 0:
        return "lose"
    return "continue"


# ---------------------------------------------------------------------------
# Reward generation
# ---------------------------------------------------------------------------

def generate_drops(enemy_id: str, player_lck: int = 1) -> dict:
    """Generate loot from a defeated enemy."""
    enemy = get_enemy(enemy_id)
    if not enemy:
        return {"zet": 0, "cards": [], "items": []}

    result: dict[str, Any] = {"zet": 0, "cards": [], "items": []}

    # Zet
    zet_range = enemy.get("zet_range", (0, 0))
    if zet_range[1] > 0:
        result["zet"] = random.randint(*zet_range)

    # LCK bonus: +1% drop chance per LCK point
    lck_bonus = player_lck * 0.01

    for drop in enemy.get("drop_table", []):
        chance = drop.get("chance", 0) + lck_bonus
        if random.random() < min(1.0, chance):
            if drop["type"] == "card":
                # Pick a random card of the given rarity
                rarity = drop.get("rarity", "common")
                available = [c for c in CARDS.values() if c.get("rarity") == rarity]
                if available:
                    picked = random.choice(available)
                    result["cards"].append(picked["id"])
            elif drop["type"] == "item":
                result["items"].append(drop["item_id"])

    return result


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def hp_bar(current: int, maximum: int, width: int = 10) -> str:
    if maximum <= 0:
        return "░" * width
    filled = max(0, min(width, round(width * current / maximum)))
    return "█" * filled + "░" * (width - filled)


def energy_pips(current: int, maximum: int) -> str:
    return "⚡" * current + "○" * (maximum - current)


def status_summary(statuses: dict) -> str:
    if not statuses:
        return "None"
    parts = []
    for name, info in statuses.items():
        parts.append(f"{name.title()} ({info['turns']}t)")
    return ", ".join(parts)