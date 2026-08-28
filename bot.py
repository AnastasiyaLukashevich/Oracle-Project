import telebot

# --- ОБНОВЛЕННЫЙ ТОКЕН БОТА ---
TOKEN = "7786619038:AAH2qq60z-m1NB9b6IHJuQrGk1irSesGu10"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_start(message):
    reply = "🔮 **Система Digital Oracle OS активирована!**\n\nЧтобы рассчитать свой Код Судьбы и пройти диагностику подсознания, перейдите на нашу интерактивную веб-платформу:\n🔗 https://streamlit.app"
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
    print("Бот успешно запущен...")
    bot.infinity_polling()
