import logging

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, PicklePersistence

import dotenv
import os
dotenv.load_dotenv()

import database as db

from bot.states import STATE
import bot.conversation.start


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

async def on_startup(app: ApplicationBuilder):
    await db.init_db()


def bot_main():

    persistence_file = PicklePersistence(filepath='conversation_data')

    BOT_TOKEN = os.getenv("telegram_token")
    if BOT_TOKEN is None:
        raise ValueError("Please set the telegram_token environment variable.")

    application = ApplicationBuilder().token(BOT_TOKEN).persistence(persistence_file).post_init(on_startup).build()




    # Configuration only for one user definied in the .env file

    states_dict = {
        STATE.NOT_ALLOWED: [],
        STATE.ALLOWED: [
            CommandHandler("start", bot.conversation.start.start_command_handler),
        ],
    }


    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", bot.conversation.start.start_command_handler)],
        states=states_dict,
        fallbacks=[],
        persistent=True,
        name="conversation_handler",
    )

    application.add_handler(conversation_handler)


    application.run_polling()
