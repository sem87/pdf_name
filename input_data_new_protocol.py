import openpyxl
import os
import random
import shutil
import subprocess
import tempfile

# ================= НАСТРОЙКИ =================
# Путь к исходному файлу (должен существовать)
input_file = 'data_base_py/best_power_protocol.xlsx'

# Папка, в которую нужно сохранить результат
output_folder = 'posle_gotovie_protocol'


# =============================================

def input_rename_new_protocol(inventory_protocol, mux_protocol, transmitter_protocol, izgotovitel_protocol,
                              serial_number_protocol, cell_id_protocol, rich_protocol, tvk_protocol,date_protocol,name_naselennogo_puncta,chastota,model_protocol):
    # Формируем полный путь для сохранения
    # Имя нового файла
    # output_filename = f"Протокол_зоны_НЦТВ_{itog_rayon}_{itog_location_measure_metrics}_{date_protocol}.xlsx"
    output_filename = f"Протокол_{date_protocol}_{name_naselennogo_puncta}_{mux_protocol}_{transmitter_protocol}_{inventory_protocol}.xlsx"
    # output_filename = f"Протокол_{clean_date}_{location}_{mux}_{transmitter}_{clean_inventory}.pdf"
    output_path = os.path.join(output_folder, output_filename)

    # 1. Создаем папку для сохранения, если она еще не существует
    os.makedirs(output_folder, exist_ok=True)

    # 2. Открываем существующий Excel файл
    try:
        workbook = openpyxl.load_workbook(input_file)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден!")
        exit()

        # Выбираем лист для редактирования
        # (можно указать имя листа: workbook['Лист1'] или оставить workbook.active для текущего)
    sheet = workbook.active

    # 3. Вставляем данные
    # --- Вариант А: Вставка в конкретные ячейки по координатам ---
    sheet['E5'] = date_protocol
    sheet['H31'] = date_protocol
    sheet['I11'] = name_naselennogo_puncta
    sheet['I12'] = str(izgotovitel_protocol)+" "+str(model_protocol)
    sheet['I13'] = str(tvk_protocol)+"(ТВК), "+str(chastota)+" (МГц)"
    sheet['I14'] = inventory_protocol
    sheet['I15'] = serial_number_protocol

    # 4. Сохраняем файл по новому пути
    workbook.save(output_path)
    print(f"✅ Файл успешно сохранен по пути:\n{output_path}")

# def convert_xlsx_to_pdf(folder_name):
#     """Конвертирует все файлы .xlsx в .pdf в указанной папке
#     с помощью LibreOffice в headless режиме."""
#     # Проверяем, существует ли папка
#     if not os.path.isdir(folder_name):
#         print(f"Ошибка: Папка '{folder_name}' не найдена.")
#         return
#     # Получаем абсолютный путь (LibreOffice лучше работает с абсолютными путями)
#     abs_folder_path = os.path.abspath(folder_name)
#     # # Счетчик для статистики
#     # converted_count = 0
#
#     # Проходим по всем файлам в папке
#     for filename in os.listdir(abs_folder_path):
#         # Проверяем, что файл имеет расширение .xlsx
#         if filename.lower().endswith('.xlsx'):
#             input_file_path = os.path.join(abs_folder_path, filename)
#             # Формируем команду для вызова LibreOffice
#             command = [
#                 'libreoffice',
#                 '--headless',  # Запуск без графического интерфейса
#                 '--norestore',  # Не восстанавливать предыдущую сессию
#                 '--convert-to', 'pdf',  # Формат конвертации
#                 '--outdir', abs_folder_path,  # Папка для сохранения (та же самая)
#                 input_file_path  # Путь к исходному файлу
#             ]
#             #
#             # print(f"Конвертирую: {filename} ...", end=" ")
#             try:
#                 # Запускаем процесс.
#                 # stdout и stderr перенаправляем в DEVNULL, чтобы не засорять консоль
#                 subprocess.run(
#                     command,
#                     check=True,
#                     stdout=subprocess.DEVNULL,
#                     stderr=subprocess.DEVNULL
#                 )
#                 print(f"Готово! (Сохранено как {filename.replace('.xlsx', '.pdf')})")
#             except subprocess.CalledProcessError:
#                 print("Ошибка при конвертации.")
#             except FileNotFoundError:
#                 print("\nКритическая ошибка: LibreOffice не найден в системе!")
#                 print("Установите его: sudo apt install libreoffice-calc")
#                 break


if __name__ == "__main__":
    convert_xlsx_to_pdf(folder_name=output_folder)
