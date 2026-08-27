import os
import streamlit as st
from datetime import date, datetime
from logic import get_combined_analysis, get_deep_test_for_number, calculate_dynamic_test_result

st.set_page_config(page_title="Oracle OS", page_icon="🔮", layout="centered")

# --- КАРТА ДИНАМИЧЕСКИХ ЦВЕТОВ ДЛЯ КАЖДОГО ЧИСЛА ---
COLOR_MAP = {
    "1": "#ff0055",  # Ярко-красный (Лидер)
    "2": "#00d2ff",  # Электрический синий (Дипломат)
    "3": "#d946ef",  # Неоновый фиолетовый (Творец — Ваш цвет)
    "4": "#00ff88",  # Кибер-зеленый (Мастер)
    "5": "#ff9f43",  # Оранжевый неон (Проводник)
    "6": "#ff7675",  # Розовый коралл (Наставник)
    "7": "#01cbc6",  # Бирюзовый (Стратег)
    "8": "#f1c40f",  # Золотой (Бизнес/Карма)
    "9": "#ffffff"   # Серебряно-белый (Мудрец)
}

# Base accent color before calculation (default deep purple)
current_accent_color = "#6c5ce7"

# Инициализация состояний сессии (память приложения)
if "stage" not in st.session_state: st.session_state.stage = 1
if "num_code" not in st.session_state: st.session_state.num_code = None
if "result_data" not in st.session_state: st.session_state.result_data = None

# Если число уже рассчитано, динамически меняем цвет интерфейса
if st.session_state.num_code in COLOR_MAP:
    current_accent_color = COLOR_MAP[st.session_state.num_code]

# --- КИБЕР-МИСТИЧЕСКИЙ ДИЗАЙН (CSS ИНЪЕКЦИЯ) ---
st.markdown(f"""
    <style>
        .stApp {{
            background-color: #0d0b18;
            color: #e0def2;
        }}
        /* Динамическая рамка вокруг полей ввода */
        .stTextInput input {{
            background-color: #16122c !important;
            color: {current_accent_color} !important;
            border: 1px solid {current_accent_color} !important;
            border-radius: 8px !important;
        }}
        /* Неоновые блоки результатов с динамическим цветом */
        .stInfo {{
            background-color: #1e1b4b !important;
            border-left: 5px solid {current_accent_color} !important;
            color: #e0e7ff !important;
            box-shadow: 0 0 15px {current_accent_color}33;
        }}
        .stSuccess {{
            background-color: #221133 !important;
            border-left: 5px solid {current_accent_color} !important;
            color: #fdf4ff !important;
            box-shadow: 0 0 15px {current_accent_color}44;
        }}
        /* Динамическая неоновая кнопка */
        .stButton button {{
            background: linear-gradient(90deg, {current_accent_color}, #0d0b18) !important;
            color: white !important;
            border-radius: 20px !important;
            border: 1px solid {current_accent_color} !important;
            font-weight: bold !important;
            box-shadow: 0 0 15px {current_accent_color}66;
            transition: 0.3s;
        }}
        .stButton button:hover {{
            box-shadow: 0 0 25px {current_accent_color}aa;
            transform: scale(1.02);
        }}
    </style>
""", unsafe_allow_html=True)


st.title("🔮 Digital Oracle OS")
st.write("🌌 Интеллектуальный краш-тест вашего сознания и разблокировка денежной энергии.")

# --- ЭТАП 1: ТЕКСТОВЫЙ ВВОД ДАТЫ (Защищен от сбоев и автопереводчиков) ---
if st.session_state.stage == 1:
    st.markdown("### 🪐 Шаг I: Точка входа в матрицу")
    with st.form("stage1_form"):
        user_date_str = st.text_input("Укажите вашу дату рождения в формате ДД.ММ.ГГГГ:", placeholder="24.10.1976")
        user_contact = st.text_input("Ваш Telegram-никнейм (для активации ключа):", placeholder="@username")
        
        if st.form_submit_button("🔑 Рассчитать Код Судьбы"):
            if not user_contact:
                st.error("Система требует контактные данные для верификации.")
            elif not user_date_str:
                st.error("Пожалуйста, укажите дату рождения.")
            else:
                try:
                    # ЖЕСТКАЯ ОЧИСТКА СТРОКИ (Удаляет опечатки, лишние точки и скрытые пробелы переводчика)
                    clean_date_str = user_date_str.strip().rstrip('.')
                    clean_date_str = "".join(clean_date_str.split())  
                    
                    # Конвертируем очищенный текст в объект даты
                    user_date = datetime.strptime(clean_date_str, "%d.%m.%Y").date()
                    
                    # Проверка корректности года
                    if user_date.year < 1920 or user_date.year > date.today().year:
                        st.error("Укажите корректный год рождения (от 1920).")
                    else:
                        # Магия бэкэнда: считаем число, пишем в файл, шлем в Telegram
                        num_code, result = get_combined_analysis(user_date, user_contact)
                        
                        # Сохраняем результаты в сессию и перезагружаем страницу
                        st.session_state.num_code = num_code
                        st.session_state.result_data = result
                        st.session_state.stage = 2
                        st.rerun()
                except ValueError:
                    st.error("❌ Неверный формат! Введите дату строго через точки. Пример: 24.10.1976")

# --- ЭТАП 2: ДИНАМИЧЕСКИЙ СВЯЗАННЫЙ ПСИХОЛОГИЧЕСКИЙ ТЕСТ ---
if st.session_state.stage == 2:
    st.header(f"✨ {st.session_state.result_data['title']}")
    
    st.markdown("#### 🧠 Базовый ментальный аудит:")
    st.info(st.session_state.result_data['psychology'])
    
    st.markdown("#### 🚀 Экспресс-шаг для прорыва застоя:")
    st.success(st.session_state.result_data['advice'])
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"### 🧪 Шаг II: Глубокое сканирование для Числа {st.session_state.num_code}")
    st.write("_Система адаптировала интерфейс и вопросы под ваш уникальный архетип._")
    
    # СВЯЗЫВАНИЕ: Извлекаем из JSON вопросы конкретно под это число судьбы
    dynamic_test = get_deep_test_for_number(st.session_state.num_code)
    user_choices = {}
    
    # Динамически выводим вопросы на экран
    for q in dynamic_test["questions"]:
        st.write(f"**{q['text']}**")
        choice = st.radio("Выберите траекторию:", list(q["answers"].keys()), key=f"dyn_q_{q['id']}")
        user_choices[q['id']] = choice
        st.markdown("<br>", unsafe_allow_html=True)
        
    if st.button("📊 Скомпилировать финальный отчет"):
        # Считаем баллы и выводим индивидуальный вердикт
        final_diagnosis = calculate_dynamic_test_result(st.session_state.num_code, user_choices)
        st.markdown("---")
        st.subheader("🏁 Итоговый системный вердикт:")
        st.warning(final_diagnosis)
        
        if st.button("Перезапустить систему"):
            st.session_state.stage = 1
            st.session_state.num_code = None
            st.session_state.result_data = None
            st.rerun()

# --- СЕКРЕТНАЯ АДМИН-ПАНЕЛЬ СКАЧИВАНИЯ БАЗЫ ---
st.markdown("<br><br><br><hr>", unsafe_allow_html=True)
with st.expander("🔑 Системный терминал (Admin)"):
    if st.text_input("Ввод пароля:", type="password", key="admin_pwd") == "supersecret2026":
        st.success("Доступ к логам открыт.")
        if os.path.exists("leads.txt"):
            with open("leads.txt", "rb") as file:
                st.download_button("📥 Выгрузить базу контактов", data=file, file_name="leads.txt")
