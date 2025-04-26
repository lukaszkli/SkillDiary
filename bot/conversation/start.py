import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import database as db

import os
from bot.states import STATE

async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""

    user_telegram_id = update.effective_user.id
    
    # Check if the user is allowed to use the bot
    if user_telegram_id not in [int(os.getenv("allowed_user_id"))]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot.")
        return STATE.NOT_ALLOWED
    

    # Create a new user in the database if it doesn't exist
    user = await db.User.get_or_none(telegram_id=user_telegram_id)
    if not user:
        user = await db.User.create(telegram_id=user_telegram_id, first_name=update.effective_user.first_name)

    # Send a welcome message
    message = f"Hello, {update.effective_user.first_name}! Welcome to the bot. What you learn today?"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    return STATE.ALLOWED