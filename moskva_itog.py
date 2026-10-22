from pathlib import Path
from logi.logi import logger
from read_xl_new_protocol import load_excel_data_protocol, get_location_data_protocol
import re, random, time, subprocess
from datetime import datetime
from input_data_new_protocol import input_rename_new_protocol, insert_png_folder_to_xlsx, convert_xlsx_to_pdf
from ocr_new_protocol_zamena_dannich import (
    find_and_replace_text_in_image_1, find_and_replace_text_in_image_2, find_and_replace_text_in_image_3,
    find_and_replace_text_in_image_4, find_and_replace_text_in_image_5, find_and_replace_text_in_image_6,
    find_and_replace_text_in_image_7
)
from openpyxl import load_workbook
# ==================ВХОДНЫЕ ДАННЫЕ=================
target_folder = Path("nachalo_moskva_itog")
EXCEL_FILE = "data_base_py/itog_moskva.xlsx"
SHEET_NAME = "title"
SHEET_NAME_MOSKVA = "data"
EXCEL_MY_BASE = "data_base_py/data_base_2026.xlsm"
SHEET_MY_BASE = "base"  # None = первый лист, или укажите имя листа

# ================================================
def go_po_papkam(target_folder):
    if not target_folder.exists():
        print(f"❌ Папка '{target_folder}' не найдена.")
        return
    # 1-й уровень папок
    for folder1 in target_folder.iterdir():
        if not folder1.is_dir():
            continue
        # 2-й уровень папок
        for folder2 in folder1.iterdir():
            if not folder2.is_dir():
                continue
            # Ищем единственный xl/xlsx файл
            xl_files = list(folder2.glob("*.xls*"))
            if len(xl_files) == 1:
                xl_path = xl_files[0]
                # print(f"\n📂 [{folder1.name}] -> [{folder2.name}]")
                # print(f"📄 Найден файл: {xl_path.name}")
                # ====================ДОБЫВАЕМ ДАННЫЕ===============
                try:
                    wb = load_workbook(xl_path, data_only=True, read_only=True)
                    ws = wb[SHEET_NAME] if SHEET_NAME else wb.active
                    filial = "РТПЦ Республики Башкортостан"
                    punct_ustanovki = ws["I11"].value
                    data_provedenia = ws["H31"].value
                    # приведем к одному формату
                    if data_provedenia:
                        if isinstance(data_provedenia, datetime):
                            data_provedenia = data_provedenia.strftime("%d.%m.%Y")
                        elif isinstance(data_provedenia, str):
                            # Пробуем распарсить разные форматы
                            for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d.%m.%y", "%d/%m/%Y"):
                                try:
                                    data_provedenia = datetime.strptime(data_provedenia, fmt).strftime("%d.%m.%Y")
                                    break
                                except ValueError:
                                    continue
                    modulator = "A"
                    tvk =  ws["I13"].value
                    shema_modulazii = ws["G18"].value
                    scorost_koda_fec = ws["G19"].value
                    zachitnii_interval = ws["G20"].value
                    modulazia_l1 = ws["G21"].value
                    modulazia_plp = ws["G22"].value
                    kolichestvo_nesuchih = ws["O18"].value
                    kolichestvo_nesuchih = ws["O18"].value
                    skorost_transportnogo_potoka = ws["O19"].value
                    rabota_v_seti = ws["O20"].value
                    fiz_yroven_plp = ws["O21"].value
                    sell_id = ws["O22"].value
                    vichodnaia_mochnost = ws["I48"].value
                    ber = ws["I49"].value
                    mer = ws["I50"].value
                    a_sch_h = ws["I51"].value
                    vnepolosnie_signali = ws["I52"].value
                    otklonenie_zentralnoi_chastoti = ws["I54"].value
                    pobochnie_izluchenia = ws["I55"].value
                    # узнаю БАШ
                    bash= ws["I14"].value
                    print(bash)
                    wb.close()
                    # ДОСТАЕМ ДАННЫЕ ИЗ МОЕЙ БАЗЫ ДАННЫХ
                    wb = load_workbook(EXCEL_MY_BASE, data_only=True, read_only=True)
                    ws = wb[SHEET_MY_BASE] if SHEET_MY_BASE else wb.active
                    found_row = None
                    for row in ws.iter_rows(min_row=2, values_only=False):
                        if row[0].value and str(row[0].value).strip() == bash:
                            found_row = row
                            break
                    if found_row:
                        id = found_row[2].value  # C - ID ПУО
                        izgotovitel = found_row[4].value  # E
                        model_peredatchika = found_row[5].value  # F
                        naimenovanie_peredatchika = found_row[6].value  # G
                        rezim = found_row[9].value  # J
                        vechaemaia_programma = found_row[10].value  # K



                    else:
                        print(f"❌ '{bash}' не найден в моей базе.")
                    wb.close()



                except Exception as e:
                    print(f"❌ Ошибка чтения файла {xl_path.name}: {e}")

                # ====================ЗАПИСЫВАЕМ ДАННЫЕ В ТАБЛИЦУ===============
                try:
                    wb = load_workbook(EXCEL_FILE)
                    ws = wb[SHEET_NAME_MOSKVA]
                    # Проверяем, есть ли уже строка где совпадают И punct_ustanovki (B), И fiz_yroven_plp (O)
                    already_exists = False
                    for row in ws.iter_rows(min_row=3, max_row=ws.max_row, min_col=2, max_col=20):
                        if row[0].value == punct_ustanovki and row[18].value == fiz_yroven_plp:
                            already_exists = True
                            break
                    if already_exists:
                        print(
                            f"⏭️ '{punct_ustanovki}' с fiz_yroven={fiz_yroven_plp} уже есть в {SHEET_NAME_MOSKVA}. Пропуск.")
                    else:
                        # Ищем следующую свободную строку в столбце B начиная с 3
                        next_row = 3
                        while ws.cell(row=next_row, column=2).value is not None:
                            next_row += 1
                        # Записываем во все нужные столбцы в эту же строку
                        ws.cell(row=next_row, column=1).value = filial  # A
                        ws.cell(row=next_row, column=2).value = punct_ustanovki  # B
                        ws.cell(row=next_row, column=3).value = id  # C
                        ws.cell(row=next_row, column=4).value = data_provedenia  # D
                        ws.cell(row=next_row, column=5).value = izgotovitel  # E
                        ws.cell(row=next_row, column=6).value = model_peredatchika  # F
                        ws.cell(row=next_row, column=7).value = naimenovanie_peredatchika  # G
                        ws.cell(row=next_row, column=8).value = rezim  # H
                        ws.cell(row=next_row, column=9).value = vechaemaia_programma  # I
                        ws.cell(row=next_row, column=10).value = tvk  # J
                        ws.cell(row=next_row, column=11).value = modulator  # K
                        ws.cell(row=next_row, column=12).value = shema_modulazii  # L
                        ws.cell(row=next_row, column=13).value = scorost_koda_fec  # M
                        ws.cell(row=next_row, column=14).value = zachitnii_interval  # N
                        ws.cell(row=next_row, column=15).value = modulazia_l1  # O
                        ws.cell(row=next_row, column=16).value = modulazia_plp  # P
                        ws.cell(row=next_row, column=17).value = kolichestvo_nesuchih  # Q
                        ws.cell(row=next_row, column=18).value = skorost_transportnogo_potoka  # R
                        ws.cell(row=next_row, column=19).value = rabota_v_seti  # S
                        ws.cell(row=next_row, column=20).value = fiz_yroven_plp  # T !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        ws.cell(row=next_row, column=21).value = sell_id  # U
                        ws.cell(row=next_row, column=22).value = vichodnaia_mochnost  # V
                        ws.cell(row=next_row, column=23).value = ber  # W
                        ws.cell(row=next_row, column=24).value = mer  # X
                        ws.cell(row=next_row, column=25).value = a_sch_h  # Y
                        ws.cell(row=next_row, column=26).value = vnepolosnie_signali  # Z
                        ws.cell(row=next_row, column=27).value = otklonenie_zentralnoi_chastoti  # AA
                        ws.cell(row=next_row, column=28).value = pobochnie_izluchenia  # AB


                        # ws.cell(row=next_row, column=15).value = fiz_yroven_plp  # P
                        wb.save(EXCEL_FILE)
                        # print(
                        #     f"✅ Записано в строку {next_row}: A={filial} | B={punct_ustanovki} | C={id} | D={data_provedenia} | E={izgotovitel}")
                    wb.close()
                except Exception as e:
                    print(f"❌ ЗАПИСЬ файла: {e}")

            # ====================КОНЕЦ  ЗАПИСЫВАЕМ ДАННЫЕ В ТАБЛИЦУ===============
            elif len(xl_files) > 1:
                print(f"⚠️ В папке {folder2.name} найдено {len(xl_files)} xl-файлов (ожидался 1). Пропуск.")


if __name__ == "__main__":
    # data = load_excel_data_protocol(filepath=EXCEL_FILE)
    try:
        go_po_papkam(target_folder=target_folder)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        print(e)