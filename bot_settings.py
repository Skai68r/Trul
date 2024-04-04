import telebot
from dotenv import load_dotenv
import os

load_dotenv()  # load_dotenv() - загрузка переменных окружения из файла .env

bot = telebot.TeleBot(os.getenv('TOKEN')) #объект бот