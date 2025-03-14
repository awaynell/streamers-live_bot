import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from handleStreamers import add_vk_streamer, get_my_vk_streamers, start_checking
from dotenv import load_dotenv
from os import getenv

load_dotenv()

tg_bot_token = getenv('TG_BOT_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


def main() -> None:
    application = Application.builder().token(tg_bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_vk_streamer", add_vk_streamer))
    application.add_handler(CommandHandler(
        "my_vk_streamers", get_my_vk_streamers))
    application.add_handler(CommandHandler("s_check", start_checking))

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
