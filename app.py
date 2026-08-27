import os
import streamlit as st
from datetime import date
from logic import get_combined_analysis, get_deep_test_for_number, calculate_dynamic_test_result

st.set_page_config(page_title="Oracle OS", page_icon="🔮", layout="centered")

COLOR_MAP = {
    "1": "#ff0055", "2": "#00d2ff", "3": "#d946ef", "4": "#00ff88", 
    "5": "#ff9f43", "6": "#ff7675", "7": "#01cbc6", "8": "#f1c40f", "9": "#ffffff"
}
current_accent_color = "#6c5ce7"

if "stage" not in st.session_state: st.session_state.stage = 1
if "num_code" not in st.session_state: st.session_state.num_code = None
if "result_data" not in st.session_state: st.session_state.result_data = None

if st.session_state.num_code in COLOR_MAP:
    current_accent_color = COLOR_MAP[st.session_state.num_code]

st.markdown(f"""
    <style>
        .stApp {{ background-color: #0d0b18; color: #e0def2; }}
        .stTextInput input, .stDateInput input {{
            background-color: #16122c !important; color: {current_accent_color} !important;
            border: 1px solid {current_accent_color} !important; border-radius: 8px !important;
        }}
        .stInfo {{ background-color: #1e1b4b !important; border-left: 5px solid {current_accent_color} !important; box-shadow: 0 0 15px {current_accent_color}33; }}
        .stSuccess {{ background-color: #221133 !important; border-left: 5px solid {current_accent_color} !important; box-shadow: 0 0 15px {current_accent_color}44; }}
        .stButton button {{
            background: linear-gradient(90deg, {current_accent_color}, #0d0b18) !important; color: white !important;
            border-radius: 20px !important; border: 1px solid {current_accent_color} !important; font-weight: bold !important; box-shadow: 0 0 15px {current_accent_color}66;
        }}
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Digital Oracle OS")

if st.session_state.stage == 1:
    st.markdown("### 🪐 Шаг I: Точка входа в матрицу")
    with st.form("stage1_form"):
        user_date = st.date_input("Укажите вашу дату рождения:", value=date(1997, 8, 5))
        user_contact = st.text_input("Ваш Telegram-никнейм:", placeholder="@username")
        if st.form_submit_button("🔑 Рассчитать Код Судьбы"):
            if not user_contact: st.error("Система требует контактные данные.")
            else:
                num_code, result = get_combined_analysis(user_date, user_contact)
                st.session_state.num_code = num_code
                st.session_state.result_data = result
                st.session_state.stage = 2
                st.rerun()

if st.session_state.stage == 2:
    st.header(f"✨ {st.session_state.result_data['title']}")
    st.info(st.session_state.result_data['psychology'])
    st.success(st.session_state.result_data['advice'])
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"### 🧪 Шаг II: Сканирование для Числа {st.session_state.num_code}")
    
    dynamic_test = get_deep_test_for_number(st.session_state.num_code)
    user_choices = {}
    for q in dynamic_test["questions"]:
        st.write(f"**{q['text']}**")
        choice = st.radio("Выберите траекторию:", list(q["answers"].keys()), key=f"dyn_q_{q['id']}")
        user_choices[q['id']] = choice
        st.markdown("<br>", unsafe_allow_html=True)
        
    if st.button("📊 Скомпилировать финальный отчет"):
        final_diagnosis = calculate_dynamic_test_result(st.session_state.num_code, user_choices)
        st.warning(final_diagnosis)
        if st.button("Перезапустить систему"):
            st.session_state.stage = 1
            st.session_state.num_code = None
            st.session_state.result_data = None
            st.rerun()

st.markdown("<br><br><br><hr>", unsafe_allow_html=True)
with st.expander("🔑 Системный терминал (Admin)"):
    if st.text_input("Ввод пароля:", type="password", key="admin_pwd") == "supersecret2026":
        st.success("Доступ к логам открыт.")
        if os.path.exists("leads.txt"):
            with open("leads.txt", "rb") as file:
                st.download_button("📥 Выгрузить базу контактов", data=file, file_name="leads.txt")
