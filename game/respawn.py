"""
game/respawn.py

Respawn logic for enemy zones and mini-bosses.
Sits between cache.py (raw Redis) and walk.py / views.py (game flow).

Public API
----------
check_encounter_allowed   — should regular encounters fire this walk step?
record_enemy_kill         — call after every battle win; returns zone status
get_zone_status           — full respawn + mini-boss info for embed display
should_encounter_miniboss — roll for mini-boss encounter this walk step?
handle_miniboss_defeat    — call after mini-boss kill; returns announcement data
get_miniboss_for_zone     — return enemy dict if zone has a live mini-boss
"""

import random

from core.cache import (
    get_zone_respawn_seconds,
    get_miniboss_respawn_seconds,
    get_miniboss_defeated_by,
    increment_zone_kills,
    is_miniboss_alive,
    is_zone_cleared,
    set_miniboss_defeated,
)
from game.data import ENEMIES, MINI_BOSSES, get_enemy

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Chance per walk step to encounter a live mini-boss (if zone has one)
MINIBOSS_ENCOUNTER_CHANCE = 0.20   # 20% — high enough to matter, not spammy

# After mini-boss is defeated, broadcast message template
MINIBOSS_DEFEAT_MSG = "⚔️ **{name}** in *{zone}* has been defeated by **{player}**! Respawns in 6 hours."


# ---------------------------------------------------------------------------
# Regular encounter gating
# ---------------------------------------------------------------------------

async def check_encounter_allowed(user_id: int, zone_id: str) -> bool:
    """
    Return True if regular enemy encounters are allowed for this player
    in this zone right now.

    Encounters are suppressed when the player has cleared the zone
    (killed ZONE_CLEAR_KILL_THRESHOLD enemies within the rolling window).
    """
    cleared = await is_zone_cleared(user_id, zone_id)
    return not cleared


async def record_enemy_kill(user_id: int, zone_id: str) -> dict:
    """
    Record a regular enemy kill for this player in this zone.
    Call this from _handle_battle_win in views.py.

    Returns a status dict:
    {
        kills:        int   — current kill count (0 if zone just cleared)
        zone_cleared: bool  — True if this kill tipped the zone into cleared state
        respawn_secs: int   — seconds until respawn (0 if not cleared)
    }
    """
    new_count = await increment_zone_kills(user_id, zone_id)

    # increment_zone_kills resets the counter to 0 when threshold is hit
    # so new_count == 0 means the zone WAS just cleared this kill
    zone_just_cleared = new_count == 0

    respawn_secs = 0
    if zone_just_cleared:
        respawn_secs = await get_zone_respawn_seconds(user_id, zone_id)

    return {
        "kills":        new_count,
        "zone_cleared": zone_just_cleared,
        "respawn_secs": respawn_secs,
    }


# ---------------------------------------------------------------------------
# Mini-boss encounter
# ---------------------------------------------------------------------------

async def get_miniboss_for_zone(zone_id: str) -> dict | None:
    """
    Return the mini-boss enemy dict if the zone has one AND it's currently alive.
    Returns None if zone has no mini-boss or it's on cooldown.
    """
    enemy_id = MINI_BOSSES.get(zone_id)
    if not enemy_id:
        return None
    alive = await is_miniboss_alive(zone_id)
    if not alive:
        return None
    return get_enemy(enemy_id)


async def should_encounter_miniboss(zone_id: str) -> bool:
    """
    Roll for a mini-boss encounter this walk step.
    Returns True only if the zone has a live mini-boss AND the RNG fires.

    Called from WalkButton before the regular encounter roll so mini-boss
    encounters are always exclusive — never alongside a regular enemy.
    """
    enemy_id = MINI_BOSSES.get(zone_id)
    if not enemy_id:
        return False
    alive = await is_miniboss_alive(zone_id)
    if not alive:
        return False
    return random.random() < MINIBOSS_ENCOUNTER_CHANCE


async def handle_miniboss_defeat(
    zone_id: str,
    character_name: str,
) -> dict:
    """
    Record a mini-boss defeat and prepare the server announcement.
    Call this from _handle_battle_win when enemy_id is a mini-boss.

    Returns:
    {
        announce:      str  — formatted announcement string
        respawn_secs:  int  — 6 hours in seconds
        enemy_name:    str  — mini-boss display name
        zone_name:     str  — zone display name
    }
    """
    from game.data import ZONES
    await set_miniboss_defeated(zone_id, character_name)

    enemy_id  = MINI_BOSSES.get(zone_id, "")
    enemy     = ENEMIES.get(enemy_id, {})
    zone_data = ZONES.get(zone_id, {})

    enemy_name = enemy.get("name", "Mini-boss")
    zone_name  = zone_data.get("name", zone_id.replace("_", " ").title())

    announce = MINIBOSS_DEFEAT_MSG.format(
        name=enemy_name,
        zone=zone_name,
        player=character_name,
    )

    return {
        "announce":     announce,
        "respawn_secs": 21600,
        "enemy_name":   enemy_name,
        "zone_name":    zone_name,
    }


# ---------------------------------------------------------------------------
# Zone status — used by zone_embed and walk_embed
# ---------------------------------------------------------------------------

async def get_zone_status(user_id: int, zone_id: str) -> dict:
    """
    Return a combined status dict for a zone, used by the embed layer
    to show respawn countdowns and mini-boss availability.

    Shape:
    {
        enemy_cleared:      bool
        enemy_respawn_secs: int   (0 if not cleared)
        miniboss_id:        str | None
        miniboss_alive:     bool
        miniboss_respawn_secs: int  (0 if alive)
        miniboss_defeated_by:  str | None
    }
    """
    cleared      = await is_zone_cleared(user_id, zone_id)
    respawn_secs = await get_zone_respawn_seconds(user_id, zone_id) if cleared else 0

    miniboss_id   = MINI_BOSSES.get(zone_id)
    mb_alive      = False
    mb_respawn    = 0
    mb_defeated   = None

    if miniboss_id:
        mb_alive    = await is_miniboss_alive(zone_id)
        mb_respawn  = 0 if mb_alive else await get_miniboss_respawn_seconds(zone_id)
        mb_defeated = await get_miniboss_defeated_by(zone_id)

    return {
        "enemy_cleared":          cleared,
        "enemy_respawn_secs":     respawn_secs,
        "miniboss_id":            miniboss_id,
        "miniboss_alive":         mb_alive,
        "miniboss_respawn_secs":  mb_respawn,
        "miniboss_defeated_by":   mb_defeated,
    }


# ---------------------------------------------------------------------------
# Formatting helpers  (used by embeds.py)
# ---------------------------------------------------------------------------

def format_respawn_time(seconds: int) -> str:
    """Convert seconds into a human-readable countdown string."""
    if seconds <= 0:
        return "now"
    minutes = seconds // 60
    hours   = minutes // 60
    if hours > 0:
        remaining_minutes = minutes % 60
        if remaining_minutes:
            return f"{hours}h {remaining_minutes}m"
        return f"{hours}h"
    return f"{minutes}m"