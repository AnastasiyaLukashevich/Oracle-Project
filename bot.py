import os
from flask import Flask
import telebot
from threading import Thread

# --- ИНИЦИАЛИЗАЦИЯ ВЕБ-СЕРВЕРА ДЛЯ RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает в фоновом режиме!"

def run_web_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- НАСТРОЙКА TELEGRAM БОТА ---
TOKEN = "7786619038:AAHKknS1gJb02oEzZ0pxaLv6Zu9O36yoW2Q"
bot = telebot.TeleBot(TOKEN)

# Сброс сетевых вебхуков
try:
    bot.remove_webhook()
except:
    pass

@bot.message_handler(commands=['start'])
def send_start(message):
    # Защищенное считывание аргумента 'report' из строки /start report
    text_args = message.text.split()
    is_report = False
    
    if len(text_args) > 1 and "report" in text_args[1].lower():
        is_report = True
    
    # --- СЦЕНАРИЙ 1: ПОЛЬЗОВАТЕЛЬ ПРИШЕЛ С САЙТА ЗА ПОЛНЫМ ОТЧЕТОМ ---
    if is_report:
        full_report_text = (
            "📊 **ВАШ РАСШИРЕННЫЙ КАРМИЧЕСКИЙ ОТЧЕТ И СТРАТЕГИЯ ПРОРЫВА**\n\n"
            "Поздравляем! Вы успешно прошли глубокое сканирование матрицы ума. "
            "Ваш экспресс-анализ зафиксирован в базе администратора @AnastasiyaLukashevich.\n\n"
            "🔑 **ГЛУБОКИЙ РАЗБОР ВСЕХ СФЕР ЖИЗНИ:**\n\n"
            "1️⃣ **Психология ума:** Ваш текущий застой — это критическая перегрузка операционной системы вашего разума. Вы пытаетесь использовать старые шаблоны поведения в новом жизненном цикле. Система требует немедленного обнуления чужих ожиданий.\n\n"
            "2️⃣ **Финансовый блок:** Денежная энергия полностью заблокирована страхом масштаба. Вы подсознательно сжимаете свои проекты и доходы, чтобы оставаться в иллюзорной безопасности. Для прорыва вам необходимо оцифровать и автоматизировать все рутинные действия, делегировав мелочи.\n\n"
            "3️⃣ **Точка слива ресурсов:** Ваша главная уязвимость — это накопление бесконечной теории, курсов и дипломов без немедленного внедрения на практике. Синдром самозванца выжигает до 80% вашей жизненной энергии.\n\n"
            "🚀 **ВАША СТРАТЕГИЯ ПРОРЫВА:**\n"
            "• Прекратите копить знания. Запустите свой первый минимальный продукт (MVP) в течение 48 часов.\n"
            "• Поднимите стоимость своих услуг минимум в 2 раза — матрица не дает ресурсы под дешевые задачи.\n"
            "• Пропишите жесткий стратегический план на 3 года вперед и убирайте любую суету из расписания.\n\n"
            "💬 *Хотите получить персональный разбор вашей матрицы и составить пошаговый план выхода на новый финансовый уровень лично с экспертом? Напишите нашему главному проводнику: @AnastasiyaLukashevich*"
        )
        bot.reply_to(message, full_report_text, parse_mode="Markdown")
        
    # --- СЦЕНАРИЙ 2: ОБЫЧНЫЙ ПЕРВЫЙ ЗАПУСК БОТА ---
    else:
        # Исправлено: убрано двойное https://
        reply = (
            "🔮 **Система Digital Oracle OS активирована!**\n\n"
            "Оцифруй свою дату рождения, чтобы за 2 шага выявить скрытые ментальные блоки в сфере денег и узнать точную причину слива энергии.\n\n"
            "Запусти персональное сканирование матрицы ума на нашей интерактивной платформе:\n"
            "🔗 https://oracle-by-lu4ek.streamlit.app/\n\n"
            "🔒 *Данные строго конфиденциальны.*"
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
