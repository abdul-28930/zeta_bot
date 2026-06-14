"""
game/guild.py — Adventurer's Guild
Place in: game/guild.py

Handles:
  - Daily contract generation (3 per day: bronze/silver/gold)
  - Contract acceptance + progress tracking
  - Contract completion + rewards
  - Weekly leaderboard
"""
import random
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

CONTRACTS_PER_DAY = 3   # bronze, silver, gold
MAX_ACTIVE        = 3   # player can hold 3 active contracts

TIER_CONFIG = {
    "bronze": {"xp": 30,  "zet": 20,  "emoji": "🥉"},
    "silver": {"xp": 80,  "zet": 60,  "emoji": "🥈"},
    "gold":   {"xp": 200, "zet": 150, "emoji": "🥇"},
}

CONTRACT_TEMPLATES = {
    "walk_steps": [
        ("bronze", 20,  "Walk {n} steps anywhere in Ironhaven."),
        ("silver", 50,  "Walk {n} steps exploring the city."),
        ("gold",   100, "Walk {n} steps across Ironhaven."),
    ],
    "kill_enemies": [
        ("bronze", 3,  "Defeat {n} enemies anywhere."),
        ("silver", 8,  "Defeat {n} enemies in low or null security zones."),
        ("gold",   15, "Defeat {n} enemies — prove your combat worth."),
    ],
    "visit_zones": [
        ("bronze", 2, "Travel to {n} different zones today."),
        ("silver", 4, "Explore {n} different parts of Ironhaven."),
        ("gold",   6, "Chart {n} distinct zones in one day."),
    ],
    "talk_npcs": [
        ("bronze", 2, "Have conversations with {n} different NPCs."),
        ("silver", 4, "Build relationships — talk to {n} people today."),
        ("gold",   6, "Speak with {n} different people in the city."),
    ],
}


def _today_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


async def get_daily_contracts(session: AsyncSession) -> list:
    """
    Get today's guild contracts, generating them if they don't exist yet.
    """
    from core.models import GuildContract
    day = _today_key()
    result = await session.execute(
        select(GuildContract).where(GuildContract.day_key == day)
    )
    contracts = result.scalars().all()
    if contracts:
        return contracts
    return await _generate_daily_contracts(day, session)


async def _generate_daily_contracts(day: str, session: AsyncSession) -> list:
    """Generate one contract per tier for today."""
    from core.models import GuildContract
    tiers     = ["bronze", "silver", "gold"]
    contract_types = list(CONTRACT_TEMPLATES.keys())
    random.shuffle(contract_types)
    generated = []
    for i, tier in enumerate(tiers):
        ctype    = contract_types[i % len(contract_types)]
        template = next(t for t in CONTRACT_TEMPLATES[ctype] if t[0] == tier)
        _, count, desc_template = template
        cfg     = TIER_CONFIG[tier]
        contract = GuildContract(
            day_key       = day,
            tier          = tier,
            contract_type = ctype,
            target_id     = None,
            target_count  = count,
            description   = desc_template.format(n=count),
            reward_xp     = cfg["xp"],
            reward_zet    = cfg["zet"],
        )
        session.add(contract)
        generated.append(contract)
    await session.flush()
    return generated


async def get_player_contracts(user_id: int, session: AsyncSession, day: str | None = None) -> list:
    """Get player's active contracts for today."""
    from core.models import PlayerGuildContract, GuildContract
    day = day or _today_key()
    result = await session.execute(
        select(PlayerGuildContract, GuildContract)
        .join(GuildContract, PlayerGuildContract.contract_id == GuildContract.id)
        .where(
            PlayerGuildContract.user_id  == user_id,
            PlayerGuildContract.status.in_(["active", "completed"]),
            GuildContract.day_key        == day,
        )
    )
    return result.all()


async def accept_contract(user_id: int, contract_id: int, session: AsyncSession) -> tuple[bool, str]:
    """Accept a guild contract. Player can hold up to MAX_ACTIVE."""
    from core.models import PlayerGuildContract, GuildContract

    # Check active count
    active = await get_player_contracts(user_id, session)
    if len(active) >= MAX_ACTIVE:
        return False, f"You already have {MAX_ACTIVE} active contracts. Complete or wait for them to expire."

    # Check not already accepted
    already = next(
        (row for row, _ in active if row.contract_id == contract_id), None
    )
    if already:
        return False, "You already have this contract."

    contract = await session.get(GuildContract, contract_id)
    if not contract:
        return False, "Contract not found."

    if contract.day_key != _today_key():
        return False, "This contract has expired — new contracts are available."

    session.add(PlayerGuildContract(
        user_id=user_id, contract_id=contract_id, progress=0, status="active"
    ))
    return True, f"Contract accepted: *{contract.description}*"


async def record_contract_progress(
    user_id: int,
    contract_type: str,
    amount: int,
    session: AsyncSession,
) -> list[str]:
    """
    Called whenever the player does something that might progress a contract.
    Returns list of completion messages if any contracts just finished.
    """
    from core.models import PlayerGuildContract, GuildContract

    active = await get_player_contracts(user_id, session)
    completed_msgs = []

    for player_contract, guild_contract in active:
        if player_contract.status != "active":
            continue
        if guild_contract.contract_type != contract_type:
            continue
        player_contract.progress = min(
            guild_contract.target_count,
            player_contract.progress + amount
        )
        if player_contract.progress >= guild_contract.target_count:
            player_contract.status = "completed"
            tier  = TIER_CONFIG[guild_contract.tier]
            completed_msgs.append(
                f"{tier['emoji']} Contract complete: **{guild_contract.description}** "
                f"— Claim at the Adventurer's Guild!"
            )

    return completed_msgs


async def claim_contract(user_id: int, contract_id: int, session: AsyncSession) -> tuple[bool, str, dict]:
    """
    Claim rewards for a completed contract.
    Returns (success, message, rewards_dict).
    """
    from core.models import PlayerGuildContract, GuildContract
    from game.world import add_xp, add_zet

    result = await session.execute(
        select(PlayerGuildContract, GuildContract)
        .join(GuildContract, PlayerGuildContract.contract_id == GuildContract.id)
        .where(
            PlayerGuildContract.user_id     == user_id,
            PlayerGuildContract.contract_id == contract_id,
        )
    )
    row = result.first()
    if not row:
        return False, "Contract not found.", {}

    player_contract, guild_contract = row

    if player_contract.status == "claimed":
        return False, "Already claimed.", {}
    if player_contract.status != "completed":
        progress = player_contract.progress
        return False, f"Not finished yet. ({progress}/{guild_contract.target_count})", {}

    # Award rewards
    xp_result = await add_xp(user_id, guild_contract.reward_xp, session)
    await add_zet(user_id, guild_contract.reward_zet, session)

    player_contract.status     = "claimed"
    player_contract.claimed_at = datetime.now(timezone.utc)

    tier    = TIER_CONFIG[guild_contract.tier]
    rewards = {"xp": guild_contract.reward_xp, "zet": guild_contract.reward_zet}
    msg = (
        f"{tier['emoji']} Contract claimed!\n"
        f"⭐ +{guild_contract.reward_xp} XP  ·  💰 +{guild_contract.reward_zet} Ƶ"
    )
    if xp_result.get("leveled_up"):
        msg += f"\n🎊 Level up! You're now level {xp_result['new_level']}!"
    return True, msg, rewards


async def get_leaderboard(session: AsyncSession, limit: int = 10) -> list:
    """Top players by total XP (global leaderboard)."""
    from core.models import Player, PlayerProgression
    result = await session.execute(
        select(Player.character_name, PlayerProgression.level, PlayerProgression.xp)
        .join(PlayerProgression, Player.user_id == PlayerProgression.user_id)
        .order_by(PlayerProgression.level.desc(), PlayerProgression.xp.desc())
        .limit(limit)
    )
    return result.all()