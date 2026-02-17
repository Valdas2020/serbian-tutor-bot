import asyncio
import logging
import signal

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import BOT_TOKEN, setup_logging
from database import init_db
from handlers import router

logger = logging.getLogger(__name__)

# Global flag so signal handler can request stop
_shutdown_event: asyncio.Event | None = None


async def main() -> None:
    global _shutdown_event
    setup_logging()
    logger.info("Starting Serbian Tutor Bot...")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Create bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    _shutdown_event = asyncio.Event()

    # Graceful shutdown on SIGTERM (sent by Render during deploys)
    loop = asyncio.get_running_loop()

    def _handle_signal(sig: int) -> None:
        logger.info("Received signal %s, shutting down...", signal.Signals(sig).name)
        _shutdown_event.set()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _handle_signal, sig)

    # Delete webhook & drop pending updates before starting polling
    # This ensures clean state and cancels any lingering getUpdates from old instance
    await bot.delete_webhook(drop_pending_updates=True)
    # Small delay to let Telegram release the old polling connection
    await asyncio.sleep(1)

    # Register bot commands so they appear in Telegram's menu
    await bot.set_my_commands([
        BotCommand(command="start", description="Start over / Начать сначала"),
        BotCommand(command="settings", description="Settings / Настройки"),
        BotCommand(command="help", description="Help / Справка"),
    ])

    logger.info("Webhook cleared, commands registered, starting polling...")

    # Start polling
    logger.info("Bot is running.")
    try:
        await dp.start_polling(
            bot,
            drop_pending_updates=True,
            polling_timeout=30,
        )
    finally:
        await bot.session.close()
        logger.info("Bot stopped cleanly.")


if __name__ == "__main__":
    asyncio.run(main())
