import openpyxl
import sys
import os
from logi.logi import logger
# ====================НАЧАЛО НАСТРОЙКИ ====================
EXCEL_FILE = "data_base_py/data_base_2026.xlsm"
SHEET_NAME = "base" # None = первый лист, или укажите имя листа

# Колонки (A=1, B=2, ...)
COL_INVENTORY = 1  # A - Инвентарный номер
COL_LOCATION = 2  # B - Пункт установки оборудования
COL_MUX = 4  # D - Мультиплекс
IZGOTOVITEL = 5  # E - Изготовитель
MODEL = 6  # F - Модель
COL_TRANSMITTER = 7  # G - Наименование передатчика
SERIAL_NUMBER = 8  # H - Серийный номер
TVK = 12  # L - ТВК
CELL_ID = 13  # M - cсел айди
RICH = 14  # N - РИЧ мощьность
CHASTOTA = 30  # AD - ЧАСТОТА
# ====================КОНЕЦ НАСТРОЙКИ ====================

def load_excel_data_protocol(filepath):
    """Загружает данные из Excel файла"""
    try:
        wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
        if SHEET_NAME:
            # точное имя листа
            ws = wb[SHEET_NAME]
        # Создаём словарь:
        data = {}
        # начинаем со 2 строки
        for row in ws.iter_rows(min_row=2, values_only=True):
            inventory = row[COL_INVENTORY - 1]
            location = row[COL_LOCATION - 1]
            mux = row[COL_MUX - 1]
            izgotovitel = row[IZGOTOVITEL - 1]
            model = row[MODEL - 1]
            transmitter = row[COL_TRANSMITTER - 1]
            serial_number = row[SERIAL_NUMBER - 1]
            tvk = row[TVK - 1]
            cell_id = row[CELL_ID - 1]
            rich = row[RICH - 1]
            chastota = row[CHASTOTA - 1]
            if inventory:
                # Нормализуем ключ (убираем пробелы, приводим к верхнему регистру)
                # key = str(inventory).strip().upper()
                key = str(location).strip()+"_"+str(mux)      #.upper()
                data[key] = {
                    'inventory': inventory or "В-XL-МЕСТО-НЕ-УКАЗАНО",
                    'mux': mux or "В-XL-MUX-НЕ-УКАЗАНО",
                    'transmitter': transmitter or "В-XL-МОДЕЛЬ-НЕ-УКАЗАНО",
                    'izgotovitel': izgotovitel or "В-XL-МОДЕЛЬ-НЕ-УКАЗАНО",
                    'model': model or "В-XL-МОДЕЛЬ-НЕ-УКАЗАНО",
                    'serial_number': serial_number or "В-XL-МОДЕЛЬ-НЕ-УКАЗАНО",
                    'cell_id': cell_id or "В-XL-МОДЕЛЬ-НЕ-УКАЗАНО",
                    'rich': rich or "В-XL-МОДЕЛЬ-НЕ-УКАЗАНО",
                    'chastota': chastota or "В-XL-МОДЕЛЬ-НЕ-УКАЗАНО",
                    'tvk': tvk or "В-XL-МОДЕЛЬ-НЕ-УКАЗАНО",
                    'location': location or "В-XL-МОДЕЛЬ-НЕ-УКАЗАНО",
                }
        wb.close()
        return data

    except FileNotFoundError:
        logger.warning(f"Файл '{filepath}' не найден!")
        sys.exit(1)
    except Exception as e:
        logger.info(f"❌ Ошибка загрузки файла: {e}")
        sys.exit(1)


def get_location_data_protocol(data, target_name):
    """ПОИСК ПО НАЗВАНИЮ (возвращает СПИСОК всех найденных совпадений)-"""
    results = []  # Создаем пустой список для накопления результатов
    # Приводим искомое название к нижнему регистру и убираем пробелы для надежности
    target_name_clean = target_name.strip().lower()
    for key, value in data.items():
        # Берем часть строки до скобки, убираем пробелы и приводим к нижнему регистру
        base_name = key.split('(')[0].strip().lower()
        if base_name == target_name_clean:
            results.append(value)  # Добавляем найденный словарь в список
    # print(f"{target_name} - ни чего не найдено ==============")
    return results  # Возвращаем список (будет пустым [], если ничего не найдено)


# ==================== ГЛАВНАЯ ФУНКЦИЯ ======================

# ==================== ГЛАВНАЯ ФУНКЦИЯ =======================
if __name__ == "__main__":
    pass
    # data = load_excel_data_protocol(filepath=EXCEL_FILE)
    # print(data)
    #
    #
    # # Использование:
    # result = get_location_data_protocol(data, 'Староактау')
    # # Вывод всех значений (или обращение к конкретным, например result['tvk'])
    # print(result)

