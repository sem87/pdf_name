import os
import re
import shutil
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from read_xl import poisk_data
from logi.logi import logger
from datetime import datetime

# ====================НАЧАЛО НАСТРОЙКИ ============================
INPUT_FOLDER = "do"
OUTPUT_FOLDER = "do_renamed"
DPI = 300
TESSERACT_LANG = 'rus'
TESSERACT_CONFIG = '--psm 6'
# ==================== КОНЕЦ НАСТРОЙКИ ================================
# ==================== НАЧАЛО РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ ====================
config = '-c tessedit_char_whitelist=АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯабвгдежзиклмнопрстуфхцчшщэюя0123456789: '

regex_date = re.compile(
    r"(?i)(?:дата\s+проведения\s+измерений|"
    r"[aа]т[аа]\s+[iі]р[оo]в[еe]д[еe]н[иі]я\s+[мm]3[мm]ер[еe]н[иі]й|"
    r"[aа]т[аа]\s+.*?[мm]3[мm]ер[еe]н[иі]й)"
    r"\s*[:：]\s*"
    r"(\d{2}[\.]\d{2}[\.]\d{4})",
    re.IGNORECASE
)

regex_inventory = re.compile(
    r"Инвентарный\s+номер\s*[:：]\s*"
    r"(БАШ[А-ЯA-Z0-9ОO]{3,10})",
    re.IGNORECASE | re.UNICODE
)


# ==================== КОНЕЦ РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ =================
# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================
def clean_ocr_text(text: str) -> str:
    if not text:
        return text
    latin_to_cyrillic = {
        'A': 'А', 'B': 'В', 'C': 'С', 'E': 'Е', 'H': 'Н',
        'K': 'К', 'M': 'М', 'O': 'О', 'P': 'Р', 'T': 'Т',
        'X': 'Х', 'Y': 'У',
        'a': 'а', 'c': 'с', 'e': 'е', 'o': 'о', 'p': 'р',
        'x': 'х', 'y': 'у',
    }
    result = text
    for latin, cyrillic in latin_to_cyrillic.items():
        result = result.replace(latin, cyrillic)
    return result


def clean_filename(name: str) -> str:
    if not name or name == "Неизвестно":
        return "Неизвестно"
    name = re.sub(r'[\\/*?:"<>|\n\r]', "", name)
    name = re.sub(r'\s+', '_', name)
    name = re.sub(
        r'_*(?:изготовитель|H3rOTOBHTeJIB|серийный|Cepийный|CepHiHbIn|'
        r'инвентарный|HBeHTapHbIi|телевизионный|TeJIeBH3HOHHbIi).*',
        '', name, flags=re.IGNORECASE
    )
    name = re.sub(r'_+', '_', name)
    return name.strip('_')


def extract_field(regex: re.Pattern, text: str, field_name: str) -> str:
    match = regex.search(text)
    if match:
        value = match.group(1).strip()
        return value
    else:
        logger.warning(f"{field_name}:НЕ НАЙДЕНО!!!")
        return "Неизвестно"


def normalize_bash_inventory_number(raw_string):
    match = re.search(r'БАШ(.*)', raw_string, re.IGNORECASE)
    if not match:
        return None
    suffix = match.group(1)
    suffix = re.sub(r'[ОоOo]', '0', suffix)
    suffix = re.sub(r'[ЗзZz]', '3', suffix)
    suffix = re.sub(r'[IiІіlL]', '1', suffix)
    suffix = re.sub(r'[Ss]', '5', suffix)
    suffix = re.sub(r'[Bb]', '8', suffix)
    suffix = re.sub(r'[Ggб]', '6', suffix)
    suffix = re.sub(r'[Tt]', '7', suffix)
    suffix = re.sub(r'[AaДд]', '4', suffix)
    digits_only = re.sub(r'\D', '', suffix)
    return f'БАШ{digits_only}'


def check_dependencies():
    try:
        tesseract_cmd = shutil.which('tesseract')
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        else:
            logger.warning("Tesseract не найден в PATH. Установите tesseract-ocr")
    except Exception as e:
        logger.error(f"Ошибка проверки Tesseract: {e}")

    if not os.path.exists(INPUT_FOLDER):
        logger.error(f"Папка ввода '{INPUT_FOLDER}' не существует!")
        return False
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    return True


# ==================== НАЧАЛО ОСНОВНАЯ ФУНКЦИЯ ====================
def process_pdfs():
    if not check_dependencies():
        return

    pdf_files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")])
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
            images = convert_from_path(file_path, first_page=1, last_page=1, dpi=DPI)
            if not images:
                logger.warning(f"Не удалось конвертировать {filename}\n")
                error_count += 1
                continue

            text = pytesseract.image_to_string(images[0], lang=TESSERACT_LANG, config=TESSERACT_CONFIG)
            text = clean_ocr_text(text)

            date = extract_field(regex_date, text, "Дата")
            if date == "Неизвестно":
                error_count += 1

            inventory = extract_field(regex_inventory, text, "Инвентарный номер")
            inventory = normalize_bash_inventory_number(inventory)

            if inventory == "Неизвестно":
                error_count += 1
                logger.info(f"=========={filename}==========")
                continue

            raw_date = clean_filename(date)
            clean_date = datetime.strptime(raw_date, '%d.%m.%Y').strftime('%Y.%m.%d')
            clean_inventory = clean_filename(inventory)

            # =====================Начало  связываемся с xl =====================
            results = poisk_data(query=clean_inventory)
            location = results['location']
            mux = "mux-" + str(results['mux'])
            transmitter = results['transmitter']
            # =====================Конец  связываемся с xl ======================

            # >>> ЯВНАЯ ПРОВЕРКА ПАПКИ <<<
            folder_name = clean_filename(f"{clean_date}_{location}")
            target_folder = os.path.join(OUTPUT_FOLDER, folder_name)

            if os.path.exists(target_folder):
                logger.info(f"Папка уже существует, сохраняем в: {target_folder}")
            else:
                os.makedirs(target_folder)
                logger.info(f"Создана новая папка: {target_folder}")

            # Новое наименование файла
            new_filename = f"{transmitter}_{clean_date}.pdf"
            new_file_path = os.path.join(target_folder, new_filename)

            # Проверка на дубликаты внутри целевой папки
            if os.path.exists(new_file_path):
                base, ext = os.path.splitext(new_filename)
                counter = 1
                while os.path.exists(new_file_path):
                    new_filename = f"{base}_{counter}_Совпад{ext}"
                    new_file_path = os.path.join(target_folder, new_filename)
                    counter += 1
                logger.warning(f"Файл уже существует, сохранён как: {new_filename}")

            # Копирование файла
            shutil.copy2(file_path, new_file_path)
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