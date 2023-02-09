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
    ConversationHandler,
)
import sheets

# states
START, SPOT, TIMETABLE = range(3)
# callback returning values
SUB, BACK = range(2)

TMP_DB = {}

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def subscribe(user, update):
    TMP_DB[update].append(user)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(timetable, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    keyboard = [[InlineKeyboardButton(k, callback_data=k) for k in timetable.keys()]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = f"Hi {user.full_name}! Select a subsidiary:"

    # TODO: Fix this moment
    if update.message is not None:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.answer()
        await update.callback_query.message.edit_text(msg, reply_markup=reply_markup)
    return SPOT


async def choose_place_btn_callback(timetable, update, context):
    query = update.callback_query
    await query.answer()
    table = "\n".join(
        [
            "%s:   %s" % (day, "   ".join(hours))
            for day, hours in timetable[query.data].items()
        ]
    )
    keyboard = [
        [
            InlineKeyboardButton(
                "Subsctibe to this subsidiary", callback_data=f"SUB%{query.data}"
            ),
            InlineKeyboardButton("Back", callback_data=BACK),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"{table}", reply_markup=reply_markup)
    return TIMETABLE


async def subscribe_btn_callback(timetable, update, context):
    # this is stub
    query = update.callback_query
    await query.answer()
    subsidiary = query.data.split("%")[1]
    await query.edit_message_text(f"You subscribed to {subsidiary} timetable updates!")
    logging.info(f"{update.effective_user.full_name} subscribed to {subsidiary}")
    subscribe(update.effective_chat.id, subsidiary)
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help is not ready yet, sorry :C")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text("Hello!")


def main() -> None:
    timetable = sheets.request_sheets()
    TMP_DB.update({k: [] for k in timetable.keys()})

    """Start the bot."""
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", partial(start, timetable))],
        states={
            # SPOT - Shows places
            SPOT: [
                CallbackQueryHandler(partial(choose_place_btn_callback, timetable)),
            ],
            # TIMETABLE - Shows timetable for selected place
            TIMETABLE: [
                # TODO: Fix pattern="^" + str(SUB) + "%.+" + "$" mismatching
                CallbackQueryHandler(partial(subscribe_btn_callback, timetable)),
                CallbackQueryHandler(
                    partial(start, timetable), pattern="^" + str(BACK) + "$"
                ),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
