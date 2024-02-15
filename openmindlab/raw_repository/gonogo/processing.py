import re
from . import pdf_reader

response_time_rect = (46.17, 314.15, 91.16, 331.59)  # Прямоугольник для "335ms"
accuracy_rect = (353.19, 314.15, 381.94, 331.59)  # Прямоугольник для "87%"
overall_score_rect = (268.75, 70.44, 277.29, 78.19)  # Прямоугольник для "3.5"
attempt_num_rect = (37.54, 74.79, 77.0, 82.24)  # Прямоугольник для "Attempt #84"
score_rect = (46.17, 167.96, 131.46, 191.95)

def extract_and_validate_numbers(obj):
    """
    Извлекает и валидирует числа из значений заданного словаря.

    :param obj: Словарь с текстовыми данными.
    :return: Словарь с извлеченными и валидированными числовыми значениями.
    """
    extracted_numbers = {}

    # Правила валидации для разных ключей
    validation_rules = {
        'response_time': r'(\d+)ms',  # целое число + ms
        'accuracy': r'(\d+)%',  # целое число + %
        'overall_score': r'(\d+(?:\.\d+)?)',  # целое или дробное число
        'attempt_num': r'Attempt #(\d+)',  # целое число после '#'
        'score': r'(\d+) points'  # целое число + points
    }

    for key, pattern in validation_rules.items():
        value = obj.get(key, '')
        match = re.search(pattern, value)
        if match:
            # Преобразование извлеченного значения в float, если это дробное число, иначе в int
            num_value = match.group(1)
            extracted_numbers[key] = float(num_value) if '.' in num_value else int(num_value)
        else:
            extracted_numbers[key] = None  # или другое значение по умолчанию для невалидных данных

    return extracted_numbers

def extract_info_from_gonogo_file(file_path):
  response_time_text = pdf_reader.extract_text_by_coordinates(file_path, response_time_rect)
  accuracy_text = pdf_reader.extract_text_by_coordinates(file_path, accuracy_rect)
  overall_score_text = pdf_reader.extract_text_by_coordinates(file_path, overall_score_rect)
  attempt_num_text = pdf_reader.extract_text_by_coordinates(file_path, attempt_num_rect)
  score_text = pdf_reader.extract_text_by_coordinates(file_path, score_rect)
  # print(response_time_text,accuracy_text, overall_score_text,attempt_num_text,score_text)
  return {
        'response_time': response_time_text,
        'accuracy': accuracy_text,
        'overall_score': overall_score_text,
        'attempt_num':attempt_num_text,
        'score':score_text
    }

def extract_info_from_gonogo_filename(filename):
    """
    Извлекает информацию из имени файла: первые 8 символов, число дней и время.

    :param filename: Имя файла в виде строки.
    :return: Словарь с извлеченной информацией.
    """
    # Извлечение первых 8 символов
    first_8_chars = filename[:8]

    # Поиск числа дней
    day_match = re.search(r'(\d+)day', filename)
    days = day_match.group(1) if day_match else None

    # Поиск числа, обозначающего время
    time_match = re.search(r'(\d+)time', filename)
    times = time_match.group(1) if time_match else None

    return {
        'respondentID': first_8_chars,
        'day': days,
        'times': times
    }