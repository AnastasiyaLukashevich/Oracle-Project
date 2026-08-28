import os
import streamlit as st
from datetime import datetime
import requests
import urllib.parse

st.set_page_config(page_title="Oracle OS", page_icon="🔮", layout="centered")

# --- СНАЙПЕРСКИ НАСТРОЕННЫЕ ДАННЫЕ БОТА ---
TELEGRAM_BOT_TOKEN = "7786619038:AAH2qq60z-m1NB9b6IHJuQrGk1irSesGu10"
TELEGRAM_CHAT_ID = "982947729"

COLOR_MAP = {"1": "#ff0055", "2": "#00d2ff", "3": "#d946ef", "4": "#00ff88", "5": "#ff9f43", "6": "#ff7675", "7": "#01cbc6", "8": "#f1c40f", "9": "#ffffff"}
current_accent_color = "#6c5ce7"

if "stage" not in st.session_state: st.session_state.stage = 1
if "num_code" not in st.session_state: st.session_state.num_code = None
if "error_text" not in st.session_state: st.session_state.error_text = None

if st.session_state.num_code in COLOR_MAP:
    current_accent_color = COLOR_MAP[st.session_state.num_code]

st.markdown(f"""
    <style>
        .stApp {{ background-color: #0d0b18; color: #e0def2; }}
        .stTextInput input {{ background-color: #16122c !important; color: {current_accent_color} !important; border: 1px solid {current_accent_color} !important; border-radius: 8px !important; }}
        .stInfo {{ background-color: #1e1b4b !important; border-left: 5px solid {current_accent_color} !important; }}
        .stSuccess {{ background-color: #221133 !important; border-left: 5px solid {current_accent_color} !important; }}
        .stButton button {{ background: linear-gradient(90deg, {current_accent_color}, #0d0b18) !important; color: white !important; border-radius: 20px !important; border: 1px solid {current_accent_color} !important; font-weight: bold !important; }}
        .stTextInput input::placeholder {{ color: #b2bec3 !important; opacity: 1 !important; }}
        div[data-testid="stRadio"] {{ background-color: #1c1936 !important; padding: 15px !important; border-radius: 10px !important; border: 1px solid {current_accent_color}44 !important; }}
        div[data-testid="stNotification"] {{ background-color: #2a244d !important; color: #ffffff !important; border-radius: 12px !important; border: 2px solid #f1c40f !important; box-shadow: 0 0 20px rgba(241, 196, 15, 0.2); }}
        div[data-testid="stNotification"] p {{ color: #ffffff !important; font-size: 16px !important; font-weight: 500 !important; }}
    </style>
""", unsafe_allow_html=True)

CORE_DATA = {
    "3": {
        "title": "Код Судьбы: 3 — Творец и Изобилие", 
        "psychology": "Ваш финансовый застой — это заблокированная созидательная энергия. Как Тройка, вы не можете быть просто исполнителем. Вам необходимо создавать свои продукты, писать тексты и управлять процессами.", 
        "advice": "Прекратите копить знания в голове. Переводите мысли в осязаемую форму — пишите коды, создавайте тексты, выпускайте продукт в мир.", 
        "q1": "Куда вы сливаете энергию созидания?", "ans1": ["В бесконечные доработки", "В бытовую рутину", "В чужие проекты"], 
        "q2": "Какая среда для написания текстов ближе?", "ans2": ["Одиночество и тишина", "Кафе среди людей", "Жесткий график"], 
        "r": ["Ваш творческий застой — это истощение матрицы. Нужна эстетика.", "Вы застряли в ловушке улучшений. Выпускайте MVP.", "Идеальный баланс! Энергия находится в зените."]
    },
    "default": {
        "title": "Код Судьбы: Расчет завершен", 
        "psychology": "Ваш финансовый застой — это временная блокировка созидательной энергии. Текущий цикл требует от вас переоценки ценностей.", 
        "advice": "Переводите мысли в осязаемую форму. Запустите этот базовый ИТ-продукт, чтобы пробить ментальный застой.", 
        "q1": "Что блокирует ваше движение вперед?", "ans1": ["Страх критических замечаний", "Привычка к чужому графику", "Синдром самозванца"], 
        "q2": "Что чувствуете при мысли о деньгах?", "ans2": ["Обида на текущую систему", "Страх, что ресурсы закончатся", "Азарт и понимание масштаба"], 
        "r": ["Вам необходим жесткий фокус на личной независимости.", "Вы застряли в накоплении информации. Начните действовать.", "Отличный фундамент. Система готова к масштабированию."]
    }
}

def calculate_numerology_number(birth_date):
    date_str = birth_date.strftime("%Y%m%d")
    digits_sum = sum(int(char) for char in date_str)
    while digits_sum > 9: digits_sum = sum(int(char) for char in str(digits_sum))
    return str(digits_sum)

def save_lead(contact, birth_date, num_key):
    try:
        msg = f"🔮 **Новый лид в Web App!**\n\n👤 **Контакт:** {contact}\n📅 **Дата:** {birth_date.strftime('%d.%m.%Y')}\n🔢 **Число:** {num_key}"
        requests.post(f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage", json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass
    with open("leads.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {contact} | {birth_date.strftime('%d.%m.%Y')} | {num_key}\n")

st.markdown("<h1 style='text-align: center;'>🔮 Digital Oracle OS</h1>", unsafe_allow_html=True)

# --- ШАГ I ---
if st.session_state.stage == 1:
    st.markdown("### 🪐 Шаг I: Точка входа в матрицу")
    user_date_str = st.text_input("Укажите вашу дату рождения в формате ДД.ММ.ГГГГ:", placeholder="05.08.1997", key="input_date")
    user_contact = st.text_input("Ваш Telegram-никнейм (для активации ключа):", placeholder="@username", key="input_contact")
    
    if st.button("🔑 Рассчитать Код Судьбы", key="btn_submit1"):
        if not user_contact or not user_date_str: 
            st.session_state.error_text = "Заполните все поля."
        else:
            try:
                clean_str = "".join(user_date_str.strip().rstrip('.').split())
                user_date = datetime.strptime(clean_str, "%d.%m.%Y").date()
                num_code = calculate_numerology_number(user_date)
                
                save_lead(user_contact, user_date, num_code)
                st.session_state.num_code = num_code
                st.session_state.error_text = None  
                st.session_state.stage = 2
                st.rerun()
            except:
                st.session_state.error_text = "❌ Неверный формат даты! Введите строго через точки. Пример: 05.08.1997"

    if st.session_state.error_text and st.session_state.num_code is None:
        st.error(st.session_state.error_text)

# --- ШАГ II ---
if st.session_state.stage == 2:
    profile = CORE_DATA.get(st.session_state.num_code, CORE_DATA["default"])
    st.header(f"✨ {profile['title']}")
    st.info(profile['psychology'])
    st.success(profile['advice'])
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"### 🧪 Шаг II: Глубокое сканирование")
    
    c1 = st.radio(f"**1. {profile['q1']}**", profile['ans1'], key="radio_q1")
    st.markdown("<br>", unsafe_allow_html=True)
    c2 = st.radio(f"**2. {profile['q2']}**", profile['ans2'], key="radio_q2")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📊 Скомпилировать финальный отчет", key="submit_stage2"):
        idx = (profile['ans1'].index(c1) + profile['ans2'].index(c2)) % 3
        st.markdown("---")
        final_report = profile['r'][idx]
        st.warning(final_report)
        
        # ЖЕСТКАЯ СБОРКА АДРЕСА ПО СТАНДАРТУ TELEGRAM БЕЗ ОПЕЧАТОК ОДНОЙ СТРОКОЙ:
        tg_share_link = f"https://t.me" + urllib.parse.quote(f"Прошел Digital Oracle. Мой вердикт застоя: {final_report} Разблокируй свой код в боте @Lu4ek_bot")
        
        st.link_button("✈️ Поделиться результатом в Telegram", tg_share_link, type="primary")
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🪐 Начать новый расчет", key="reset_app"):
        st.session_state.stage = 1
        st.session_state.num_code = None
        st.session_state.error_text = None  
        st.rerun()

# --- СЕКРЕТНАЯ АДМИНКА ---
st.markdown("<br><br><hr>", unsafe_allow_html=True)
with st.expander("🔑 Admin"):
    if st.text_input("Пароль:", type="password", key="admin_password") == "supersecret2026" and os.path.exists("leads.txt"):
        with open("leads.txt", "rb") as file: st.download_button("📥 Скачать базу контактов", data=file, file_name="leads.txt", key="download_leads")
