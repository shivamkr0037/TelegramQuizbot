import logging
import os
import json
import random
import sqlite3
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from utils.handlers import QuizBot
from utils.database import setup_database, setup_databasee
from utils.models import load_categories, parse_questions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
def main():
    with open('token.txt', 'r') as f:
        token = f.read().strip()

    # Set up the SQLite database for high scores
    setup_database()
    setup_databasee()
    # Load the questions from the categories folder
    categories = load_categories()

    # Initialize the QuizBot
    quiz_bot = QuizBot(token, categories)

    # Register the handlers
    quiz_bot.register_handlers()

    # Run the bot
    quiz_bot.run()


if __name__ == '__main__':
    main()

