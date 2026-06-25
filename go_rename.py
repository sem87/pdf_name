import os
import re
import shutil
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from read_xl import poisk_data
from logi.logi import logger
# ====================НАЧАЛО НАСТРОЙКИ ============================
INPUT_FOLDER = "do"
OUTPUT_FOLDER = "do_renamed"
DPI = 300
TESSERACT_LANG = 'rus'
TESSERACT_CONFIG = '--psm 6'
# ==================== КОНЕЦ НАСТРОЙКИ ================================
# ==================== НАЧАЛО РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ ====================
# Разрешаем только кириллицу и цифры
config = '-c tessedit_char_whitelist=АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯабвгдежзиклмнопрстуфхцчшщэюя0123456789: '

# # Общие паттерны OCR-искажений для кириллицы
# OCR_CYRILLIC_PATTERNS = {
#     'а': '[аa]', 'е': '[еe]', 'о': '[оo]', 'р': '[рp]', 'с': '[сc]',
#     'у': '[уy]', 'х': '[хx]', 'н': '[нh]', 'к': '[кk]', 'м': '[мm]',
#     'т': '[тt]', 'в': '[вb]', 'д': '[дg]', 'з': '[з3]', 'и': '[иu]',
#     'л': '[лn]', 'п': '[пn]', 'ф': '[фo]', 'б': '[б6]', 'г': '[гr]',
#     'я': '[яa]', 'ю': '[юo]', 'ч': '[ч4]', 'ш': '[шw]', 'щ': '[щw]',
#     'э': '[э3]', 'ж': '[жx]', 'ц': '[цu]', 'й': '[йu]', 'ь': '[ьb]',
#     'ъ': '[ъb]', 'ё': '[ёe]',
# }
# Дата проведения измерений
regex_date = re.compile(
    r"(?i)(?:дата\s+проведения\s+измерений|"
    r"[aа]т[аа]\s+[iі]р[оo]в[еe]д[еe]н[иі]я\s+[мm]3[мm]ер[еe]н[иі]й|"
    r"[aа]т[аа]\s+.*?[мm]3[мm]ер[еe]н[иі]й)"
    r"\s*[:：]\s*"
    r"(\d{2}[\.]\d{2}[\.]\d{4})",
    re.IGNORECASE
)

# Инвентарный номер
# regex_inventory = re.compile(
#     r"(?i)(?:инвентарный\s+номер|"
#     r"[iі][нн][вв][еe][нн][тt][аa][рр][нн][ыы][йй]\s+[нн][оo][мm][еe][рр])"
#     r"\s*[:：]\s*"
#     r"([A-Za-zА-Яа-я0-9\-]{3,20}?)"
#     r"(?=\s*(?:[сc][еe][рр][иі][йй][нн][ыы][йй]|"
#     r"[сc][еe][рр][иі][йй][нн][ыы][йй]\s+[нн][оo][мm][еe][рр]|"
#     r"$))",
#     re.IGNORECASE
# )
regex_inventory = re.compile(
    r"Инвентарный\s+номер\s*[:：]\s*"
    r"(БАШ[А-ЯA-Z0-9ОO]{3,10})",
    re.IGNORECASE | re.UNICODE
)
# regex_inventory = re.compile(
#     r"Инвентарный\s+номер\s*[:：]\s*"      # Метка "Инвентарный номер:"
#     r"(БАШ\d{3,10})",                      # Номер: БАШ + 3-10 цифр
#     re.IGNORECASE | re.UNICODE
# )
# ==================== КОНЕЦ РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ =================
# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================
def clean_ocr_text(text: str) -> str:
    """Норм OCR-текст:замлатиницу на кириллицу в русских словах.Работает на уровне символов, а не целых слов."""
    if not text:
        return text
    # Маппинг: латинский символ → кириллический (похожие по начертанию)
    latin_to_cyrillic = {
        'A': 'А', 'B': 'В', 'C': 'С', 'E': 'Е', 'H': 'Н',
        'K': 'К', 'M': 'М', 'O': 'О', 'P': 'Р', 'T': 'Т',
        'X': 'Х', 'Y': 'У',
        'a': 'а', 'c': 'с', 'e': 'е', 'o': 'о', 'p': 'р',
        'x': 'х', 'y': 'у',
    }
    # Простая замена (может сломать английский текст!)
    result = text
    for latin, cyrillic in latin_to_cyrillic.items():
        result = result.replace(latin, cyrillic)
    return result

def clean_filename(name: str) -> str:
    """Очищает строку от недопустимых для имени файла символов"""
    if not name or name == "Неизвестно":
        return "Неизвестно"

    # Удаляем недопустимые символы
    name = re.sub(r'[\\/*?:"<>|\n\r]', "", name)

    # Заменяем пробелы на подчёркивания
    name = re.sub(r'\s+', '_', name)

    # Удаляем прилипшие слова из OCR
    name = re.sub(
        r'_*(?:изготовитель|H3rOTOBHTeJIB|серийный|Cepийный|CepHiHbIn|'
        r'инвентарный|HBeHTapHbIi|телевизионный|TeJIeBH3HOHHbIi).*',
        '', name, flags=re.IGNORECASE
    )

    # Удаляем множественные подчёркивания
    name = re.sub(r'_+', '_', name)

    return name.strip('_')

def extract_field(regex: re.Pattern, text: str, field_name: str) -> str:
    """Извлекает поле из текста с помощью регулярного выражения"""
    # search() ищет первое совпадение в тексте. Если нужно найти все — используйте findall()
    match = regex.search(text)
    if match:
        value = match.group(1).strip()
        return value
    else:
        logger.warning(f"{field_name}:НЕ НАЙДЕНО!!!")
        return "Неизвестно"


def normalize_bash_inventory_number(raw_string):
    """
    Преобразует строку инвентарного номера к виду БАШ + только цифры.
    Заменяет похожие на цифры буквы (O→0, з→3 и т.д.)
    """
    # Извлекаем часть после БАШ
    match = re.search(r'БАШ(.*)', raw_string, re.IGNORECASE)
    if not match:
        return None
    suffix = match.group(1)
    # Заменяем типичные OCR-ошибки: буквы, похожие на цифры
    suffix = re.sub(r'[ОоOo]', '0', suffix)  # О, о, O, o → 0
    suffix = re.sub(r'[ЗзZz]', '3', suffix)  # З, з, Z, z → 3
    suffix = re.sub(r'[IiІіlL]', '1', suffix)  # I, i, І, і, l, L → 1
    suffix = re.sub(r'[Ss]', '5', suffix)  # S, s → 5
    suffix = re.sub(r'[Bb]', '8', suffix)  # B, b → 8
    suffix = re.sub(r'[Ggб]', '6', suffix)  # G, g, б → 6
    suffix = re.sub(r'[Tt]', '7', suffix)  # T, t → 7
    suffix = re.sub(r'[AaДд]', '4', suffix)  # A, a, Д, д → 4
    # Оставляем только цифры
    digits_only = re.sub(r'\D', '', suffix)
    return f'БАШ{digits_only}'

def check_dependencies():
    """Проверяет наличие необходимых зависимостей"""
    # Проверка Tesseract  есть или нет (распознает текст)
    try:
        tesseract_cmd = shutil.which('tesseract')
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            # logger.info(f"✅ Tesseract найден: {tesseract_cmd}")
        else:
            logger.warning("Tesseract не найден в PATH. Установите tesseract-ocr")
    except Exception as e:
        logger.error(f"Ошибка проверки Tesseract: {e}")
    # Проверка папок
    if not os.path.exists(INPUT_FOLDER):
        logger.error(f"Папка ввода '{INPUT_FOLDER}' не существует!")
        return False
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    # logger.info(f"✅ Папка вывода '{OUTPUT_FOLDER}' готова")
    return True


# ==================== НАЧАЛО ОСНОВНАЯ ФУНКЦИЯ ====================
def process_pdfs():
    """Обрабатывает PDF-файлы и переименовывает их, благодаря xl таблице"""
    # Проверка зависимостей
    if not check_dependencies():
        return
    # Получаем список PDF-файлов
    pdf_files = sorted([f for f in os.listdir(INPUT_FOLDER)if f.lower().endswith(".pdf")])
    if not pdf_files:
        logger.warning(f"️В папке '{INPUT_FOLDER}' не найдено PDF-файлов")
        return
    logger.info(f"==============================================\n")
    logger.info(f"Найдено файлов для обработки: {len(pdf_files)}\n")

    success_count = 0
    error_count = 0
    for filename in pdf_files:
        file_path = os.path.join(INPUT_FOLDER, filename)
        logger.info(f"Обработка: {filename}")
        try:
            # Конвертация PDF в изображение
            images = convert_from_path(file_path,first_page=1,last_page=1,dpi=DPI)
            if not images:
                logger.warning(f"Не удалось конвертировать {filename}\n")
                error_count += 1
                continue
            # OCR распознавание
            text = pytesseract.image_to_string(images[0],lang=TESSERACT_LANG,config=TESSERACT_CONFIG) #    lang='rus', config=config

            # !!!!!!! Без очистки текста
            # Очистка OCR-текста
            text = clean_ocr_text(text)
            #logger.info(f"=========={text}==========")
            # Извлечение параметров
            date = extract_field(regex_date, text, "Дата")
            # logger.info(f"как распознался до обработки ==={date}===")
            if date == "Неизвестно":
                error_count += 1
            #     logger.info(f"=========={filename}==========")
            #     continue
            inventory = extract_field(regex_inventory, text, "Инвентарный номер")
            # нужно для проверки и устранения проблем более чистой обработки
            #   logger.info(f"как распознался до обработки ==={inventory}===")
            # после БАШ делает цифры
            inventory=normalize_bash_inventory_number(inventory)
            # logger.info(f"!!!!!!!!!!!!!!!!!!!!!{inventory}!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if inventory == "Неизвестно":
                error_count += 1
                logger.info(f"=========={filename}==========")
                continue
            clean_date = clean_filename(date)
            clean_inventory = clean_filename(inventory)

            # =====================Начало  связываемся с xl =====================
            results = poisk_data(query=clean_inventory)
            location = results['location']
            mux = "mux-"+str(results['mux'])
            transmitter = results['transmitter']
            # =====================Конец  связываемся с xl ======================
            # logger.info(f"Дата: {clean_date}")
            # logger.info(f"Место: {location}")
            # logger.info(f"MUX: {mux}")
            # logger.info(f"Модель: {transmitter}")
            # logger.info(f"Инв. номер: {clean_inventory}")
            # Формирование имени файла
            new_filename = f"Протокол_{clean_date}_{location}_{mux}_{transmitter}_{clean_inventory}.pdf"
            new_file_path = os.path.join(OUTPUT_FOLDER, new_filename)

            # Проверка на дубликаты
            if os.path.exists(new_file_path):
                base, ext = os.path.splitext(new_filename)
                counter = 1
                while os.path.exists(new_file_path):
                    new_filename = f"{base}_{counter}??Совпад??{ext}"
                    new_file_path = os.path.join(OUTPUT_FOLDER, new_filename)
                    counter += 1
                logger.warning(f"Файл уже существует, сохранён как: {new_filename}")

            # Копирование файла
            shutil.copy2(file_path, new_file_path)
            # logger.info(f"Сохранён: {new_filename}\n")
            success_count += 1

        except Exception as e:
            logger.error(f"Ошибка при обработке {filename}: {e}\n", exc_info=True)
            error_count += 1

    # Итоговая статистика
    logger.info("=" * 50)
    logger.info(f"Успешно обработано: {success_count}")
    logger.info(f"Ошибок: {error_count}")
    logger.info(f"Всего: {len(pdf_files)}")
    logger.info("=" * 50)
# ==================== КОНЕЦ ОСНОВНАЯ ФУНКЦИЯ ====================

if __name__ == "__main__":
    process_pdfs()