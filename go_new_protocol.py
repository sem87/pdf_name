from pathlib import Path
from logi.logi import logger
from read_xl_new_protocol import load_excel_data_protocol, get_location_data_protocol
import re
from input_data_new_protocol import input_rename_new_protocol

# ==================ВХОДНЫЕ ДАННЫЕ=================
# Указываем имя/путь папки
target_folder = Path("do_nachalo_new_protocol")
EXCEL_FILE = "data_base_py/data_base_2026.xlsm"
SHEET_NAME = "base"  # None = первый лист, или укажите имя листа


# ==================ВХОДНЫЕ ДАННЫЕ=================


def go_po_papkam(target_folder, data):
    # Проверяем корректность пути
    if not target_folder.exists():
        print(f"❌ Папка '{target_folder}' не найдена. Проверьте путь и текущую рабочую директорию.")
    else:
        # Перебираем все папки, выводим только названия папок
        for item in sorted(target_folder.iterdir()):  # print(item)  # print(item.name)
            if item.is_dir():
                # Пробуем разделить по подчеркиванию
                print(item.name)
                if '_' in item.name:
                    date_protocol, name_naselennogo_puncta = item.name.split('_', 1)
                # Если нет подчеркивания, пробуем по пробелу
                elif ' ' in item.name:
                    date_protocol, name_naselennogo_puncta = item.name.split(' ', 1)
                else:
                    # Если разделителя нет, пропускаем или обрабатываем иначе
                    logger.info(f"Не удалось разобрать: {item.name}\n")
                    continue
                # ходим по папкам в mux
                for item2 in sorted(item.iterdir()):
                    if item2.is_dir():
                        # сдесь зацепиться за значение ,нужно название населенного пункта
                        result = get_location_data_protocol(data=data, target_name=name_naselennogo_puncta)
                        for result_nuznii in result:
                            if result_nuznii['mux'] == get_mux_number(mux_value=item2.name):
                                # Итак есть название и дата протокола  date_protocol и   name_naselennogo_puncta
                                # print(
                                #     f"Дата: {date_protocol}, Название: {name_naselennogo_puncta} Вложенная папка: {item2.name}")
                                print(result_nuznii)
                                inventory_protocol = result_nuznii["inventory"]
                                mux_protocol = result_nuznii["mux"]
                                transmitter_protocol = result_nuznii["transmitter"]
                                izgotovitel_protocol = result_nuznii["izgotovitel"]
                                model_protocol = result_nuznii["model"]
                                serial_number_protocol = result_nuznii["serial_number"]
                                cell_id_protocol = result_nuznii["cell_id"].split('(')[0].strip()
                                rich_protocol = result_nuznii["rich"]
                                tvk_protocol = result_nuznii["tvk"]
                                chastota = result_nuznii["chastota"]
                                # print(inventory_protocol, mux_protocol, transmitter_protocol, izgotovitel_protocol,
                                #       serial_number_protocol, cell_id_protocol, rich_protocol, tvk_protocol)
                                #

                                input_rename_new_protocol(inventory_protocol=inventory_protocol,
                                                          mux_protocol=mux_protocol,
                                                          transmitter_protocol=transmitter_protocol,
                                                          izgotovitel_protocol=izgotovitel_protocol,
                                                          serial_number_protocol=serial_number_protocol,
                                                          cell_id_protocol=cell_id_protocol,
                                                          rich_protocol=rich_protocol, tvk_protocol=tvk_protocol,
                                                          date_protocol=date_protocol,
                                                          name_naselennogo_puncta=name_naselennogo_puncta,
                                                          chastota=chastota,model_protocol=model_protocol)


def get_mux_number(mux_value):
    """Вычисляем mux только цифру"""
    # Преобразуем значение в строку (на случай, если там уже число)
    mux_str = str(mux_value)
    # Ищем одну или более цифр (\d+) в строке
    match = re.search(r'\d+', mux_str)

    if match:
        return int(match.group())  # Возвращаем как целое число (int)
    return None  # Если цифр нет, возвращаем None


if __name__ == "__main__":
    data = load_excel_data_protocol(filepath=EXCEL_FILE)
    go_po_papkam(target_folder=target_folder, data=data)
