import os
import config
import logging
import asyncio
import google.generativeai as genai
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CallbackContext, CommandHandler, filters, Application, ApplicationBuilder, ContextTypes, CallbackQueryHandler

# Create a new Gemini API client
genai.configure(api_key=config.gemini_api)
gemini = genai.GenerativeModel('gemini-pro')

#Create a ChatGPT client
chatgpt_api = config.chatgpt_api

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Defining the start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [
         [InlineKeyboardButton("ChatGPT", callback_data='chatgpt')],
         [InlineKeyboardButton("Gemini", callback_data='gemini')]

    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("How you doing? Now choose which AI you wanna use.",
                                    reply_markup=reply_markup)


# Defining the buttons
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'chatgpt':
        await query.edit_message_text(text="You've chosen ChatGPT.")
        await handle_chatgpt(update, context)
        await update.reply_text("Hello")

    elif query.data == 'gemini':
        await query.edit_message_text(text="You've chosen Gemini.")
        await handle_gemini(update, context)

async def handle_gemini(update: Update, context: CallbackContext):
    '''
    Defining a function to generate text from Gemini
    '''
    response = genai.GenerativeModel('gemini-pro').start_chat(history=[]).send_message(update.message.text, stream = False)
    await update.message.reply_text(response.text)

async def handle_chatgpt(update: Update, context: CallbackContext):
     '''
     Defining a function to generate text from ChatGPT
     '''
     if update.message and update.message.text:
        client = OpenAI(api_key=config.chatgpt_api)
        response = await client.chat.completions.create(
          model = config.chatgpt_model,
          messages = [
               {"role": "system", "content": "Answer nicely!."},
                {"role": "user", "content": update.message.text},
          ],
          stream = False
     )
        await update.message.reply_text(response.choices[0].message)
     else:
        client = OpenAI(api_key=config.chatgpt_api)
        response = await client.chat.completions.create(
            model = config.chatgpt_model,
            messages = [
                {"role": "system", "content": "Answer nicely!"},
                {"role": "user", "content": "Hello"},
            ],
            stream = False
        )
        await update.message.reply_text(response.choices[0].message)

def main() -> None:
    '''Start the bot'''
    application = (
        ApplicationBuilder()
        .token(config.telegram_token)
        .concurrent_updates(True)
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .build()
    )

    # Add Handler
    user_filter = filters.ALL
    if len(config.allowed_telegram_usernames) > 0:
            usernames = [x for x in config.allowed_telegram_usernames if isinstance(x, str)]
            any_ids = [x for x in config.allowed_telegram_usernames if isinstance(x, int)]
            user_ids = [x for x in any_ids if x > 0]
            group_ids = [x for x in any_ids if x < 0]
            user_filter = filters.User(username=usernames) | filters.User(user_id=user_ids) | filters.Chat(chat_id=group_ids)

    application.add_handler(CommandHandler("start", start_command, filters = user_filter))
    application.add_handler(CallbackQueryHandler(button_click, pattern= "^(chatgpt|gemini)$"))
    application.add_handler(MessageHandler(filters.Regex(r'^\/.*') & user_filter, handle_chatgpt))
    application.add_handler(MessageHandler(filters.Regex(r'^(?!\/).*') & user_filter, handle_gemini))
    application.run_polling()

if __name__ == "__main__":
    main()
