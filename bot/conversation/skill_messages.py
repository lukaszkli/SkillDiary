import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.skills_updater import skill_updater_message_handler

import database as db

async def skill_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_telegram_id = update.effective_user.id
    user = await db.User.get(telegram_id=user_telegram_id)
    user_message = update.message.text

    # Enable writing signal in telegram
    await update.message.reply_chat_action(telegram.constants.ChatAction.TYPING)

    # Get the skill categories demand from the user message
    skills = await skill_updater_message_handler(user.id, user_message)

    # Create the inline keyboard buttons
    message = ""
    if skills.updated_skills:
        message += "<b>✨ Updated Skills ✨</b>\n\n"
        for category in skills.updated_skills:
            message += f"📚 <b>Category:</b> <i>{category.category_name}</i>\n"
            for skill in category.skills:
                message += f"  - 🛠️ <b>Skill:</b> <code>{skill.skill_name}</code> | <b>Points:</b> <code>{skill.points}</code>\n"
            message += "\n" # Add a newline between categories
    else:
        message = "🤔 No skills were updated based on your message."


    await context.bot.send_message(text=message, chat_id=user_telegram_id, parse_mode=telegram.constants.ParseMode.HTML)
    