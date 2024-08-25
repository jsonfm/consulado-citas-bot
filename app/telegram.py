import telebot
from app.config import Config


bot = telebot.TeleBot(Config.TELEGRAM_TOKEN, parse_mode=None) 
