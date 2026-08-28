import os
from flask import Flask
import telebot
from threading import Thread

# --- ИНИЦИАЛИЗАЦИЯ ВЕБ-СЕРВЕРА ДЛЯ БЕСПЛАТНОГО ТАРИФА RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает в фоновом режиме!"

def run_web_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- НАСТРОЙКА И КОМАНДЫ TELEGRAM БОТА ---
TOKEN = "7786619038:AAH2qq60z-m1NB9b6IHJuQrGk1irSesGu10"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_start(message):
    reply = "🔮 **Система Digital Oracle OS активирована!**\n\nЧтобы рассчитать свой Код Судьбы и пройти диагностику подсознания, перейдите на нашу интерактивную веб-платформу:\n🔗 https://oracle-by-lu4ek.streamlit.app/"
    bot.reply_to(message, reply, parse_mode="Markdown")

@bot.message_handler(commands=['about'])
def send_about(message):
    reply = "✨ **О проекте Digital Oracle OS**\n\nЭто экспертная ИТ-система, объединяющая прикладную психологию ума и алгоритмы нумерологической матрицы застоя.\n\nРазработчик: @Lu4ek_bot"
    bot.reply_to(message, reply, parse_mode="Markdown")

@bot.message_handler(commands=['admin'])
def send_admin(message):
    reply = "🔑 **Доступ ограничен.**\n\nБаза лидов выгружается строго через защищенный SSL-интерфейс веб-платформы Streamlit во вкладке Admin."
    bot.reply_to(message, reply, parse_mode="Markdown")

if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Telegram бот успешно запущен...")
    bot.infinity_polling()
