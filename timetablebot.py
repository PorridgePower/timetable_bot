import logging
from functools import partial
from config import Config
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
import sheets

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(timetable, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    keyboard = [[InlineKeyboardButton(k, callback_data=k) for k in timetable.keys()]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Hi {user.full_name}! Select a subsidiary:", reply_markup=reply_markup
    )


async def callback_button(timetable, update, context):
    query = update.callback_query
    table = "\n".join(
        [f"{day}:  {hours}" for day, hours in timetable[query.data].items()]
    )
    await query.answer()
    await query.edit_message_text(text=f"{table}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help is not ready yet, sorry :C")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text("Hello!")


def main() -> None:
    timetable = sheets.request_sheets()

    """Start the bot."""
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", partial(start, timetable)))
    application.add_handler(CallbackQueryHandler(partial(callback_button, timetable)))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
