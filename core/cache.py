import json
from datetime import datetime, timezone
from typing import Any

import redis.asyncio as aioredis

from config import settings

_redis: aioredis.Redis | None = None


async def init_redis() -> aioredis.Redis:
    global _redis
    _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def get_redis() -> aioredis.Redis:
    if _redis is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return _redis


# ---------------------------------------------------------------------------
# Embed / game session state
# ---------------------------------------------------------------------------

async def get_embed_state(user_id: int) -> dict | None:
    r = get_redis()
    raw = await r.get(f"embed_state:{user_id}")
    return json.loads(raw) if raw else None


async def set_embed_state(user_id: int, state: dict, ttl: int = 86400) -> None:
    r = get_redis()
    await r.set(f"embed_state:{user_id}", json.dumps(state), ex=ttl)


async def clear_embed_state(user_id: int) -> None:
    r = get_redis()
    await r.delete(f"embed_state:{user_id}")


# ---------------------------------------------------------------------------
# Battle state
# ---------------------------------------------------------------------------

async def get_battle_state(user_id: int) -> dict | None:
    r = get_redis()
    raw = await r.get(f"battle:{user_id}")
    return json.loads(raw) if raw else None


async def set_battle_state(user_id: int, state: dict, ttl: int = 3600) -> None:
    r = get_redis()
    await r.set(f"battle:{user_id}", json.dumps(state), ex=ttl)


async def clear_battle_state(user_id: int) -> None:
    r = get_redis()
    await r.delete(f"battle:{user_id}")


# ---------------------------------------------------------------------------
# Character creation flow
# ---------------------------------------------------------------------------

async def get_char_creation(user_id: int) -> dict | None:
    r = get_redis()
    raw = await r.get(f"char_create:{user_id}")
    return json.loads(raw) if raw else None


async def set_char_creation(user_id: int, data: dict, ttl: int = 600) -> None:
    r = get_redis()
    await r.set(f"char_create:{user_id}", json.dumps(data), ex=ttl)


async def clear_char_creation(user_id: int) -> None:
    r = get_redis()
    await r.delete(f"char_create:{user_id}")


# ---------------------------------------------------------------------------
# Zone player presence
# ---------------------------------------------------------------------------

async def add_to_zone(user_id: int, zone_id: str, character_name: str) -> None:
    r = get_redis()
    key = f"zone_players:{zone_id}"
    await r.hset(key, str(user_id), character_name)
    await r.expire(key, 600)


async def remove_from_zone(user_id: int, zone_id: str) -> None:
    r = get_redis()
    await r.hdel(f"zone_players:{zone_id}", str(user_id))


async def get_zone_players(zone_id: str) -> dict[str, str]:
    r = get_redis()
    return await r.hgetall(f"zone_players:{zone_id}")


# ---------------------------------------------------------------------------
# Generic flag cache
# ---------------------------------------------------------------------------

async def cache_set(key: str, value: Any, ttl: int = 300) -> None:
    r = get_redis()
    await r.set(key, json.dumps(value), ex=ttl)


async def cache_get(key: str) -> Any | None:
    r = get_redis()
    raw = await r.get(key)
    return json.loads(raw) if raw else None


# ---------------------------------------------------------------------------
# Walk / Step counter
# ---------------------------------------------------------------------------

async def get_step_count(user_id: int, zone_id: str) -> int:
    """Get today's step count for a user in a zone."""
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    r = get_redis()
    val = await r.get(f"steps:{user_id}:{zone_id}:{today}")
    return int(val) if val else 0


async def increment_step(user_id: int, zone_id: str) -> int:
    """Increment step count. Returns new total."""
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    r = get_redis()
    key = f"steps:{user_id}:{zone_id}:{today}"
    count = await r.incr(key)
    await r.expire(key, 86400)
    return count


async def get_total_steps(user_id: int, zone_id: str) -> int:
    """Get all-time total steps in a zone (for mastery)."""
    r = get_redis()
    val = await r.get(f"total_steps:{user_id}:{zone_id}")
    return int(val) if val else 0


async def increment_total_steps(user_id: int, zone_id: str) -> int:
    """Increment all-time step count. Returns new total."""
    r = get_redis()
    key = f"total_steps:{user_id}:{zone_id}"
    count = await r.incr(key)
    return count


async def get_walk_state(user_id: int) -> dict | None:
    r = get_redis()
    raw = await r.get(f"walk_state:{user_id}")
    return json.loads(raw) if raw else None


async def set_walk_state(user_id: int, state: dict, ttl: int = 3600) -> None:
    r = get_redis()
    await r.set(f"walk_state:{user_id}", json.dumps(state), ex=ttl)


async def clear_walk_state(user_id: int) -> None:
    r = get_redis()
    await r.delete(f"walk_state:{user_id}")


# ---------------------------------------------------------------------------
# Zone mastery milestone tracker
# ---------------------------------------------------------------------------

async def check_mastery_milestone(user_id: int, zone_id: str, total_steps: int) -> int | None:
    """
    Check if player just crossed a mastery milestone.
    Returns the milestone step threshold (int) or None if no milestone hit.
    Milestones: 100 / 500 / 1000 / 5000 total steps.
    Uses >= check so missed steps (lag, disconnect) never skip a milestone.
    """
    from game.walk_data import MASTERY_STEPS
    r = get_redis()
    for threshold in MASTERY_STEPS:
        if total_steps >= threshold:
            key = f"mastery:{user_id}:{zone_id}:{threshold}"
            # Only fire once per milestone — set NX (only if not exists)
            claimed = await r.set(key, "1", nx=True)
            if claimed:
                return threshold   # just crossed this one
    return None


# ---------------------------------------------------------------------------
# No-repeat shuffle bag for walk content
# ---------------------------------------------------------------------------

async def get_seen_indices(user_id: int, zone_id: str, content_type: str) -> set[int]:
    """Return set of already-seen pool indices for this content type."""
    r   = get_redis()
    key = f"seen:{user_id}:{zone_id}:{content_type}"
    raw = await r.get(key)
    if not raw:
        return set()
    return set(json.loads(raw))


async def mark_seen(
    user_id: int, zone_id: str, content_type: str,
    idx: int, pool_size: int,
) -> None:
    """
    Mark an index as seen. When all indices have been seen,
    reset the bag so the pool cycles again (with reshuffled order).
    TTL: 24 hours so bags reset daily naturally.
    """
    r   = get_redis()
    key = f"seen:{user_id}:{zone_id}:{content_type}"
    raw = await r.get(key)
    seen: set[int] = set(json.loads(raw)) if raw else set()
    seen.add(idx)
    # Full cycle complete — reset the bag
    if len(seen) >= pool_size:
        seen = set()
    await r.set(key, json.dumps(list(seen)), ex=86400)


# ---------------------------------------------------------------------------
# Enemy respawn timer  (Phase 3)
# ---------------------------------------------------------------------------
#
# Per-player, per-zone. After ZONE_CLEAR_KILL_THRESHOLD kills in a zone,
# encounters are suppressed for ZONE_CLEAR_TTL seconds (30 min).
# The kill counter uses a short rolling window so it resets naturally.
# ---------------------------------------------------------------------------

ZONE_CLEAR_KILL_THRESHOLD = 3       # kills before zone goes quiet
ZONE_CLEAR_TTL            = 1800    # 30 minutes in seconds
ZONE_KILL_WINDOW          = 3600    # kill counter window (1 hour)


async def get_zone_kill_count(user_id: int, zone_id: str) -> int:
    """How many enemies this player has killed in this zone recently."""
    r = get_redis()
    val = await r.get(f"zone_kills:{user_id}:{zone_id}")
    return int(val) if val else 0


async def increment_zone_kills(user_id: int, zone_id: str) -> int:
    """
    Record an enemy kill. Returns the new kill count.
    Automatically sets zone_cleared flag when threshold is reached.
    """
    r   = get_redis()
    key = f"zone_kills:{user_id}:{zone_id}"
    count = await r.incr(key)
    await r.expire(key, ZONE_KILL_WINDOW)

    if count >= ZONE_CLEAR_KILL_THRESHOLD:
        # Mark zone as cleared — suppress encounters for 30 min
        cleared_key = f"zone_cleared:{user_id}:{zone_id}"
        await r.set(cleared_key, "1", ex=ZONE_CLEAR_TTL)
        # Reset kill counter so it can accumulate again after respawn
        await r.delete(key)

    return count


async def is_zone_cleared(user_id: int, zone_id: str) -> bool:
    """True if this player has cleared this zone and enemies haven't respawned yet."""
    r = get_redis()
    return bool(await r.get(f"zone_cleared:{user_id}:{zone_id}"))


async def get_zone_respawn_seconds(user_id: int, zone_id: str) -> int:
    """
    Seconds until enemies respawn for this player in this zone.
    Returns 0 if zone is not cleared.
    """
    r   = get_redis()
    ttl = await r.ttl(f"zone_cleared:{user_id}:{zone_id}")
    return max(0, ttl)


# ---------------------------------------------------------------------------
# Mini-boss state  (Phase 3)
# ---------------------------------------------------------------------------
#
# Global per-zone. One mini-boss per zone, shared across all players.
# After defeat: 6-hour cooldown before it respawns.
# State stored as JSON: {alive, defeated_at, defeated_by}
# ---------------------------------------------------------------------------

MINIBOSS_RESPAWN_TTL = 21600   # 6 hours in seconds


async def get_miniboss_state(zone_id: str) -> dict | None:
    """
    Returns mini-boss state dict or None if no record exists yet.
    Dict shape: {alive: bool, defeated_at: str|None, defeated_by: str|None}
    None means the mini-boss has never been defeated — treat as alive.
    """
    r   = get_redis()
    raw = await r.get(f"miniboss:{zone_id}")
    return json.loads(raw) if raw else None


async def is_miniboss_alive(zone_id: str) -> bool:
    """True if the mini-boss is currently spawned and available to fight."""
    state = await get_miniboss_state(zone_id)
    if state is None:
        return True   # never defeated → alive
    return state.get("alive", True)


async def set_miniboss_defeated(zone_id: str, defeated_by: str) -> None:
    """
    Record a mini-boss defeat. Starts the 6-hour respawn timer.
    After the TTL expires the key is gone → treated as alive again.
    """
    r     = get_redis()
    state = {
        "alive":       False,
        "defeated_at": datetime.now(timezone.utc).isoformat(),
        "defeated_by": defeated_by,
    }
    await r.set(f"miniboss:{zone_id}", json.dumps(state), ex=MINIBOSS_RESPAWN_TTL)


async def get_miniboss_respawn_seconds(zone_id: str) -> int:
    """
    Seconds until the mini-boss respawns.
    Returns 0 if it's already alive (or has never been defeated).
    """
    r   = get_redis()
    ttl = await r.ttl(f"miniboss:{zone_id}")
    return max(0, ttl)


async def get_miniboss_defeated_by(zone_id: str) -> str | None:
    """Returns the character name that last killed this mini-boss, or None."""
    state = await get_miniboss_state(zone_id)
    if not state:
        return None
    return state.get("defeated_by")


# ---------------------------------------------------------------------------
# Ancient Vault cooldown
# Per-player, 6-hour TTL. Key disappears when loot resets.
# ---------------------------------------------------------------------------

VAULT_COOLDOWN_TTL = 21600   # 6 hours in seconds


async def is_vault_on_cooldown(user_id: int) -> bool:
    """True if this player has already looted the vault and it hasn't reset yet."""
    r = get_redis()
    return bool(await r.get(f"vault_cooldown:{user_id}"))


async def set_vault_cooldown(user_id: int) -> None:
    """Start the 6-hour cooldown after a player loots the vault."""
    r = get_redis()
    await r.set(f"vault_cooldown:{user_id}", "1", ex=VAULT_COOLDOWN_TTL)


async def get_vault_cooldown_seconds(user_id: int) -> int:
    """Seconds until the vault resets for this player. Returns 0 if not on cooldown."""
    r   = get_redis()
    ttl = await r.ttl(f"vault_cooldown:{user_id}")
    return max(0, ttl)