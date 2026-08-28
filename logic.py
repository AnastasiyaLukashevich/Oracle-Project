# Полностью замените функцию в самом низу файла logic.py:

def calculate_dynamic_test_result(num_key, selected_answers):
    """
    Улучшенный расчет результатов Шага II.
    Защищен от ошибок KeyError.
    """
    test_data = get_deep_test_for_number(num_key)
    results_block = test_data.get("results", {})
    
    total_score = 0
    for q in test_data.get("questions", []):
        user_choice = selected_answers.get(q["id"])
        total_score += q["answers"].get(user_choice, 0)
        
    # Прямая и безопасная привязка к ключам в data.json
    if total_score <= 2:
        return results_block.get("low", "Анализ завершен успешно.")
    elif total_score <= 4:
        return results_block.get("medium", "Анализ завершен успешно.")
    else:
        return results_block.get("high", "Анализ завершен успешно.")
