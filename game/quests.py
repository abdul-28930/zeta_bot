"""
Quest Engine — Zeta

Handles all quest logic:
- Offering quests based on relationship score
- Tracking progress (zone visits, NPC interactions)
- Completing quests and distributing rewards
- Advancing quest chains
"""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from game.quest_chains import QUEST_CHAINS


# ---------------------------------------------------------------------------
# Quest state helpers
# ---------------------------------------------------------------------------

async def get_quest(
    user_id: int,
    quest_id: str,
    session: AsyncSession,
):
    """Get a PlayerQuest row, or None."""
    from core.models import PlayerQuest
    result = await session.execute(
        select(PlayerQuest).where(
            PlayerQuest.user_id == user_id,
            PlayerQuest.quest_id == quest_id,
        )
    )
    return result.scalar_one_or_none()


async def get_active_quest_for_npc(
    user_id: int,
    npc_id: str,
    session: AsyncSession,
):
    """Return the player's current active quest from this NPC, or None."""
    from core.models import PlayerQuest
    result = await session.execute(
        select(PlayerQuest).where(
            PlayerQuest.user_id == user_id,
            PlayerQuest.npc_id == npc_id,
            PlayerQuest.status == "active",
        )
    )
    return result.scalar_one_or_none()


async def get_completed_quest_ids(
    user_id: int,
    npc_id: str,
    session: AsyncSession,
) -> set[str]:
    """Return set of completed quest IDs for this NPC."""
    from core.models import PlayerQuest
    result = await session.execute(
        select(PlayerQuest.quest_id).where(
            PlayerQuest.user_id == user_id,
            PlayerQuest.npc_id == npc_id,
            PlayerQuest.status == "completed",
        )
    )
    return {row[0] for row in result.fetchall()}


# ---------------------------------------------------------------------------
# Offering logic
# ---------------------------------------------------------------------------

async def get_available_quest(
    user_id: int,
    npc_id: str,
    relationship_score: int,
    session: AsyncSession,
) -> dict | None:
    """
    Return the next quest in the chain this player can receive, or None.

    Logic:
    1. Get all completed quest IDs for this NPC
    2. Check for any in-progress quest (offered OR active) — don't re-offer
    3. Walk the chain and return the first unlocked quest
    """
    from core.models import PlayerQuest
    from sqlalchemy import select as sa_select

    chain = QUEST_CHAINS.get(npc_id, [])
    if not chain:
        return None

    completed_ids = await get_completed_quest_ids(user_id, npc_id, session)

    # Check for ANY quest that is offered or active (not completed)
    # This prevents the same quest being offered repeatedly if accept didn't persist
    result = await session.execute(
        sa_select(PlayerQuest).where(
            PlayerQuest.user_id == user_id,
            PlayerQuest.npc_id == npc_id,
            PlayerQuest.status.in_(["offered", "active"]),
        )
    )
    in_progress = result.scalar_one_or_none()
    in_progress_id = in_progress.quest_id if in_progress else None

    for quest in chain:
        qid = quest["id"]

        # Skip completed
        if qid in completed_ids:
            continue

        # Skip any quest already in progress (offered OR active)
        if qid == in_progress_id:
            return None

        # Check relationship requirement
        if relationship_score < quest["min_relationship"]:
            return None

        # This is the next available quest
        return quest

    return None  # All quests completed


async def offer_quest(
    user_id: int,
    quest: dict,
    session: AsyncSession,
):
    """Mark a quest as offered. If already exists, return existing row."""
    from core.models import PlayerQuest
    # Check if already exists to avoid PK conflict
    existing = await get_quest(user_id, quest["id"], session)
    if existing:
        return existing
    row = PlayerQuest(
        user_id=user_id,
        quest_id=quest["id"],
        npc_id=quest["giver_npc"],
        status="offered",
        progress={},
    )
    session.add(row)
    await session.flush()
    return row


async def accept_quest(
    user_id: int,
    quest_id: str,
    session: AsyncSession,
):
    """Player accepts a quest — moves from offered to active."""
    from core.models import PlayerQuest
    row = await get_quest(user_id, quest_id, session)
    if row:
        row.status = "active"
        row.started_at = datetime.now(timezone.utc)
        # Initialise progress tracking for zone and NPC targets
        quest_data = _find_quest(quest_id)
        if quest_data:
            progress = {}
            for zone_id in quest_data.get("zone_targets", []):
                progress[f"zone:{zone_id}"] = False
            for npc_id in quest_data.get("npc_targets", []):
                progress[f"npc:{npc_id}"] = False
            row.progress = progress
    return row


# ---------------------------------------------------------------------------
# Progress tracking
# ---------------------------------------------------------------------------

async def record_zone_visit(
    user_id: int,
    zone_id: str,
    session: AsyncSession,
) -> list[dict]:
    """
    Called when player enters a zone.
    Updates progress on any active quest that targets this zone.
    Returns list of quests that are now fully complete.
    """
    from core.models import PlayerQuest
    from sqlalchemy.orm.attributes import flag_modified

    result = await session.execute(
        select(PlayerQuest).where(
            PlayerQuest.user_id == user_id,
            PlayerQuest.status == "active",
        )
    )
    active_quests = result.scalars().all()
    ready_to_complete = []

    for quest_row in active_quests:
        key = f"zone:{zone_id}"
        if key in quest_row.progress:
            # Must use flag_modified — SQLAlchemy won't detect JSONB dict mutations
            updated = dict(quest_row.progress)
            updated[key] = True
            quest_row.progress = updated
            flag_modified(quest_row, "progress")

            if _all_objectives_met(quest_row.progress):
                ready_to_complete.append(_find_quest(quest_row.quest_id))

    return [q for q in ready_to_complete if q]


async def record_npc_interaction(
    user_id: int,
    npc_id: str,
    session: AsyncSession,
) -> list[dict]:
    """
    Called when player talks to an NPC.
    Updates progress on any active quest targeting this NPC.
    Returns list of quests now ready to complete.
    """
    from core.models import PlayerQuest
    from sqlalchemy.orm.attributes import flag_modified

    result = await session.execute(
        select(PlayerQuest).where(
            PlayerQuest.user_id == user_id,
            PlayerQuest.status == "active",
        )
    )
    active_quests = result.scalars().all()
    ready_to_complete = []

    for quest_row in active_quests:
        key = f"npc:{npc_id}"
        if key in quest_row.progress:
            updated = dict(quest_row.progress)
            updated[key] = True
            quest_row.progress = updated
            flag_modified(quest_row, "progress")

            if _all_objectives_met(quest_row.progress):
                ready_to_complete.append(_find_quest(quest_row.quest_id))

    return [q for q in ready_to_complete if q]


def _all_objectives_met(progress: dict) -> bool:
    """Return True if all tracked objectives are True.
    Empty dict means progress wasn't initialized yet — not complete."""
    if not progress:
        return False  # Empty = not set up, never auto-complete
    return all(progress.values())


# ---------------------------------------------------------------------------
# Completion
# ---------------------------------------------------------------------------

async def complete_quest(
    user_id: int,
    quest_id: str,
    session: AsyncSession,
) -> dict:
    """
    Mark quest as completed, distribute rewards.
    Returns result dict with rewards info.
    """
    from core.models import PlayerQuest
    from game.world import add_xp, add_zet

    quest_data = _find_quest(quest_id)
    if not quest_data:
        return {}

    # Update quest row
    row = await get_quest(user_id, quest_id, session)
    if row:
        row.status = "completed"
        row.completed_at = datetime.now(timezone.utc)

    # Distribute rewards
    xp_result = {}
    if quest_data.get("xp"):
        xp_result = await add_xp(user_id, quest_data["xp"], session)
        xp_result["xp_gained"] = quest_data["xp"]

    if quest_data.get("zet"):
        await add_zet(user_id, quest_data["zet"], session)

    return {
        "quest": quest_data,
        "xp_gained": quest_data.get("xp", 0),
        "zet_gained": quest_data.get("zet", 0),
        "leveled_up": xp_result.get("leveled_up", False),
        "new_level":  xp_result.get("new_level", 1),
        "relationship_gain": quest_data.get("relationship_gain", 0),
    }


async def apply_quest_relationship_gain(
    user_id: int,
    npc_id: str,
    amount: int,
    session: AsyncSession,
):
    """Add bonus relationship score from quest completion."""
    from core.models import NPCRelationship
    result = await session.execute(
        select(NPCRelationship).where(
            NPCRelationship.user_id == user_id,
            NPCRelationship.npc_id == npc_id,
        )
    )
    rel = result.scalar_one_or_none()
    if rel:
        rel.relationship_score = min(100, rel.relationship_score + amount)


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

async def get_all_active_quests(
    user_id: int,
    session: AsyncSession,
) -> list[tuple]:
    """
    Return list of (quest_data, quest_row) for all active quests.
    Used for the quest log UI.
    """
    from core.models import PlayerQuest
    result = await session.execute(
        select(PlayerQuest).where(
            PlayerQuest.user_id == user_id,
            PlayerQuest.status == "active",
        )
    )
    rows = result.scalars().all()
    out = []
    for row in rows:
        quest_data = _find_quest(row.quest_id)
        if quest_data:
            out.append((quest_data, row))
    return out


async def get_quest_log(
    user_id: int,
    session: AsyncSession,
) -> dict:
    """
    Return structured quest log for UI display.
    {
        "active": [(quest_data, quest_row), ...],
        "completed_count": int,
    }
    """
    from core.models import PlayerQuest

    active = await get_all_active_quests(user_id, session)

    completed_result = await session.execute(
        select(PlayerQuest).where(
            PlayerQuest.user_id == user_id,
            PlayerQuest.status == "completed",
        )
    )
    completed_count = len(completed_result.scalars().all())

    return {
        "active": active,
        "completed_count": completed_count,
    }


async def has_ready_to_complete(
    user_id: int,
    npc_id: str,
    session: AsyncSession,
) -> dict | None:
    """
    Check if player has a quest from this NPC that's ready to turn in
    (all objectives met, status=active).
    Returns quest_data or None.
    """
    from core.models import PlayerQuest
    result = await session.execute(
        select(PlayerQuest).where(
            PlayerQuest.user_id == user_id,
            PlayerQuest.npc_id == npc_id,
            PlayerQuest.status == "active",
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        return None

    if _all_objectives_met(row.progress):
        return _find_quest(row.quest_id)
    return None


# ---------------------------------------------------------------------------
# Internal lookup
# ---------------------------------------------------------------------------

def _find_quest(quest_id: str) -> dict | None:
    """Find quest data by ID across all NPC chains."""
    for chain in QUEST_CHAINS.values():
        for quest in chain:
            if quest["id"] == quest_id:
                return quest
    return None


def get_quest_progress_display(progress: dict, quest_data: dict) -> str:
    """
    Build a human-readable progress string for the UI.
    E.g. "✅ Port District  ·  ⬜ Maren"
    """
    if not progress:
        return "Go complete the objective and return."

    from game.data import ZONES, NPCS
    parts = []

    for key, done in progress.items():
        icon = "✅" if done else "⬜"
        if key.startswith("zone:"):
            zone_id = key[5:]
            zone = ZONES.get(zone_id, {})
            name = zone.get("name", zone_id)
            parts.append(f"{icon} Visit {name}")
        elif key.startswith("npc:"):
            npc_id = key[4:]
            npc = NPCS.get(npc_id, {})
            name = npc.get("name", npc_id)
            parts.append(f"{icon} Talk to {name}")

    return "  ·  ".join(parts) if parts else "Complete the task and return."