import os
import streamlit as st
from datetime import date, datetime
import requests
import urllib.parse

# Чистый импорт внешней базы данных core_data.py
from core_data import CORE_DATA

st.set_page_config(page_title="Oracle OS", page_icon="🔮", layout="centered")

# --- НАСТРОЙКА СВЯЗИ С TELEGRAM ---
TELEGRAM_BOT_TOKEN = "7786619038:AAHKknS1gJb02oEzZ0pxaLv6Zu9O36yoW2Q"
TELEGRAM_CHAT_ID = 982947729  # Ваш личный цифровой ID для получения лидов

# --- ИНИЦИАЛИЗАЦИЯ БЕЗОПАСНОЙ ПАМЯТИ CRM ВНУТРИ ОБЛАКА ---
if "stage" not in st.session_state: st.session_state.stage = 1
if "num_code" not in st.session_state: st.session_state.num_code = None
if "user_contact" not in st.session_state: st.session_state.user_contact = ""
if "user_birth_date_str" not in st.session_state: st.session_state.user_birth_date_str = ""
if "crm_db" not in st.session_state: st.session_state.crm_db = []

def calculate_numerology_number(birth_date):
    date_str = birth_date.strftime("%Y%m%d")
    digits_sum = sum(int(char) for char in date_str)
    while digits_sum > 9: digits_sum = sum(int(char) for char in str(digits_sum))
    return str(digits_sum)

def save_lead(contact, date_text, num_key):
    try:
        msg = (
            f"🔮 **SYSTEM: Новый лид в системе!**\n\n"
            f"👤 **Юзер:** {contact}\n"
            f"📅 **Дата рождения:** {date_text}\n"
            f"🔢 **Код матрицы:** Число {num_key}\n\n"
            f"Администратор: @AnastasiyaLukashevich"
        )
        gateway_url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(gateway_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def send_results_to_admin(contact, date_text, num_key, q1, r1, t1, q2, r2, t2, report):
    try:
        msg = (
            f"📊 **SYSTEM: Пользователь полностью прошёл тест!**\n\n"
            f"👤 **Ник пользователя:** {contact}\n"
            f"📅 **Дата рождения:** {date_text}\n"
            f"🔢 **Код матрицы:** Число {num_key}\n\n"
            f"❓ **Вопрос 1:** {q1}\n"
            f"🔘 *Выбранный клик:* {r1}\n"
            f"✍️ *Свой текст:* {t1 if t1 else 'Не заполнено'}\n\n"
            f"❓ **Вопрос 2:** {q2}\n"
            f"🔘 *Выбранный клик:* {r2}\n"
            f"✍️ *Свой текст:* {t2 if t2 else 'Не заполнено'}\n\n"
            f"📝 **Итоговый вердикт сайта:** {report}\n\n"
            f"Администратор: @AnastasiyaLukashevich"
        )
        gateway_url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(gateway_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

st.title("🔮 Digital Oracle OS")

if st.session_state.stage == 1:
    st.subheader("🪐 Шаг I: Творение персональной матрицы")
    with st.form("stage1_form"):
        user_date = st.date_input("Выберите вашу дату рождения:", value=date(2000, 1, 1), min_value=date(1920, 1, 1), max_value=date.today())
        user_contact = st.text_input("Ваш Telegram-никнейм для активации ключа:", placeholder="@username")
        if st.form_submit_button("🔑 Рассчитать Код Судьбы"):
            if user_date == date(2000, 1, 1): 
                st.error("Пожалуйста, откройте календарь и выберите ваш настоящий день рождения.")
            elif not user_contact: 
                st.error("Пожалуйста, введите ваш Telegram-никнейм.")
            else:
                num_code = calculate_numerology_number(user_date)
                date_formatted = user_date.strftime('%d.%m.%Y')
                
                st.session_state.num_code = num_code
                st.session_state.user_contact = user_contact
                st.session_state.user_birth_date_str = date_formatted
                
                st.session_state.crm_db.append(
                    f"Запись: {datetime.now().strftime('%d.%m.%Y %H:%M')} | Юзер: {user_contact} | Дата: {date_formatted} | Код: {num_code}"
                )
                
                save_lead(user_contact, date_formatted, num_code)
                st.session_state.stage = 2
                st.rerun()
else:
    profile = CORE_DATA.get(st.session_state.num_code, CORE_DATA["default"])
    st.subheader(f"✨ {profile['title']}")
    
    # Показываем сферы жизни через надежные стандартные блоки Streamlit
    st.error(profile['psychology'])
    st.success(profile['advice'])
    
    st.write("---")
    st.subheader("🧪 Шаг II: Глубокое сканирование подсознания")
    
    r1 = st.radio(f"**1. {profile['q1']}**", profile['ans1'], key="radio_q1")
    t1 = st.text_input("Или распишите ответ своими словами (необязательно):", placeholder="Укажите причину тут...", key="text_q1")
    
    st.write("")
    
    r2 = st.radio(f"**2. {profile['q2']}**", profile['ans2'], key="radio_q2")
    t2 = st.text_input("Или дополните своими мыслями (необязательно):", placeholder="Опишите ваши чувства подробнее...", key="text_q2")
    
    # Кнопка-призыв к переходу в бот
    tg_share_link = "tg://resolve?domain=Lu4ek_bot&start=report"
    st.markdown(f'🌐 **[🔮 ХОЧЕШЬ УЗНАТЬ ПОЛНЫЙ РЕЗУЛЬТАТ? НАПИШИ БОТУ!]({tg_share_link})**')
    
    if st.button("📊 Скомпилировать экспресс-отчет на сайте"):
        idx = profile['ans1'].index(r1)
        final_report = profile['r'][idx]
        
        st.warning(final_report)
        
        if st.session_state.crm_db:
            st.session_state.crm_db[-1] += f" | Ответ 1: {r1} (Текст: {t1 if t1 else 'Нет'}) | Ответ 2: {r2} (Текст: {t2 if t2 else 'Нет'}) | Вердикт: {final_report}"
        
        send_results_to_admin(
            st.session_state.user_contact,
            st.session_state.user_birth_date_str,
            st.session_state.num_code,
            profile['q1'], r1, t1,
            profile['q2'], r2, t2,
            final_report
        )
        
        site_url = "https://oracle-by-lu4ek.streamlit.app/"
        share_text = f"Прошел Digital Oracle. Мой вердикт застоя: {final_report}\n\nПройти тест на сайте: {site_url}\nЗапустить чат-бот проекта: https://t.me"
        
        encoded_url = urllib.parse.quote(site_url)
        encoded_text = urllib.parse.quote(share_text)
        tg_share_link_msg = f"tg://msg_url?url={encoded_url}&text={encoded_text}"
        
        st.markdown(f'🚀 **[✈️ ПОДЕЛИТЬСЯ РЕЗУЛЬТАТОМ В TELEGRAM]({tg_share_link_msg})**')
        
    st.write("")
    if st.button("🔄 Рассчитать новую дату рождения"):
        st.session_state.stage = 1
        st.session_state.num_code = None
        st.rerun()

# --- ПАНЕЛЬ АДМИНИСТРАТОРА (HTML КАРТОЧКИ) ---
st.write("---")
with st.expander("🔑 Панель Администратора (CRM)"):
    if st.text_input("Введите мастер-пароль доступа:", type="password", key="admin_pwd_field") == "supersecret2026":
        st.success("🔒 Доступ к облачной базе данных разрешен!")
        
        if not st.session_state.crm_db:
            st.info("ℹ️ База данных пуста. Ожидание первого заполнения анкеты пользователем.")
        else:
            st.write("### 📊 Текущий поток клиентов:")
            for item in st.session_state.crm_db:
                st.info(item)
            
            crm_text = "\n".join(st.session_state.crm_db)
            st.download_button(
                label="📥 СКАЧАТЬ ПОЛНУЮ ТАБЛИЦУ В TXT/EXCEL",
                data=crm_text,
                file_name=f"oracle_leads_{datetime.now().strftime('%d_%m_%Y')}.txt",
                mime="text/plain"
            )
