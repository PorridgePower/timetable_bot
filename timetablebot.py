import logging
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
import sheets
from config import Config

# states
START, SPOT, TIMETABLE = range(3)
# callback returning values
SUB, BACK = range(2)

# Temporary test solution for subscribers
TMP_DB = {}
# For Sheets changes momitoring
HASHES = {}

# Enable logging
logging.basicConfig(
    format="%(asctime)s -- %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def subscribe(user, update):
    TMP_DB[update].append(user)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    timetable = context.bot_data["timetable"]
    keyboard = [[InlineKeyboardButton(k, callback_data=k) for k in timetable.keys()]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = f"Hi {user.full_name}! Select a subsidiary:"

    # TODO: Fix this moment
    if update.message is not None:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.answer()
        await query.message.edit_text(msg, reply_markup=reply_markup)
    return SPOT


async def choose_place_btn_callback(update, context):
    query = update.callback_query
    timetable = context.bot_data["timetable"]
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


async def subscribe_btn_callback(update, context):
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


async def check_updates(context: CallbackContext):
    timetable = sheets.request_sheets()
    for k, v in HASHES.items():
        if hash(str(timetable[k])) != v:
            logging.info(f"Timetable for {k} was updated")
            # send message to all users subscribed to subsidiary
            for id in TMP_DB[k]:
                table = "\n".join(
                    [
                        "%s:   %s" % (day, "   ".join(hours))
                        for day, hours in timetable[k].items()
                    ]
                )
                await context.bot.send_message(
                    chat_id=id, text=(f"Timetable for {k} was updated:\n{table}")
                )
            HASHES[k] = timetable[k]
            context.bot_data["timetable"] = timetable


def main() -> None:
    timetable = sheets.request_sheets()
    TMP_DB.update({k: [] for k in timetable.keys()})
    HASHES.update({k: hash(str(v)) for k, v in timetable.items()})

    """Start the bot."""
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # SPOT - Shows places
            SPOT: [
                CallbackQueryHandler(choose_place_btn_callback),
            ],
            # TIMETABLE - Shows timetable for selected place
            TIMETABLE: [
                # TODO: Fix pattern="^" + str(SUB) + "%.+" + "$" mismatching
                CallbackQueryHandler(subscribe_btn_callback),
                CallbackQueryHandler(start, pattern="^" + str(BACK) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    application.add_handler(conv_handler)

    application.bot_data["timetable"] = timetable

    jq = application.job_queue
    jq.run_repeating(check_updates, interval=3600, first=3600)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
