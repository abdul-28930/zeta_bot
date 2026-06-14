"""
cogs/dev.py — Zeta Developer Commands

Testing-phase commands for resetting player state.
Restrict to developer Discord user IDs only.

Save as: cogs/dev.py
Then add to main.py: await bot.load_extension("cogs.dev")
"""
import discord
from discord import app_commands
from discord.ext import commands

from core.database import get_session
from core.cache import get_redis

# ── Developer user IDs ────────────────────────────────────────────────────────
# Add your Discord user ID(s) here. Only these users can run dev commands.
DEV_USER_IDS = {
    524873455636840448,   # Ultimate Kagune (replace with your actual ID)
}


def is_dev(interaction: discord.Interaction) -> bool:
    return interaction.user.id in DEV_USER_IDS


class DevCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── /dev_reset ────────────────────────────────────────────────────────────

    @app_commands.command(
        name="dev_reset",
        description="[DEV] Completely reset a user's data — wipes all progress and sends them back to tutorial.",
    )
    @app_commands.describe(user="The user to reset (leave blank to reset yourself)")
    async def dev_reset(
        self,
        interaction: discord.Interaction,
        user: discord.User | None = None,
    ) -> None:
        if not is_dev(interaction):
            return await interaction.response.send_message(
                "❌ Developer only command.", ephemeral=True
            )

        target      = user or interaction.user
        target_id   = target.id

        await interaction.response.defer(ephemeral=True)

        deleted = []
        errors  = []

        # ── 1. Wipe DB rows ───────────────────────────────────────────────────
        try:
            from sqlalchemy import text
            async with get_session() as session:
                # Use CASCADE via a single query — delete player, FK cascade handles children
                # But first try explicit child deletion for tables without CASCADE
                child_tables = [
                    "player_quests",
                    "player_storylet_progress",
                    "player_flags",
                    "npc_relationships",
                    "player_inventory",
                    "player_deck",
                    "player_card_collection",
                    "player_stats",
                    "player_progression",
                    "player_bank",
                    "dialogue_turns",
                    "player_items",
                    "player_equipment",
                    "player_achievements",
                    "player_daily_quests",
                    "player_faction_rep",
                    "player_zone_mastery",
                ]
                for table in child_tables:
                    try:
                        # SAVEPOINT lets us recover if table doesn't exist
                        # without aborting the whole transaction
                        await session.execute(text(f"SAVEPOINT sp_{table}"))
                        result = await session.execute(
                            text(f"DELETE FROM {table} WHERE user_id = :uid"),
                            {"uid": target_id},
                        )
                        await session.execute(text(f"RELEASE SAVEPOINT sp_{table}"))
                        if result.rowcount:
                            deleted.append(f"DB: {table} ({result.rowcount} rows)")
                    except Exception:
                        # Roll back to savepoint — transaction stays alive
                        try:
                            await session.execute(text(f"ROLLBACK TO SAVEPOINT sp_{table}"))
                        except Exception:
                            pass

                # Delete parent row — all FK children already cleared above
                await session.execute(
                    text("DELETE FROM players WHERE user_id = :uid"),
                    {"uid": target_id},
                )
            deleted.append("✅ DB wipe complete")
        except Exception as e:
            errors.append(f"DB error: {e}")

        # ── 2. Wipe Redis keys ────────────────────────────────────────────────
        try:
            r      = get_redis()
            # Find all keys belonging to this user
            patterns = [
                f"battle:{target_id}",
                f"embed_state:{target_id}",
                f"char_create:{target_id}",
                f"walk_state:{target_id}",
                f"steps:{target_id}:*",
                f"total_steps:{target_id}:*",
                f"walk_seen:{target_id}:*",
                f"mastery:{target_id}:*",
                f"zone_players:*",  # will scan and remove member
            ]
            redis_deleted = 0
            for pattern in patterns:
                if "*" in pattern:
                    keys = await r.keys(pattern)
                    if keys:
                        await r.delete(*keys)
                        redis_deleted += len(keys)
                else:
                    deleted_count = await r.delete(pattern)
                    redis_deleted += deleted_count

            deleted.append(f"✅ Redis wipe complete ({redis_deleted} keys)")
        except Exception as e:
            errors.append(f"Redis error: {e}")

        # ── 3. Build response ─────────────────────────────────────────────────
        embed = discord.Embed(
            title=f"🔄  Reset Complete — {target.display_name}",
            color=0x57B05E if not errors else 0xEF9F27,
        )

        if deleted:
            embed.add_field(
                name="Wiped",
                value="\n".join(deleted[-5:]),  # last 5 to keep it readable
                inline=False,
            )

        if errors:
            embed.add_field(
                name="⚠️ Errors",
                value="\n".join(errors),
                inline=False,
            )

        embed.add_field(
            name="Next step",
            value=f"{target.mention} can now run `/zeta` to go through the tutorial fresh.",
            inline=False,
        )

        embed.set_footer(text="DEV command · Testing phase only")
        await interaction.followup.send(embed=embed, ephemeral=True)

    # ── /dev_setlevel ─────────────────────────────────────────────────────────

    @app_commands.command(
        name="dev_setlevel",
        description="[DEV] Set a user's level directly.",
    )
    @app_commands.describe(
        level="Level to set (1-50)",
        user="The user to modify (leave blank for yourself)",
    )
    async def dev_setlevel(
        self,
        interaction: discord.Interaction,
        level: int,
        user: discord.User | None = None,
    ) -> None:
        if not is_dev(interaction):
            return await interaction.response.send_message(
                "❌ Developer only command.", ephemeral=True
            )

        target    = user or interaction.user
        target_id = target.id

        if not 1 <= level <= 50:
            return await interaction.response.send_message(
                "Level must be between 1 and 50.", ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)

        try:
            from sqlalchemy import update, text
            async with get_session() as session:
                await session.execute(
                    text("UPDATE player_progression SET level = :lvl WHERE user_id = :uid"),
                    {"lvl": level, "uid": target_id},
                )
            await interaction.followup.send(
                f"✅ Set **{target.display_name}** to level **{level}**.", ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)

    # ── /dev_givezet ──────────────────────────────────────────────────────────

    @app_commands.command(
        name="dev_givezet",
        description="[DEV] Give a user some Ƶet.",
    )
    @app_commands.describe(
        amount="Amount of Ƶ to give",
        user="The user to give Ƶ to (leave blank for yourself)",
    )
    async def dev_givezet(
        self,
        interaction: discord.Interaction,
        amount: int,
        user: discord.User | None = None,
    ) -> None:
        if not is_dev(interaction):
            return await interaction.response.send_message(
                "❌ Developer only command.", ephemeral=True
            )

        target    = user or interaction.user
        target_id = target.id

        await interaction.response.defer(ephemeral=True)

        try:
            from game.world import add_zet
            async with get_session() as session:
                await add_zet(target_id, amount, session)
            await interaction.followup.send(
                f"✅ Gave **{amount} Ƶ** to **{target.display_name}**.", ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)

    # ── /dev_inspect ──────────────────────────────────────────────────────────

    @app_commands.command(
        name="dev_inspect",
        description="[DEV] View a user's raw game state.",
    )
    @app_commands.describe(user="The user to inspect (leave blank for yourself)")
    async def dev_inspect(
        self,
        interaction: discord.Interaction,
        user: discord.User | None = None,
    ) -> None:
        if not is_dev(interaction):
            return await interaction.response.send_message(
                "❌ Developer only command.", ephemeral=True
            )

        target    = user or interaction.user
        target_id = target.id

        await interaction.response.defer(ephemeral=True)

        try:
            from game.world import get_full_player
            from game.quests import get_quest_log
            async with get_session() as session:
                player    = await get_full_player(target_id, session)
                quest_log = await get_quest_log(target_id, session)

            if not player:
                return await interaction.followup.send(
                    f"No player found for {target.display_name}.", ephemeral=True
                )

            prog  = player.progression
            stats = player.stats

            embed = discord.Embed(
                title=f"🔍  {player.character_name}  ({target.display_name})",
                color=0x7F77DD,
            )
            embed.add_field(
                name="Progression",
                value=(
                    f"Level: {prog.level}\n"
                    f"XP: {prog.xp}\n"
                    f"HP: {prog.current_hp}\n"
                    f"Ƶ: {prog.zet_wallet}\n"
                    f"Zone: {prog.current_zone_id}"
                ),
                inline=True,
            )
            embed.add_field(
                name="Stats",
                value=(
                    f"STR:{stats.strength} DEF:{stats.defense}\n"
                    f"AGI:{stats.agility} INT:{stats.intel}\n"
                    f"VIT:{stats.vit} LCK:{stats.lck}\n"
                    f"Unspent: {stats.unspent_points}"
                ),
                inline=True,
            )
            embed.add_field(
                name="Quests",
                value=(
                    f"Active: {len(quest_log['active'])}\n"
                    f"Completed: {quest_log['completed_count']}"
                ),
                inline=True,
            )
            embed.add_field(
                name="Identity",
                value=f"Race: {player.race_id}\nClass: {player.class_id}",
                inline=True,
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DevCog(bot))