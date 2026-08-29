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

COLOR_MAP = {
    "1": "#ff0055", "2": "#00d2ff", "3": "#d946ef", "4": "#00ff88", 
    "5": "#ff9f43", "6": "#ff7675", "7": "#01cbc6", "8": "#f1c40f", "9": "#ffffff"
}
current_accent_color = "#6c5ce7"

# --- ИНИЦИАЛИЗАЦИЯ БЕЗОПАСНОЙ ПАМЯТИ CRM ВНУТРИ ОБЛАКА ---
if "stage" not in st.session_state: st.session_state.stage = 1
if "num_code" not in st.session_state: st.session_state.num_code = None
if "user_contact" not in st.session_state: st.session_state.user_contact = ""
if "user_birth_date_str" not in st.session_state: st.session_state.user_birth_date_str = ""
if "crm_db" not in st.session_state: st.session_state.crm_db = []

if st.session_state.num_code in COLOR_MAP:
    current_accent_color = COLOR_MAP[st.session_state.num_code]

# --- ИНЪЕКЦИЯ КОНТРАСТНОГО НЕОНОВОГО ДИЗАЙНА (CSS) ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: #0d0b18; color: #e0def2; }}
        .stTextInput input, div[data-testid="stDateInput"] input {{ background-color: #16122c !important; color: {current_accent_color} !important; border: 1px solid {current_accent_color} !important; border-radius: 8px !important; }}
        .stButton button {{ background: linear-gradient(90deg, {current_accent_color}, #0d0b18) !important; color: white !important; border-radius: 20px !important; border: 1px solid {current_accent_color} !important; font-weight: bold !important; }}
        div[data-testid="stRadio"] {{ background-color: #1c1936 !important; padding: 15px !important; border-radius: 10px !important; border: 1px solid {current_accent_color}44 !important; }}
        
        /* ЖЕСТКОЕ ОКРАШИВАНИЕ ВОПРОСОВ ДЛЯ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ */
        h4, h5, p, label, div[data-testid="stMarkdownContainer"] p {{
            color: {current_accent_color} !important;
            font-weight: bold !important;
        }}
        
        .neon-box {{
            background-color: #16122c !important;
            padding: 18px !important;
            border-radius: 10px !important;
            margin-bottom: 15px !important;
            word-wrap: break-word !important;
            white-space: normal !important;
            line-height: 1.5 !important;
        }}
    </style>
""", unsafe_allow_html=True)

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

st.markdown("<h1 style='text-align: center; color:#ffffff !important;'>🔮 Digital Oracle OS</h1>", unsafe_allow_html=True)

if st.session_state.stage == 1:
    st.markdown("### 🪐 Шаг I: Творение персональной матрицы")
    with st.form("stage1_form"):
        # ИСПРАВЛЕНО ДЛЯ СТАРЫХ ВЕРСИЙ СЕРВЕРА: выставлена базовая дата 01.01.2000
        user_date = st.date_input("Выберите вашу дату рождения:", value=date(2000, 1, 1), min_value=date(1920, 1, 1), max_value=date.today())
        user_contact = st.text_input("Ваш Telegram-никнейм для активации ключа:", placeholder="@username")
        if st.form_submit_button("🔑 Рассчитать Код Судьбы"):
            # Проверка, изменил ли пользователь дефолтную проверочную дату
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
                
                # Запись в CRM-список
                st.session_state.crm_db.append(
                    f"Запись: {datetime.now().strftime('%d.%m.%Y %H:%M')} | Юзер: {user_contact} | Дата: {date_formatted} | Код: {num_code}"
                )
                
                save_lead(user_contact, date_formatted, num_code)
                st.session_state.stage = 2
                st.rerun()
else:
    profile = CORE_DATA.get(st.session_state.num_code, CORE_DATA["default"])
    st.header(f"✨ {profile['title']}")
    
    st.markdown(f"""
        <div class="neon-box" style="border-left: 5px solid #ff0055;">
            <span style="color: #ff0055; font-weight: bold; font-size: 15px;">{profile['psychology']}</span>
        </div>
        <div class="neon-box" style="border-left: 5px solid #00ff88;">
            <span style="color: #00ff88; font-weight: bold; font-size: 15px;">{profile['advice']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🧪 Шаг II: Глубокое сканирование подсознания")
    
    st.markdown(f"#### 🔘 1. {profile['q1']}")
    r1 = st.radio("Варианты ответа:", profile['ans1'], key="radio_q1", label_visibility="collapsed")
    t1 = st.text_input("Или распишите ответ своими словами (необязательно):", placeholder="Укажите причину тут...", key="text_q1")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"#### 🔘 2. {profile['q2']}")
    r2 = st.radio("Варианты ответа:", profile['ans2'], key="radio_q2", label_visibility="collapsed")
    t2 = st.text_input("Или дополните своими мыслями (необязательно):", placeholder="Опишите ваши чувства подробнее...", key="text_q2")
    
    # КНОПКА ПРИЗЫВА К БОТУ С ПРЯМЫМ ДИПЛИНКОМ
    st.markdown(f"""
        <div style="text-align: center; margin: 25px auto; width: 100%;">
            <a href="tg://resolve?domain=Lu4ek_bot&start=report" style="text-decoration: none;">
                <div style="background: linear-gradient(90deg, #d946ef, #ff0055); color: white !important; text-align: center; padding: 14px 20px; border-radius: 25px; font-weight: bold; font-size: 15px; box-shadow: 0 0 20px rgba(217, 70, 239, 0.6); border: 1px solid #ffffff33;">
                    🔮 ХОЧЕШЬ УЗНАТЬ ПОЛНЫЙ РЕЗУЛЬТАТ? НАПИШИ БОТУ!
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Скомпилировать экспресс-отчет на сайте"):
        idx = profile['ans1'].index(r1)
        final_report = profile['r'][idx]
        
        st.markdown(f"""
            <div class="neon-box" style="border: 2px solid #f1c40f; background-color: #221a35 !important; margin-top: 15px;">
                <span style="color: #ffffff; font-weight: bold; font-size: 15px;">{final_report}</span>
            </div>
        """, unsafe_allow_html=True)
        
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
        tg_share_link = f"tg://msg_url?url={encoded_url}&text={encoded_text}"
        
        st.markdown(f"""
            <a href="{tg_share_link}" target="_blank" style="text-decoration: none;">
