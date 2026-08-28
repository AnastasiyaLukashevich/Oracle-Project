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

# --- НАСТРОЙКА И КОМАНДЫ TELEGRAM БОТА С ВАШИМ АКТУАЛЬНЫМ ТОКЕНОМ ---
TOKEN = "7786619038:AAHKknS1gJb02oEzZ0pxaLv6Zu9O36yoW2Q"
bot = telebot.TeleBot(TOKEN)

# МГНОВЕННЫЙ СБРОС СЕТЕВЫХ КОНФЛИКТОВ ДО ЗАПУСКА КОМАНД
try:
    bot.remove_webhook()
except:
    pass

@bot.message_handler(commands=['start'])
def send_start(message):
    # --- ТЕКСТ ВАШЕГО ОБНОВЛЕННОГО ПРИВЕТСТВЕННОГО СООБЩЕНИЯ С НОВОЙ ССЫЛКОЙ ---
    reply = (
        "🔮 **Добро пожаловать в Digital Oracle OS!**\n\n"
        "Я — твой... Персональный цифровой проводник по матрице подсознания. "
        "Твой финансовый застой, выгорание или потеря фокуса — это не тупик, "
        "а зашифрованный сигнал системы о необходимости срочного обновления. "
        "Пора провести глубокий кармический аудит твоего ума! 🪐\n\n"
        "⚡ **За 2 шага мы полностью оцифруем твою дату рождения и выдадим точечный вердикт:**\n"
        "🧠 Твою индивидуальную психологию застоя\n"
        "💸 Скрытые ментальные блоки в сфере денег\n"
        "🪫 Точную причину, куда ты прямо сейчас сливаешь энергию\n\n"
        "Переходи по ссылке на нашу защищенную интерактивную веб-платформу, чтобы запустить сканирование матрицы:\n"
        "🔗 https://oracle-by-lu4ek.streamlit.app/\n\n"
        "🔒 *Данные строго конфиденциальны. Приготовься увидеть скрытые паттерны своего разума.*"
    )
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
    bot.infinity_polling(skip_pending=True)
