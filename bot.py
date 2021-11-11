from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os

from diagram import generate_diagram

TOKEN = '1844583589:AAG2uRYXMTuU9KpQdBeUZEBrFHat9azDYW8'
hello_message = r'Привіт\! Надішли свій середній бал у форматі ХХ\.ХХ та в діапазоні від 50 до ста балів'
error_message = r'Cередній бал повинен бути у форматі ХХ.ХХ та в діапазоні від 50 до 100 балів'


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(hello_message, reply_markup=ForceReply(selective=True), )


def result_diag(update: Update, context: CallbackContext) -> None:
    if update.message is None:
        return

    try:
        user_rate = float(update.message.text)
    except ValueError:
        update.message.reply_text(error_message)
    else:
        if user_rate < 50 or user_rate > 100:
            update.message.reply_text(error_message)
        else:
            diag_path = f'diags\diag_{update.message.chat.id}.png'
            generate_diagram(user_rate, diag_path)
            with open(diag_path, 'rb') as diag_res:
                update.message.reply_photo(diag_res)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, result_diag))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
