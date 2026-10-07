from pathlib import Path
from logi.logi import logger
from read_xl_new_protocol import load_excel_data_protocol, get_location_data_protocol
import re
import random
import time
import subprocess
from datetime import datetime
from input_data_new_protocol import input_rename_new_protocol, insert_png_folder_to_xlsx, convert_xlsx_to_pdf
from ocr_new_protocol_zamena_dannich import find_and_replace_text_in_image_1, find_and_replace_text_in_image_2, \
    find_and_replace_text_in_image_3, find_and_replace_text_in_image_4, find_and_replace_text_in_image_5, \
    find_and_replace_text_in_image_6, find_and_replace_text_in_image_7

# ==================ВХОДНЫЕ ДАННЫЕ=================
# Указываем имя/путь папки
target_folder = Path("do_nachalo_new_protocol")
EXCEL_FILE = "data_base_py/data_base_2026.xlsm"
SHEET_NAME = "base"  # None = первый лист, или укажите имя листа


# ==================ВХОДНЫЕ ДАННЫЕ=================


def go_po_papkam(target_folder, data):
    empty_results_dict = {}
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
                        # print(f"{name_naselennogo_puncta} - {result}===============")
                        # Проверяем, пуст ли результат
                        if not result:  # Сработает, если result == [] или result is None
                            # Добавляем в словарь (в качестве значения можно указать True, None или сам result)
                            empty_results_dict[name_naselennogo_puncta] = "НЕ НАШЕЛ В БАЗЕ ДАННЫХ НАЗВАНИЕ"
                    for result_nuznii in result:
                        if result_nuznii['mux'] == get_mux_number(mux_value=item2.name):
                            # # Итак есть название и дата протокола  date_protocol и   name_naselennogo_puncta
                            # print(
                            #     f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/zzzzzzzzzzzzzzzzzz")
                            # print(result_nuznii)
                            # НУЖНО СОЗДАТЬ ПАПКУ ПОТОМ В НЕЙ ПАПКУ С MUX И УЖЕ В НЕЙ СОХРАНЯТЬ ПЕРЕДЕЛАННЫЕ ФОТО ГОТОВЫЙ ПРОТОКОЛ XL И PDF
                            # Нужно определится с этими параметрами !!!!!!!!!!!!!!!!!!!!!!!
                            replace_text_date_protocol = datetime.strptime(date_protocol, "%Y-%m-%d").strftime(
                                "%d/%m/%Y")
                            time_date_protocol = f"{random.randint(12, 15)}:{random.randint(10, 57)}"
                            replace_text_chastota = result_nuznii["chastota"]
                            replace_text_power = round(result_nuznii["rich"] * (1 + (random.randint(2, 8) / 100)),
                                                       1)
                            replace_text_atenuazia = random.randint(45, 55)
                            replace_text_neravnomernost_achh = round(random.randint(2, 9) / 10, 1)
                            replace_text_MER = round(random.randint(365, 405) / 10, 1)
                            replace_text_MER_niznie = round(
                                float(replace_text_MER) - float(random.randint(2, 15) / 10), 1)
                            replace_text_frequency_offset = round(random.randint(-4, 4) / 10, 1)
                            replace_text_frequency_niznie = round(
                                float(replace_text_frequency_offset) - float(random.randint(1, 4) / 10), 1)
                            vnutrennia_power = round(random.randint(-1402, -1072) / 100, 1)
                            # =========До начала изменения пропишу все параметры чтобы не запутаться=========
                            # Нужно определится с этими параметрами !!!!!!!!!!!!!!!!!!!!!!!

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
                            location_itog = result_nuznii["location"]
                            # print(inventory_protocol, mux_protocol, transmitter_protocol, izgotovitel_protocol,
                            #       serial_number_protocol, cell_id_protocol, rich_protocol, tvk_protocol)
                            #

                            input_rename_new_protocol(
                                output_folder=f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/",
                                inventory_protocol=inventory_protocol,
                                mux_protocol=mux_protocol,
                                transmitter_protocol=transmitter_protocol,
                                izgotovitel_protocol=izgotovitel_protocol,
                                serial_number_protocol=serial_number_protocol,
                                cell_id_protocol=cell_id_protocol,
                                rich_protocol=rich_protocol, tvk_protocol=tvk_protocol,
                                date_protocol=date_protocol,
                                name_naselennogo_puncta=name_naselennogo_puncta,
                                location_itog=location_itog,
                                chastota=chastota, model_protocol=model_protocol,
                                replace_text_power=replace_text_power, replace_text_MER=replace_text_MER,
                                replace_text_neravnomernost_achh=replace_text_neravnomernost_achh,
                                replace_text_frequency_offset=replace_text_frequency_offset)

                            # переделывание 1 картинки
                            input_image_1 = f"do_nachalo_new_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/1.png"
                            output_image_1 = f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/1.png"
                            find_and_replace_text_in_image_1(input_path=input_image_1, output_path=output_image_1,
                                                             replace_text_date_protocol=replace_text_date_protocol,
                                                             replace_text_chastota=replace_text_chastota,
                                                             replace_text_frequency_offset=replace_text_frequency_offset,
                                                             time_date_protocol=time_date_protocol,
                                                             replace_text_MER=replace_text_MER,
                                                             replace_text_MER_niznie=replace_text_MER_niznie,
                                                             vnutrennia_power=vnutrennia_power)

                            # переделывание 2 картинки
                            input_image_2 = f"do_nachalo_new_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/2.png"
                            output_image_2 = f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/2.png"
                            find_and_replace_text_in_image_2(input_path=input_image_2, output_path=output_image_2,
                                                             replace_text_date_protocol=replace_text_date_protocol,
                                                             time_date_protocol=time_date_protocol,
                                                             replace_text_chastota=replace_text_chastota,
                                                             replace_text_MER=replace_text_MER,
                                                             replace_text_MER_niznie=replace_text_MER_niznie,
                                                             replace_text_frequency_niznie=replace_text_frequency_niznie,
                                                             vnutrennia_power=vnutrennia_power)
                            # переделывание 3 картинки
                            input_image_3 = f"/home/sem/py/pdf_name/data_base_py/3_etalon.png"
                            output_image_3 = f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/3.png"
                            find_and_replace_text_in_image_3(input_path=input_image_3, output_path=output_image_3,
                                                             replace_text_date_protocol=replace_text_date_protocol,
                                                             time_date_protocol=time_date_protocol,
                                                             replace_text_chastota=replace_text_chastota,
                                                             replace_text_MER=replace_text_MER,
                                                             vnutrennia_power=vnutrennia_power)

                            # переделывание 4 картинки
                            input_image_4 = f"do_nachalo_new_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/4.png"
                            output_image_4 = f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/4.png"
                            find_and_replace_text_in_image_4(input_path=input_image_4, output_path=output_image_4,
                                                             replace_text_neravnomernost_achh=replace_text_neravnomernost_achh,
                                                             replace_text_MER=replace_text_MER,
                                                             replace_text_chastota=replace_text_chastota,
                                                             replace_text_date_protocol=replace_text_date_protocol,
                                                             time_date_protocol=time_date_protocol,
                                                             vnutrennia_power=vnutrennia_power)
                            # переделывание 5 картинки
                            input_image_5 = f"do_nachalo_new_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/5.png"
                            output_image_5 = f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/5.png"
                            find_and_replace_text_in_image_5(input_path=input_image_5, output_path=output_image_5,
                                                             replace_text_chastota=replace_text_chastota,
                                                             time_date_protocol=time_date_protocol,
                                                             replace_text_date_protocol=replace_text_date_protocol,
                                                             vnutrennia_power=vnutrennia_power)
                            # переделывание 6 картинки
                            input_image_6 = f"do_nachalo_new_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/6.png"
                            output_image_6 = f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/6.png"
                            find_and_replace_text_in_image_6(input_path=input_image_6, output_path=output_image_6,
                                                             replace_text_chastota=replace_text_chastota,
                                                             replace_text_date_protocol=replace_text_date_protocol,
                                                             time_date_protocol=time_date_protocol,
                                                             vnutrennia_power=vnutrennia_power)
                            # переделывание мощности
                            input_image_7 = f"/home/sem/py/pdf_name/data_base_py/power_etalon.png"
                            output_image_7 = f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/power.png"
                            find_and_replace_text_in_image_7(input_path=input_image_7, output_path=output_image_7,
                                                             replace_text_chastota=replace_text_chastota,
                                                             replace_text_power=replace_text_power,
                                                             replace_text_atenuazia=replace_text_atenuazia)

                            # Вставляем картинки в xl и сохраняем
                            # Индивидуальная конфигурация каждой картинки
                            images_config = {
                                "1.png": {"x_cm": 2.0, "y_cm": 52.0, "w_cm": 8.0, "h_cm": 6.0},
                                "2.png": {"x_cm": 10.5, "y_cm": 52.0, "w_cm": 8.0, "h_cm": 6.0},
                                "3.png": {"x_cm": 2.0, "y_cm": 58.1, "w_cm": 8.0, "h_cm": 6.0},
                                "4.png": {"x_cm": 10.5, "y_cm": 58.1, "w_cm": 8.0, "h_cm": 6.0},
                                "5.png": {"x_cm": 2.0, "y_cm": 64.2, "w_cm": 8.0, "h_cm": 6.0},
                                "6.png": {"x_cm": 10.5, "y_cm": 64.2, "w_cm": 8.0, "h_cm": 6.0},
                                "power.png": {"x_cm": 2.0, "y_cm": 70.6, "w_cm": 10.0, "h_cm": 5.3},
                            }
                            insert_png_folder_to_xlsx(
                                xlsx_path=f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/Протокол_{date_protocol}_{name_naselennogo_puncta}_{mux_protocol}_{transmitter_protocol}_{inventory_protocol}.xlsx",
                                image_folder=f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}",
                                sheet_name="title", images_config=images_config)
                            time.sleep(1)

                            # делаем PDF
                            convert_xlsx_to_pdf(
                                xlsx_path=f"posle_gotovie_protocol/{date_protocol} {name_naselennogo_puncta}/{item2.name}/Протокол_{date_protocol}_{name_naselennogo_puncta}_{mux_protocol}_{transmitter_protocol}_{inventory_protocol}.xlsx",
                                output_folder="posle_gotovie_protocol/pdf_folder")
    print("================Пустые результаты в списке:", empty_results_dict)


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
    try:
        go_po_papkam(target_folder=target_folder, data=data)
    except Exception as e:
        print(e)
