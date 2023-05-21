# QuizBot

QuizBot is a Telegram bot that allows users to take a quiz and save their high scores.

## Installation

To use QuizBot, you must have Python 3.x installed on your system. If you're using Ubuntu, you can install Python using the following command in your terminal:

```

sudo apt-get update && sudo apt-get install -y python3

```

Once you have Python installed, you can install the necessary dependencies using pip:

```

pip install -r requirements.txt

```

You should also have a Telegram bot token, which you can obtain by creating a new bot using the BotFather on Telegram.

## Usage

To start QuizBot, run the following command in your terminal:

```

python3 quizbot.py

```

Make a file token.txt add your Telegram bot token in it.

Once the bot is running, users can interact with it by sending commands and answering quiz questions.

## Commands

- `/start` - Start the quiz

- `/score` - View your current score

- `/highscores` - View the top 10 high scores

- `/leaderboard` - View the top 10 high scores with usernames

- `/end` - End the quiz

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



