from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import random


# def replace_carrier_frequency_offset(input_image_path, output_image_path, new_value="0.7"):
#     """
#     Заменяет значение Carrier Frequency Offset на изображении
#     """
#     # Открываем изображение
#     img = Image.open(input_image_path)
#     draw = ImageDraw.Draw(img)
#
#     # Координаты области значения Carrier Frequency Offset
#     # (настройте под ваше изображение)
#     # Примерные координаты для вашего скриншота:
#     x1, y1 = 520, 395  # левый верхний угол
#     x2, y2 = 620, 420  # правый нижний угол
#
#     # Цвет фона (серый, как на изображении)
#     bg_color = (210, 210, 210)  # светло-серый
#
#     # Закрашиваем область старым значением
#     draw.rectangle([x1, y1, x2, y2], fill=bg_color)
#
#     # Пробуем загрузить шрифт (можно изменить на свой)
#     try:
#         # Для Linux
#         font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
#     except:
#         try:
#             # Для Windows
#             font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
#         except:
#             # Стандартный шрифт
#             font = ImageFont.load_default()
#
#     # Текст с новым значением
#     text = f"{new_value} Hz"
#     text_color = (0, 0, 180)  # темно-синий, как на оригинальном изображении
#
#     # Вычисляем позицию для центрирования текста
#     bbox = draw.textbbox((0, 0), text, font=font)
#     text_width = bbox[2] - bbox[0]
#     text_height = bbox[3] - bbox[1]
#
#     x_text = x1 + (x2 - x1 - text_width) // 2
#     y_text = y1 + (y2 - y1 - text_height) // 2
#
#     # Рисуем новый текст
#     draw.text((x_text, y_text), text, fill=text_color, font=font)
#
#     # Сохраняем результат
#     img.save(output_image_path)
#     print(f"Изображение сохранено: {output_image_path}")
#     return img
#
#
# def replace_carrier_frequency_offset_auto(input_image_path, output_image_path, new_value="0.7"):
#     """
#     Автоматический поиск и замена значения Carrier Frequency Offset
#     с использованием OpenCV и шаблонов
#     """
#     # Открываем изображение
#     img = Image.open(input_image_path)
#     img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     draw = ImageDraw.Draw(img)
#
#     # Ищем строку "Carrier Frequency Offset"
#     # Координаты примерные - нужно настроить или использовать OCR
#     label_y = 395  # Y-координата строки
#
#     # Область где находится значение (справа от метки)
#     value_x_start = 520
#     value_x_end = 620
#     value_y_start = 395
#     value_y_end = 420
#
#     # Закрашиваем старое значение
#     bg_color = (210, 210, 210)
#     draw.rectangle([value_x_start, value_y_start, value_x_end, value_y_end], fill=bg_color)
#
#     # Загружаем шрифт
#     try:
#         font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
#     except:
#         try:
#             font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
#         except:
#             font = ImageFont.load_default()
#
#     # Новый текст
#     text = f"{new_value} Hz"
#     text_color = (0, 0, 180)
#
#     # Позиция текста
#     bbox = draw.textbbox((0, 0), text, font=font)
#     text_width = bbox[2] - bbox[0]
#     text_height = bbox[3] - bbox[1]
#
#     x_text = value_x_start + (value_x_end - value_x_start - text_width) // 2
#     y_text = value_y_start + (value_y_end - value_y_start - text_height) // 2
#
#     draw.text((x_text, y_text), text, fill=text_color, font=font)
#
#     # Сохраняем
#     img.save(output_image_path)
#     print(f"Изображение сохранено: {output_image_path}")
#     return img

def menaem_parametri_na_nuznie(draw, replace_text, x1, y1, x2, y2, text_color, bg_color, font):
    """МЕНЯЕТ НА НУЖНЫЙ ТЕКСТ, МОЖНО НЕСКОЛЬКО БЛОКОВ НА 1 КАРТИНКУ"""
    # Координаты значения (настройте под ваше изображение)
    coords = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
    draw.rectangle([coords['x1'], coords['y1'], coords['x2'], coords['y2']], fill=bg_color)
    text = f"{replace_text}"
    # Рисуем текст, жестко привязывая его верхний левый угол к координатам (x1, y1)
    draw.text((x1, y1), text, fill=text_color, font=font, anchor="lt")


def find_and_replace_text_in_image_1(input_path, output_path, replace_text_date_protocol, replace_text_chastota,
                                     replace_text_frequency_offset, time_date_protocol, replace_text_MER,
                                     replace_text_MER_niznie,vnutrennia_power):
    """ОТКРЫВАЕМ И СОХРАНЯЕМ ДАННЫЕ"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_seredina = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                       size=16)  # боле менее похож
    font_date = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                   size=18)  # боле менее похож
    # вставка даты
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_date_protocol, x1=456, y1=3, x2=534, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка времени
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=368, y1=24, x2=390, y2=34,
                               text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка carrier frequency offset
    menaem_parametri_na_nuznie(draw, replace_text=f"   {replace_text_frequency_offset}", x1=426, y1=266, x2=467, y2=277,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina)
    # вставка внутренняя мощьность
    menaem_parametri_na_nuznie(draw, replace_text=f"   {vnutrennia_power}", x1=421, y1=166, x2=458, y2=177,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina)
    # вставка BER
    menaem_parametri_na_nuznie(draw, replace_text="0.0E-09", x1=353, y1=406, x2=402, y2=416, text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina)
    # вставка BER
    menaem_parametri_na_nuznie(draw, replace_text="0.0E-09", x1=531, y1=406, x2=577, y2=416, text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina)
    # вставка MER вверху
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER_niznie, x1=360, y1=306, x2=387, y2=316,
                               text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina)
    # вставка MER ниже
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=360, y1=345, x2=384, y2=357,
                               text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina)
    img.save(output_path)
    return img


def find_and_replace_text_in_image_2(input_path, output_path, replace_text_date_protocol, replace_text_chastota,
                                     replace_text_MER, replace_text_MER_niznie, replace_text_frequency_niznie,
                                     time_date_protocol,vnutrennia_power):
    """ОТКРЫВАЕМ И СОХРАНЯЕМ ДАННЫЕ"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_seredina = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                       size=16)  # боле менее похож
    font_date = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                   size=18)  # боле менее похож
    # вставка даты
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_date_protocol, x1=456, y1=3, x2=534, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка времени
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=580, y1=46, x2=601, y2=56,
                               text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка MER
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=588, y1=366, x2=615, y2=376,
                               text_color=(0, 0, 180), bg_color=(189, 190, 189), font=font_seredina)
    # вставка MER  пониженные значение
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER_niznie, x1=588, y1=286, x2=613, y2=297,
                               text_color=(0, 0, 180), bg_color=(189, 190, 189), font=font_seredina)
    # вставка внутренней мощьности
    vnutrennia_power2=round(vnutrennia_power-random.randint(1, 4) / 10, 2)
    menaem_parametri_na_nuznie(draw, replace_text=vnutrennia_power2, x1=570, y1=166, x2=601, y2=177,
                               text_color=(0, 0, 180), bg_color=(189, 190, 189), font=font_seredina)
    # вставка carrier frequency offset  пониженные значение
    menaem_parametri_na_nuznie(draw, replace_text=f"   {replace_text_frequency_niznie}", x1=583, y1=246, x2=615, y2=258,
                               text_color=(0, 0, 180), bg_color=(189, 190, 189), font=font_seredina)
    # вставка BER
    menaem_parametri_na_nuznie(draw, replace_text="0.0E-09", x1=589, y1=386, x2=635, y2=397, text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina)
    # вставка BER
    menaem_parametri_na_nuznie(draw, replace_text="0.0E-09", x1=589, y1=406, x2=635, y2=417, text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina)
    img.save(output_path)
    return img


def find_and_replace_text_in_image_3(input_path, output_path, replace_text_date_protocol, replace_text_chastota,
                                     replace_text_MER, time_date_protocol,vnutrennia_power):
    """ОТКРЫВАЕМ И СОХРАНЯЕМ ДАННЫЕ"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_seredina = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                       size=16)  # боле менее похож
    font_seredina2 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                        size=16)  # боле менее похож
    font_date = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                   size=18)  # боле менее похож
    # вставка даты
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_date_protocol, x1=456, y1=3, x2=534, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка времени
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=367, y1=24, x2=392, y2=34,
                               text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка MER первый вариант
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=586, y1=124, x2=614, y2=136,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina2)
    # вставка внутренней мощьности
    vnutrennia_power2 = round(vnutrennia_power - random.randint(2, 5) / 10, 2)
    menaem_parametri_na_nuznie(draw, replace_text=vnutrennia_power2, x1=91, y1=124, x2=121, y2=136,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina2)
    # вставка MER второй вариант
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=147, y1=189, x2=175, y2=199,
                               text_color=(132, 207, 255), bg_color=(0, 0, 0), font=font_seredina)
    img.save(output_path)
    return img


def find_and_replace_text_in_image_4(input_path, output_path, replace_text_neravnomernost_achh, replace_text_MER,
                                     replace_text_chastota, replace_text_date_protocol, time_date_protocol,vnutrennia_power):
    """ОТКРЫВАЕМ ,ВСТАВЛЯЕМ И СОХРАНЯЕМ ДАННЫЕ"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_seredina = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                       size=16)  # боле менее похож
    font_date = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                   size=18)  # боле менее похож
    # вставка неравномерность АЧХ
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_neravnomernost_achh, x1=256, y1=144, x2=278, y2=154,
                               text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка MER
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=585, y1=124, x2=615, y2=134,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina)
    # вставка внутренней мощьности
    vnutrennia_power2 = round(vnutrennia_power + random.randint(2, 5) / 10, 2)
    menaem_parametri_na_nuznie(draw, replace_text=vnutrennia_power2, x1=91, y1=124, x2=121, y2=136,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=368, y1=24, x2=391, y2=34,
                               text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка даты
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_date_protocol, x1=456, y1=3, x2=534, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка времени
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    img.save(output_path)
    # print(f"Заменено: '{search_text}' -> '{replace_text}'")
    # print(f"Сохранено в: {output_path}")
    return img


def find_and_replace_text_in_image_5(input_path, output_path, replace_text_chastota, replace_text_date_protocol,
                                     time_date_protocol,vnutrennia_power):
    """ОТКРЫВАЕМ ,ВСТАВЛЯЕМ И СОХРАНЯЕМ ДАННЫЕ"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_seredina = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                       size=18)  # боле менее похож
    font_seredina2 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                       size=16)  # боле менее похож
    font_date = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                   size=18)  # боле менее похож
    # вставка даты
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_date_protocol, x1=456, y1=3, x2=534, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка времени
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=66, y1=425, x2=99, y2=439,
                               text_color=(250, 250, 250), bg_color=(0, 0, 0), font=font_seredina)
    # вставка внутренней мощьности
    vnutrennia_power2 = round(vnutrennia_power - random.randint(2, 10) / 10, 2)
    menaem_parametri_na_nuznie(draw, replace_text=vnutrennia_power2, x1=143, y1=84, x2=174, y2=94,
                               text_color=(247, 243, 16), bg_color=(0, 48, 123), font=font_seredina2)
    img.save(output_path)
    return img


def find_and_replace_text_in_image_6(input_path, output_path, replace_text_chastota, replace_text_date_protocol,
                                     time_date_protocol,vnutrennia_power):
    """ОТКРЫВАЕМ ,ВСТАВЛЯЕМ И СОХРАНЯЕМ ДАННЫЕ"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_seredina = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                       size=18)  # боле менее похож
    font_seredina2 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                       size=16)  # боле менее похож
    font_date = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                   size=18)  # боле менее похож
    # вставка даты
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_date_protocol, x1=456, y1=3, x2=534, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка времени
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=66, y1=425, x2=99, y2=439,
                               text_color=(250, 250, 250), bg_color=(0, 0, 0), font=font_seredina)
    # вставка внутренней мощьности
    vnutrennia_power2 = round(vnutrennia_power - random.randint(1, 10) / 10, 2)
    menaem_parametri_na_nuznie(draw, replace_text=vnutrennia_power2, x1=143, y1=64, x2=174, y2=74,
                               text_color=(247, 243, 16), bg_color=(0, 48, 123), font=font_seredina2)
    img.save(output_path)
    return img


def find_and_replace_text_in_image_7(input_path, output_path, replace_text_chastota, replace_text_power,
                                     replace_text_atenuazia):
    """ОТКРЫВАЕМ ,ВСТАВЛЯЕМ И СОХРАНЯЕМ ДАННЫЕ"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_seredina = ImageFont.truetype("/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
                                       size=36)  # боле менее похож  -Bold
    font_power = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", size=119)

    # вставка мощности
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_power, x1=400, y1=299, x2=720, y2=390,
                               text_color=(136, 136, 136), bg_color=(223, 233, 252), font=font_power)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=1351, y1=801, x2=1440, y2=826,
                               text_color=(0, 0, 0), bg_color=(255, 255, 255), font=font_seredina)
    # вставка аттенюация
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_atenuazia, x1=1086, y1=801, x2=1144, y2=826,
                               text_color=(0, 0, 0), bg_color=(255, 255, 255), font=font_seredina)
    img.save(output_path)
    return img


if __name__ == "__main__":
    # =========До начала изменения пропишу все параметры чтобы не запутаться=========
    replace_text_date_protocol = "10/07/2026"
    replace_text_chastota = 555
    replace_text_neravnomernost_achh = 0.9
    replace_text_MER = "40.9"
    replace_text_MER_niznie = round(float(replace_text_MER) - float(random.randint(2, 15) / 10), 1)
    replace_text_frequency_offset = "-0.4"
    replace_text_frequency_niznie = round(float(replace_text_frequency_offset) - float(random.randint(1, 4) / 10), 1)
    time_date_protocol = f"{random.randint(12, 15)}:{random.randint(10, 57)}"
    replace_text_power = 20.5
    replace_text_atenuazia = random.randint(45, 55)
    vnutrennia_power = round(random.randint(-1402, -702) / 100, 1)
    # =========До начала изменения пропишу все параметры чтобы не запутаться=========
    # переделывание 1 картинки
    input_image_1 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux1/1.png"
    output_image_1 = "output_modified.png"
    find_and_replace_text_in_image_1(input_path=input_image_1, output_path=output_image_1,
                                     replace_text_date_protocol=replace_text_date_protocol,
                                     replace_text_chastota=replace_text_chastota,
                                     replace_text_frequency_offset=replace_text_frequency_offset,
                                     time_date_protocol=time_date_protocol, replace_text_MER=replace_text_MER,
                                     replace_text_MER_niznie=replace_text_MER_niznie,vnutrennia_power=vnutrennia_power)
    # переделывание 2 картинки
    input_image_2 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux1/2.png"
    output_image_2 = "output_modified_2.png"
    find_and_replace_text_in_image_2(input_path=input_image_2, output_path=output_image_2,
                                     replace_text_date_protocol=replace_text_date_protocol,
                                     replace_text_chastota=replace_text_chastota, replace_text_MER=replace_text_MER,
                                     replace_text_MER_niznie=replace_text_MER_niznie,
                                     replace_text_frequency_niznie=replace_text_frequency_niznie,
                                     time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)
    # переделывание 3 картинки
    input_image_3 = f"/home/sem/py/pdf_name/data_base_py/3_etalon.png"
    output_image_3 = "output_modified_3.png"
    find_and_replace_text_in_image_3(input_path=input_image_3, output_path=output_image_3,
                                     replace_text_date_protocol=replace_text_date_protocol,
                                     replace_text_chastota=replace_text_chastota, replace_text_MER=replace_text_MER,
                                     time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)

    # переделывание 4 картинки
    input_image_4 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux1/4.png"
    output_image_4 = "output_modified_4.png"
    find_and_replace_text_in_image_4(input_path=input_image_4, output_path=output_image_4,
                                     replace_text_neravnomernost_achh=replace_text_neravnomernost_achh,
                                     replace_text_MER=replace_text_MER, replace_text_chastota=replace_text_chastota,
                                     replace_text_date_protocol=replace_text_date_protocol,
                                     time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)
    # переделывание 5 картинки
    input_image_5 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux1/5.png"
    output_image_5 = "output_modified_5.png"
    find_and_replace_text_in_image_5(input_path=input_image_5, output_path=output_image_5,
                                     replace_text_chastota=replace_text_chastota,
                                     replace_text_date_protocol=replace_text_date_protocol,
                                     time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)
    # переделывание 6 картинки
    input_image_6 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux1/6.png"
    output_image_6 = "output_modified_6.png"
    find_and_replace_text_in_image_6(input_path=input_image_6, output_path=output_image_6,
                                     replace_text_chastota=replace_text_chastota,
                                     replace_text_date_protocol=replace_text_date_protocol,
                                     time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)
    # переделывание power
    input_image_p = f"/home/sem/py/pdf_name/data_base_py/power_etalon.png"
    output_image_p = "output_modified_power.png"
    find_and_replace_text_in_image_7(input_path=input_image_p, output_path=output_image_p,
                                     replace_text_chastota=replace_text_chastota, replace_text_power=replace_text_power,
                                     replace_text_atenuazia=replace_text_atenuazia)
