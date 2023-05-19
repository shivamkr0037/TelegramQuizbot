import sqlite3
import telegram
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
from the utils.database and utils.models modules

from utils.database import setup_database, get_score, update_highscore, get_highscores, get_global_highscores

from utils.models import load_categories

class QuizBot:
    def __init__(self, token):
        self.bot = telegram.Bot(token=token)
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        # Load the questions from the categories folder
        self.categories = load_categories()

        # Register the handlers
        self.register_handlers()

        # Set up the SQLite database for high scores
        setup_database()

    def register_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('cat', self.show_categories))
        self.dispatcher.add_handler(CallbackQueryHandler(self.select_category, pattern='^category:'))
        self.dispatcher.add_handler(CallbackQueryHandler(self.answer))
        self.dispatcher.add_handler(CommandHandler('score', self.score))
        self.dispatcher.add_handler(CommandHandler('highscores', self.highscores))
        self.dispatcher.add_handler(CommandHandler('leaderboard', self.leaderboard))
        self.dispatcher.add_handler(CommandHandler('end', self.end))
        self.dispatcher.add_handler(CommandHandler('next', self.next_question))

    def start(self, update, context):
        update.message.reply_text("Welcome to the quiz bot! Type /cat to select a category.")

    def show_categories(self, update, context):
        keyboard = [[InlineKeyboardButton(category_name, callback_data=f"category:{category_name}")] for category_name in self.categories.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Select a category:", reply_markup=reply_markup)

    def select_category(self, update, context):
        query = update.callback_query
        query.answer()
        category_name = query.data[9:]
        context.chat_data['selected_category'] = category_name
        context.chat_data['score'] = 0
        context.chat_data['question_index'] = 0
        context.chat_data['questions'] = self.shuffle_questions(self.categories[category_name])
        self.ask_question(update, context)

    def answer(self, update, context):
        query = update.callback_query
        query.answer()

        user_first_name = update.effective_user.first_name
        correct_answer = context.chat_data['questions'][context.chat_data['question_index']]['correct_answer']
        chat_id = update.effective_chat.id

        if query.data == correct_answer:
            user_id = update.effective_user.id
            user_name = update.effective_user.full_name
            score = self.get_score(user_id, chat_id)
            score += 10
            context.chat_data['score'] = score
            self.update_highscore(user_id, user_name, chat_id, context.chat_data['score'])
            query.bot.send_message(chat_id=chat_id, text=f"{user_first_name}, That's Correct! 🎉 Your score: {context.chat_data['score']}")
        else:
            query.bot.send_message(chat_id=chat_id, text=f"Sorry {user_first_name}, that's incorrect. 😞 Your score: {context.chat_data['score']}")

        context.chat_data['question_index'] += 1
        if context.chat_data['question_index'] < len(context.chat_data['questions']):
            self.next_question(update, context)
        else:
            self.end_quiz(update, context)

    def ask_question(self, update, context):
        question = context.chat_data['questions'][context.chat_data['question_index']]['question']
        answer_options = context.chat_data['questions'][context.chat_data['question_index']]['answer_options']
        answer_options_text = '\n'.join(['{}. {}'.format(chr(i+65), option) for i, option in enumerate(answer_options)])
        keyboard = [[InlineKeyboardButton(answer_option, callback_data=answer_option) for answer_option in answer_options]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text=f"{question}\n\n{answer_options_text}", reply_markup=reply_markup)

    def next_question(self, update, context):
        self.ask_question(update, context)

    def shuffle_questions(self, category):
        shuffled_category = category.copy()
        random.shuffle(shuffled_category)
        return shuffled_category
    
    def end_quiz(self, update, context):
        chat_id = update.effective_chat.id
        update.callback_query.bot.send_message(chat_id=chat_id, text=f"End of quiz! Your score: {context.chat_data['score']}\nType /cat to play again.")

    def end(self, update, context):
        update.message.reply_text("Thank you for playing! Type /cat to play again.")

    def score(self, update, context):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        score = self.get_score(user_id, chat_id)
        update.message.reply_text(f"Your current score is: {score}")

    def highscores(self, update, context):
        chat_id = update.effective_chat.id
        highscores = self.get_highscores(chat_id)
        if not highscores:
            update.message.reply_text("No highscores for this chat yet.")
        else:
            highscore_message = "Highscores for this chat:\n"
            for idx, highscore in enumerate(highscores):
                if idx < 3:
                    emoji = "🥇"
                elif idx >= 3 and idx < 6:
                    emoji = "🥈"
                else:
                    emoji = "🥉"

                highscore_message += "{}. {} {} - Score: {}\n".format(idx + 1, emoji, highscore[1], highscore[3])

            update.message.reply_text(highscore_message)

    def leaderboard(self, update, context):
        global_highscores = self.get_global_highscores()
        if not global_highscores:
            update.message.reply_text("No global highscores yet.")
        else:
            leaderboard_message = "Global Leaderboard:\n"
            for idx, highscore in enumerate(global_highscores):
                leaderboard_message += "{}. {} - Score: {}\n".format(idx + 1, highscore[1], highscore[2])

            update.message.reply_text(leaderboard_message)

    def get_score(self, user_id, chat_id):
        conn = sqlite3.connect('highscores.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT score FROM highscores WHERE user_id=? AND chat_id=?", (user_id, chat_id))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def update_highscore(self, user_id, user_name, chat_id, score):
        conn = sqlite3.connect('highscores.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO highscores VALUES (?, ?, ?, ?)", (user_id, user_name, chat_id, score))
        conn.commit()
        conn.close()

    def get_highscores(self, chat_id):
        conn = sqlite3.connect('highscores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM highscores WHERE chat_id=? ORDER BY score DESC", (chat_id,))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_global_highscores(self):
        conn = sqlite3.connect('highscores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, user_name, SUM(score) as total_score FROM highscores GROUP BY user_id, user_name ORDER BY total_score DESC")
        result = cursor.fetchall()
        conn.close()
        return result

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

