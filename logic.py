import json
from datetime import datetime
import requests

# ВСТАВЬТЕ СВОИ ДАННЫЕ СЮДА:
TELEGRAM_BOT_TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"
TELEGRAM_CHAT_ID = "ВАШ_CHAT_ID_ОТ_USERINFOBOT"

def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def calculate_numerology_number(birth_date):
    date_str = birth_date.strftime("%Y%m%d")
    digits_sum = sum(int(char) for char in date_str)
    while digits_sum > 9:
        digits_sum = sum(int(char) for char in str(digits_sum))
    return str(digits_sum)

def send_telegram_notification(contact, birth_date, num_key):
    formatted_date = birth_date.strftime("%d.%m.%Y")
    message = f"🔮 **Новый лид в Web App!**\n\n👤 **Контакт:** {contact}\n📅 **Дата:** {formatted_date}\n🔢 **Число:** {num_key}"
    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=5)
    except Exception:
        pass

def save_lead(contact, birth_date, num_key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_date = birth_date.strftime("%d.%m.%Y")
    with open("leads.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {contact} | {formatted_date} | Число: {num_key}\n")
    send_telegram_notification(contact, birth_date, num_key)

def get_combined_analysis(birth_date, contact):
    data = load_data()
    num_key = calculate_numerology_number(birth_date)
    save_lead(contact, birth_date, num_key)
    result_data = data.get("results", {}).get(num_key, {"title": f"Код {num_key}", "psychology": "В разработке.", "advice": "В разработке."})
    return num_key, result_data

def get_deep_test_for_number(num_key):
    data = load_data()
    tests = data.get("deep_tests_by_number", {})
    if num_key in tests:
        return tests[num_key]
    return tests.get("default", {"questions": [], "results": {}})

def calculate_dynamic_test_result(num_key, selected_answers):
    test_data = get_deep_test_for_number(num_key)
    results_block = test_data.get("results", {})
    
    total_score = 0
    for q in test_data.get("questions", []):
        user_choice = selected_answers.get(q["id"])
        total_score += q["answers"].get(user_choice, 0)
        
    if total_score <= 2:
        return results_block.get("low", "Анализ завершен успешно.")
    elif total_score <= 4:
        return results_block.get("medium", "Анализ завершен успешно.")
    else:
        return results_block.get("high", "Анализ завершен успешно.")
