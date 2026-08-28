import os
import streamlit as st
from datetime import datetime
import requests
import urllib.parse  # Библиотека для безопасного кодирования текста ссылки

st.set_page_config(page_title="Oracle OS", page_icon="🔮", layout="centered")

# --- НАСТРОЙКА TELEGRAM БОТА (Впишите свои данные в кавычках) ---
TELEGRAM_BOT_TOKEN = "7786619038:AAGDbcMRh7sLbfMsYwAgBG4Ro7tho9AvJNk"
TELEGRAM_CHAT_ID = "@Lu4ek_bot"

COLOR_MAP = {"1": "#ff0055", "2": "#00d2ff", "3": "#d946ef", "4": "#00ff88", "5": "#ff9f43", "6": "#ff7675", "7": "#01cbc6", "8": "#f1c40f", "9": "#ffffff"}
current_accent_color = "#6c5ce7"

if "stage" not in st.session_state: st.session_state.stage = 1
if "num_code" not in st.session_state: st.session_state.num_code = None

if st.session_state.num_code in COLOR_MAP:
    current_accent_color = COLOR_MAP[st.session_state.num_code]

st.markdown(f"""
    <style>
        .stApp {{ background-color: #0d0b18; color: #e0def2; }}
        .stTextInput input {{ background-color: #16122c !important; color: {current_accent_color} !important; border: 1px solid {current_accent_color} !important; border-radius: 8px !important; }}
        .stInfo {{ background-color: #1e1b4b !important; border-left: 5px solid {current_accent_color} !important; }}
        .stSuccess {{ background-color: #221133 !important; border-left: 5px solid {current_accent_color} !important; }}
        .stButton button {{ background: linear-gradient(90deg, {current_accent_color}, #0d0b18) !important; color: white !important; border-radius: 20px !important; border: 1px solid {current_accent_color} !important; font-weight: bold !important; }}
        
        .stTextInput input::placeholder {{
            color: #b2bec3 !important;
            opacity: 1 !important;
        }}
        
        div[data-testid="stRadio"] {{
            background-color: #1c1936 !important;
            padding: 15px !important;
            border-radius: 10px !important;
            border: 1px solid {current_accent_color}44 !important;
            box-shadow: 0 0 10px {current_accent_color}11;
        }}
    </style>
""", unsafe_allow_html=True)

P_3 = "Ваш финансовый застой — это заблокированная созидательная энергия. Как Тройка, вы не можете быть просто исполнителем. Вам необходимо создавать свои продукты, писать тексты и управлять процессами."
A_3 = "Прекратите копить знания в голове. Переводите мысли в осязаемую форму — пишите коды, создавайте тексты, выпускайте продукт в мир."
P_DEF = "Ваш финансовый застой — это временная блокировка созидательной энергии. Текущий цикл требует от вас переоценки ценностей и автоматизации процессов."
A_DEF = "Переводите мысли в осязаемую форму. Запустите этот базовый ИТ-продукт, чтобы пробить ментальный застой."

CORE_DATA = {
    "3": {
        "title": "Код Судьбы: 3 — Творец и Изобилие", "psychology": P_3, "advice": A_3,
        "q1": "Куда вы сливаете энергию созидания?", "ans1": ["В бесконечные доработки", "В бытовую рутину", "В чужие проекты"],
        "q2": "Какая среда для написания текстов ближе?", "ans2": ["Одиночество и тишина", "Кафе среди людей", "Жесткий график"],
        "r": ["Ваш творческий застой — это истощение матрицы. Нужна эстетика.", "Вы застряли в ловушке улучшений. Выпускайте MVP.", "Идеальный баланс! Энергия находится в зените."]
    },
    "default": {
        "title": "Код Судьбы: Расчет завершен", "psychology": P_DEF, "advice": A_DEF,
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
        msg = f"🔮 Новый лид!\n👤 Контакт: {contact}\n📅 Дата: {birth_date.strftime('%d.%m.%Y')}\n🔢 Число: {num_key}"
        requests.post(f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage", json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=5)
    except: pass
    with open("leads.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {contact} | {birth_date.strftime('%d.%m.%Y')} | {num_key}\n")

st.markdown("<h1 style='text-align: center;'>🔮 Digital Oracle OS</h1>", unsafe_allow_html=True)

# --- ЭТАП 1 ---
if st.session_state.stage == 1:
    with st.form("stage1_form"):
        user_date_str = st.text_input("Укажите вашу дату рождения в формате ДД.ММ.ГГГГ:", placeholder="05.08.1997")
        user_contact = st.text_input("Ваш Telegram-никнейм (для активации ключа):", placeholder="@username")
        if st.form_submit_button("🔑 Рассчитать Код Судьбы"):
            if not user_contact or not user_date_str: 
                st.error("Заполните все поля.")
            else:
                try:
                    clean_str = "".join(user_date_str.strip().rstrip('.').split())
                    user_date = datetime.strptime(clean_str, "%d.%m.%Y").date()
                    num_code = calculate_numerology_number(user_date)
                    save_lead(user_contact, user_date, num_code)
                    st.session_state.num_code = num_code
                    st.session_state.stage = 2
                    st.rerun()
                except: 
                    st.error("❌ Неверный формат! Пример: 05.08.1997")

# --- ЭТАП 2 ---
if st.session_state.stage == 2:
    profile = CORE_DATA.get(st.session_state.num_code, CORE_DATA["default"])
    st.header(f"✨ {profile['title']}")
    st.info(profile['psychology'])
    st.success(profile['advice'])
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"### 🧪 Шаг II: Глубокое сканирование")
    
    c1 = st.radio(f"**1. {profile['q1']}**", profile['ans1'])
    st.markdown("<br>", unsafe_allow_html=True)
    c2 = st.radio(f"**2. {profile['q2']}**", profile['ans2'])
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📊 Скомпилировать финальный отчет"):
        idx = (profile['ans1'].index(c1) + profile['ans2'].index(c2)) % 3
        st.markdown("---")
        
        final_report = profile['r'][idx]
        st.warning(final_report)
        
        # Текст, который улетит в Telegram получателю
        raw_text = f"Прошел Digital Oracle. Мой вердикт застоя: {final_report} Узнай свой код силы по ссылке:"
        encoded_text = urllib.parse.quote(raw_text)
        
        # Ссылка на ваш текущий сайт (берется автоматически или жестко)
        site_url = "https://streamlit.app" # Укажите здесь точную ссылку на ваш сайт, если она другая
        
        # Формируем железно рабочую ссылку-шер для Telegram
        tg_share_link = f"https://t.me{site_url}&text={encoded_text}"
        
        # --- КНОПКА ПОДЕЛИТЬСЯ ЧЕРЕЗ TELEGRAM ---
        st.markdown(f"""
            <a href="{tg_share_link}" target="_blank" style="text-decoration: none;">
                <div style="
                    background: linear-gradient(90deg, #6c5ce7, #d946ef);
                    color: white;
                    text-align: center;
                    padding: 12px 20px;
                    border-radius: 20px;
                    font-weight: bold;
                    width: 90%;
                    box-shadow: 0 0 15px rgba(217, 70, 239, 0.4);
                    margin: 15px auto 25px auto;
                ">
                    ✈️ Поделиться результатом в Telegram
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("Перезапустить систему"):
            st.session_state.stage = 1
            st.session_state.num_code = None
            st.rerun()

st.markdown("<br><br><hr>", unsafe_allow_html=True)
with st.expander("🔑 Admin"):
    if st.text_input("Пароль:", type="password") == "supersecret2026" and os.path.exists("leads.txt"):
        with open("leads.txt", "rb") as file: st.download_button("📥 Скачать базу", data=file, file_name="leads.txt")
