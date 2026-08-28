@bot.message_handler(commands=['start'])
def send_start(message):
    reply = (
        "🔮 **Система Digital Oracle OS активирована!**\n\n"
        "Оцифруй свою дату рождения, чтобы за 2 шага выявить скрытые ментальные блоки в сфере денег и узнать точную причину слива энергии.\n\n"
        "Запусти персональное сканирование матрицы ума на нашей интерактивной платформе:\n"
        "🔗 https://oracle-by-lu4ek.streamlit.app/\n\n"
        "🔒 *Данные строго конфиденциальны.*"
    )
    bot.reply_to(message, reply, parse_mode="Markdown")
