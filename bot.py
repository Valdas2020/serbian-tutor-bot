import asyncio
import logging
import signal

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, setup_logging
from database import init_db
from handlers import router

logger = logging.getLogger(__name__)


async def main() -> None:
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

    # Graceful shutdown on SIGTERM (sent by Render during deploys)
    loop = asyncio.get_running_loop()

    def _handle_signal(sig: int) -> None:
        logger.info("Received signal %s, shutting down...", signal.Signals(sig).name)
        # Stop polling immediately so the new instance can take over
        dp.shutdown()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _handle_signal, sig)

    # Delete webhook & drop pending updates before starting polling
    # This ensures clean state after a deploy
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook cleared, starting polling...")

    # Start polling
    logger.info("Bot is running.")
    try:
        await dp.start_polling(bot, drop_pending_updates=True)
    finally:
        await bot.session.close()
        logger.info("Bot stopped cleanly.")


if __name__ == "__main__":
    asyncio.run(main())
