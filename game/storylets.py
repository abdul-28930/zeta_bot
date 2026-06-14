"""
game/storylets.py

Checks whether any storylet should fire for a given player/zone/npc context.
Called from WalkButton and _send_dialogue_message in views.py.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from game.data import STORYLETS


async def check_storylet_trigger(
    user_id: int,
    zone_id: str | None = None,
    npc_id: str | None = None,
    session: AsyncSession = None,
) -> dict | None:
    """
    Return the first storylet that should fire for this player in this context.
    Returns None if no storylet is ready.

    Checks:
      - required flag(s) set
      - optional zone_id match
      - optional npc_id match
      - optional relationship_min threshold
      - storylet not already completed or in progress
    """
    from game.world import get_flag
    from core.models import PlayerStoryletProgress, NPCRelationship

    completed = await _get_completed_storylets(user_id, session)

    for storylet_id, storylet in STORYLETS.items():
        if storylet_id in completed:
            continue

        trigger = storylet.get("trigger", {})

        # Zone match (if trigger has zone_id requirement)
        if trigger.get("zone_id") and zone_id != trigger["zone_id"]:
            continue

        # NPC match (if trigger has npc_id requirement)
        if trigger.get("npc_id") and npc_id != trigger.get("npc_id"):
            continue

        # Primary flag check
        primary_flag = trigger.get("flag")
        if primary_flag:
            val = await get_flag(user_id, primary_flag, session)
            if not val:
                continue

        # Secondary flag check (AND logic)
        secondary_flag = trigger.get("flag_2")
        if secondary_flag:
            val2 = await get_flag(user_id, secondary_flag, session)
            if not val2:
                continue

        # Relationship minimum
        rel_min = trigger.get("relationship_min")
        if rel_min and npc_id:
            result = await session.execute(
                select(NPCRelationship).where(
                    NPCRelationship.user_id == user_id,
                    NPCRelationship.npc_id == npc_id,
                )
            )
            rel = result.scalar_one_or_none()
            if not rel or (rel.relationship_score or 0) < rel_min:
                continue

        # All conditions met
        return storylet

    return None


async def _get_completed_storylets(user_id: int, session: AsyncSession) -> set[str]:
    from core.models import PlayerStoryletProgress
    result = await session.execute(
        select(PlayerStoryletProgress.storylet_id).where(
            PlayerStoryletProgress.user_id == user_id,
            PlayerStoryletProgress.status == "completed",
        )
    )
    return {row[0] for row in result.fetchall()}


async def complete_storylet(
    user_id: int,
    storylet_id: str,
    choice_id: str,
    session: AsyncSession,
) -> dict:
    """
    Record a storylet completion and apply all outcome effects.
    Returns the outcome dict.
    """
    from datetime import datetime, timezone
    from core.models import PlayerStoryletProgress
    from game.world import add_xp, add_zet, add_item, set_flag

    storylet = STORYLETS.get(storylet_id)
    if not storylet:
        return {}

    outcome = storylet.get("outcomes", {}).get(choice_id, {})

    # Record completion
    session.add(PlayerStoryletProgress(
        user_id=user_id,
        storylet_id=storylet_id,
        status="completed",
        choice_made=choice_id,
        completed_at=datetime.now(timezone.utc),
    ))

    # Apply effects
    if outcome.get("flag_set"):
        await set_flag(user_id, outcome["flag_set"], "true", session)
    if outcome.get("flag_set_2"):
        await set_flag(user_id, outcome["flag_set_2"], "true", session)
    if outcome.get("xp"):
        await add_xp(user_id, outcome["xp"], session)
    if outcome.get("zet"):
        await add_zet(user_id, outcome["zet"], session)
    if outcome.get("item_reward"):
        await add_item(user_id, outcome["item_reward"], 1, session)

    return outcome