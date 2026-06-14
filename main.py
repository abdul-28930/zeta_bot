"""
Zeta — AI RPG Discord Bot
Main entry point.
"""
import asyncio
import logging
import discord
from discord.ext import commands
from config import settings

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("zeta")


class ZetaBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        logger.info("Initializing database...")
        from core.database import init_db
        await init_db()

        logger.info("Connecting to Redis...")
        from core.cache import init_redis
        await init_redis()

        logger.info("Loading cogs...")
        await self.load_extension("cogs.game")
        await self.load_extension("cogs.dev")

        logger.info("Syncing slash commands...")
        await self.tree.sync()
        logger.info("Sync complete.")

    async def on_ready(self) -> None:
        logger.info(f"✅  Zeta is online as {self.user} (ID: {self.user.id})")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="www.zetabot.xyz",
            )
        )

    async def on_command_error(self, ctx, error) -> None:
        logger.error(f"Command error: {error}")

    async def on_application_command_error(
        self, interaction: discord.Interaction, error
    ) -> None:
        logger.error(f"Slash command error: {error}")
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "Something went wrong. Please try again.", ephemeral=True
                )
        except Exception:
            pass


async def main() -> None:
    bot = ZetaBot()
    async with bot:
        await bot.start(settings.discord_token)


if __name__ == "__main__":
    asyncio.run(main())