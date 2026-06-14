"""
GameCog — main /zeta slash command.

The entire game runs through one persistent Discord message.
This cog handles entry-point logic; Views handle all button interactions.
"""
import discord
from discord import app_commands
from discord.ext import commands

from core.cache import clear_battle_state, get_battle_state
from core.database import get_session
from game.data import STORYLETS, get_zone
from game.world import get_flag, get_full_player, get_or_create_relationship, set_flag
from ui.embeds import char_creation_race_embed, error_embed, storylet_embed, zone_embed
from ui.views import (
    MainZoneView,
    RaceSelectView,
    StoryletView,
)


class GameCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # -------------------------------------------------------------------------
    # /zeta — main entry point
    # -------------------------------------------------------------------------

    @app_commands.command(name="zeta", description="Open your Zeta RPG game.")
    async def zeta(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id

        async with get_session() as session:
            player = await get_full_player(user_id, session)

            # New player — start character creation
            if player is None or not player.char_created:
                embed = char_creation_race_embed()
                view = RaceSelectView(user_id)
                await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
                return

            # Existing player — show current zone + check for storylet triggers
            zone_id = player.progression.current_zone_id
            zone = get_zone(zone_id)

            # Check if a storylet should trigger
            storylet = await _check_storylet_triggers(user_id, zone_id, session)

            if storylet:
                embed = storylet_embed(storylet)
                view = StoryletView(user_id, storylet)
                await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
                return

            # Normal zone view
            embed = zone_embed(player, zone)
            view = MainZoneView(user_id)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=False)

    # -------------------------------------------------------------------------
    # /zeta_battle — check active battle (admin/debug)
    # -------------------------------------------------------------------------

    @app_commands.command(name="zeta_resetbattle", description="Reset your active battle if you're stuck.")
    async def reset_battle(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id
        state = await get_battle_state(user_id)
        if state:
            await clear_battle_state(user_id)
            await interaction.response.send_message("⚠️ Battle cleared. Run `/zeta` to return to the game.", ephemeral=True)
        else:
            await interaction.response.send_message("No active battle found.", ephemeral=True)

    # -------------------------------------------------------------------------
    # /zeta_heal — restore HP at inn (convenience command)
    # -------------------------------------------------------------------------

    @app_commands.command(name="zeta_rest", description="Rest at the inn to restore HP. Costs 20 Ƶ.")
    async def rest(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id
        async with get_session() as session:
            player = await get_full_player(user_id, session)
            if not player or not player.char_created:
                return await interaction.response.send_message("You don't have a character yet. Use `/zeta`.", ephemeral=True)

            # Must be in town_square to rest at the inn
            if player.progression.current_zone_id not in ("town_square", "residential_ward"):
                return await interaction.response.send_message("You must be in Town Square or the Residential Ward to rest.", ephemeral=True)

            from game.world import deduct_zet, full_heal_player
            success = await deduct_zet(user_id, 20, session)
            if not success:
                return await interaction.response.send_message("You need 20 Ƶ to rest at the inn.", ephemeral=True)

            await full_heal_player(user_id, session)
            player = await get_full_player(user_id, session)

        max_hp = player.stats.vit * 5
        await interaction.response.send_message(
            f"🛏️ You rest at the inn. HP fully restored ({max_hp}/{max_hp}). Cost: 20 Ƶ.",
            ephemeral=True,
        )


# ---------------------------------------------------------------------------
# Storylet trigger checker
# ---------------------------------------------------------------------------

async def _check_storylet_triggers(user_id: int, zone_id: str, session) -> dict | None:
    """Return a storylet dict if any should trigger for this player right now."""
    for storylet in STORYLETS.values():
        # Check zone match
        if storylet.get("zone_id") != zone_id:
            continue

        # Check if already completed
        completed = await get_flag(user_id, f"storylet_{storylet['id']}_done", session)
        if completed:
            continue

        # Check trigger conditions
        trigger = storylet.get("trigger", {})
        triggered = False

        if "flag" in trigger:
            val = await get_flag(user_id, trigger["flag"], session)
            if val:
                triggered = True

        if "or_flag" in trigger and not triggered:
            val = await get_flag(user_id, trigger["or_flag"], session)
            if val:
                triggered = True

        if "npc_id" in trigger and "visit_count" in trigger:
            from core.models import NPCRelationship
            from sqlalchemy import select
            result = await session.execute(
                select(NPCRelationship).where(
                    NPCRelationship.user_id == user_id,
                    NPCRelationship.npc_id == trigger["npc_id"],
                )
            )
            rel = result.scalar_one_or_none()
            if rel and rel.visit_count >= trigger["visit_count"]:
                triggered = True

        if triggered:
            # Mark as triggered so it doesn't loop
            await set_flag(user_id, f"storylet_{storylet['id']}_done", "triggered", session)
            return storylet

    return None


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GameCog(bot))