import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


import database as db

from core.skillset import get_skillset


async def skillset_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Handler for the /skillset command
        Showing the skillset of the user.
    """
    
    user_telegram_id = update.effective_user.id
    user = await db.User.get(telegram_id=user_telegram_id)
    
    # Get the skillset
    skillset = await get_skillset(user)


    # Create message
    message = "<b>✨ Skillset ✨</b>\n\n"
    for category in skillset.skill_categories:
        message += f"📚 <b>Category:</b> <i>{category.category_name}</i>\n"
        message += f"  - <b>Description:</b> <i>{category.category_description}</i>\n"
        message += f"  - <b>Points:</b> <code>{category.sum_points}</code>\n"
        message += "\n" # Add a newline between categories
    message += "<b>💡 Note:</b> The skillset is based on the skills you have learned and the points you have earned.\n"
    
    # Send the message
    await update.message.reply_text(
        text=message,
        parse_mode=telegram.constants.ParseMode.HTML
    )

    

async def skillset_summary_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Handler for the /skillset_summary command
        Showing the skillset of the user.
    """

    user_telegram_id = update.effective_user.id
    user = await db.User.get(telegram_id=user_telegram_id)
    
    # Get the skillset
    skillset = await get_skillset(user, summary=True)


    # Create message
    message = "<b>✨ Skillset Summary ✨</b>\n\n"
    message += f"{skillset.summary}\n\n"
    message += "<b>💡 Note:</b> The skillset is based on the skills you have learned and the points you have earned.\n"

    # Send the message
    await update.message.reply_text(
        text=message,
        parse_mode=telegram.constants.ParseMode.HTML
    )

