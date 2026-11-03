import cv2
import numpy as np
import os
import random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont


def menaem_parametri_na_nuznie(draw, replace_text, x1, y1, x2, y2,
                               text_color, bg_color, font, anchor="lt", tracking=-1):
    draw.rectangle([x1, y1, x2, y2], fill=bg_color)
    text = str(replace_text)

    if anchor[0] == "l":   tx = x1
    elif anchor[0] == "m": tx = (x1 + x2) / 2
    elif anchor[0] == "r": tx = x2
    else:                  tx = x1

    if anchor[1] == "t":   ty = y1
    elif anchor[1] == "m": ty = (y1 + y2) / 2
    elif anchor[1] in ("b", "d", "s"): ty = y2
    else:                  ty = y1

    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)

    if anchor[0] == "m":   cx = tx - total / 2
    elif anchor[0] == "r": cx = tx - total
    else:                  cx = tx

    for c, w in zip(text, widths):
        draw.text((cx, ty), c, fill=text_color, font=font, anchor="l" + anchor[1])
        cx += w + tracking



def find_and_replace_text_in_image_1(input_path, output_path, replace_text_date_protocol, replace_text_chastota,
                                     replace_text_frequency_offset, time_date_protocol, replace_text_MER,
                                     replace_text_MER_niznie,vnutrennia_power,symbol_rate_ofset,crest_factor,bb_BER):
    """ОТКРЫВАЕМ И СОХРАНЯЕМ ДАННЫЕ"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_seredina = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf", size=15)
    font_seredina2 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf", size=16)
    font_date = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
                                   size=18)  # боле менее похож

    # вставка даты
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_date_protocol, x1=456, y1=3, x2=534, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date, anchor="rd")
    # вставка времени
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date, anchor="rd")
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=368, y1=24, x2=390, y2=34,
                               text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка внутренняя мощьность
    menaem_parametri_na_nuznie(draw, replace_text=f"   {vnutrennia_power}", x1=421, y1=162, x2=458, y2=177,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina, anchor="rs")
    # вставка crest_factor
    menaem_parametri_na_nuznie(draw, replace_text=f"   {crest_factor}", x1=421, y1=182, x2=458, y2=197,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina, anchor="rs")

    # вставка carrier frequency offset
    menaem_parametri_na_nuznie(draw, replace_text=f"   {replace_text_frequency_offset}", x1=426, y1=262, x2=458, y2=277,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina,anchor="rs")
    # вставка simbol rate offset
    menaem_parametri_na_nuznie(draw, replace_text=f"   {symbol_rate_ofset}", x1=420, y1=282, x2=458, y2=297,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina,anchor="rs")
    # вставка MER вверху
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER_niznie, x1=360, y1=302, x2=385, y2=317,
                               text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina,anchor="rs")
    # вставка MER ниже
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=360, y1=342, x2=385, y2=357,
                               text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina,anchor="rs")

    # вставка BER
    menaem_parametri_na_nuznie(draw, replace_text="0.0E-09", x1=353, y1=402, x2=402, y2=417, text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina,anchor="rs")
    # вставка BER
    menaem_parametri_na_nuznie(draw, replace_text="0.0E-09", x1=531, y1=402, x2=577, y2=417, text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina,anchor="rs")
    # вставка BER
    menaem_parametri_na_nuznie(draw, replace_text=f"0.0E-0{bb_BER}", x1=323, y1=422, x2=371, y2=437, text_color=(0, 0, 165),
                               bg_color=(189, 190, 189), font=font_seredina,anchor="rs")

    img.save(output_path)
    return img


def find_and_replace_text_in_image_2(input_path, output_path, replace_text_date_protocol, replace_text_chastota,
                                     replace_text_MER, replace_text_MER_niznie, replace_text_frequency_niznie,
                                     time_date_protocol,vnutrennia_power,atenuazia_vezde,symbol_rate_ofset):
    """ОТКРЫВАЕМ И СОХРАНЯЕМ ДАННЫЕ"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_seredina = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf", size=15)
    font_seredina2 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf", size=16)
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
    # # вставка атеньюация
    # menaem_parametri_na_nuznie(draw, replace_text=atenuazia_vezde, x1=599, y1=125, x2=613, y2=137,
    #                            text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка MER
    replace_text_MER = round(replace_text_MER + random.randint(0, 5) / 10,1)
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=588, y1=366, x2=615, y2=376,
                               text_color=(0, 0, 180), bg_color=(189, 190, 189), font=font_seredina)
    # вставка MER  пониженные значение
    replace_text_MER_niznie = round(replace_text_MER_niznie + random.randint(0, 5) / 10,1)
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER_niznie, x1=588, y1=286, x2=613, y2=297,
                               text_color=(0, 0, 180), bg_color=(189, 190, 189), font=font_seredina)
    # вставка внутренней мощьности
    vnutrennia_power2=round(vnutrennia_power-random.randint(1, 4) / 10, 2)
    menaem_parametri_na_nuznie(draw, replace_text=f"  {vnutrennia_power2}", x1=564, y1=166, x2=601, y2=177,
                               text_color=(0, 0, 180), bg_color=(189, 190, 189), font=font_seredina)
    # вставка carrier frequency offset  пониженные значение
    menaem_parametri_na_nuznie(draw, replace_text=f" {replace_text_frequency_niznie}", x1=583, y1=246, x2=615, y2=258,
                               text_color=(0, 0, 180), bg_color=(189, 190, 189), font=font_seredina)
    # вставка simbol rate offset
    menaem_parametri_na_nuznie(draw, replace_text=f" {symbol_rate_ofset}", x1=580, y1=266, x2=602, y2=276,
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
                                     replace_text_MER, time_date_protocol,vnutrennia_power,atenuazia_vezde):
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
    time_date_protocol = datetime.strptime(time_date_protocol, "%H:%M") + timedelta(minutes=random.randint(0, 1))
    time_date_protocol = time_date_protocol.strftime("%H:%M")
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=367, y1=24, x2=392, y2=34,
                               text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # # вставка атенюация
    # menaem_parametri_na_nuznie(draw, replace_text=atenuazia_vezde, x1=531, y1=83, x2=545, y2=95,
    #                            text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка MER первый вариант
    replace_text_MER = round(replace_text_MER + random.randint(0, 3) / 10,1)
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=586, y1=124, x2=614, y2=136,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina2)
    # вставка внутренней мощьности
    vnutrennia_power2 = round(vnutrennia_power - random.randint(2, 5) / 10, 2)
    menaem_parametri_na_nuznie(draw, replace_text=vnutrennia_power2, x1=91, y1=124, x2=121, y2=136,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina2)
    # вставка MER второй вариант
    # replace_text_MER = round(replace_text_MER + random.randint(0, 3) / 10,1)
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=147, y1=189, x2=175, y2=199,
                               text_color=(132, 207, 255), bg_color=(0, 0, 0), font=font_seredina)
    img.save(output_path)
    return img


def find_and_replace_text_in_image_4(input_path, output_path, replace_text_neravnomernost_achh, replace_text_MER,
                                     replace_text_chastota, replace_text_date_protocol, time_date_protocol,vnutrennia_power,atenuazia_vezde):
    """ОТКРЫВАЕМ- ,ВСТАВЛЯЕМ И СОХРАНЯЕМ ДАННЫЕ"""
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
    replace_text_MER = round(replace_text_MER + random.randint(0, 5) / 10,1)
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_MER, x1=585, y1=124, x2=615, y2=134,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina)
    # вставка внутренней мощьности
    vnutrennia_power2 = round(vnutrennia_power + random.randint(2, 5) / 10, 2)
    menaem_parametri_na_nuznie(draw, replace_text=f"{vnutrennia_power2}", x1=84, y1=124, x2=121, y2=136,
                               text_color=(0, 0, 165), bg_color=(189, 190, 189), font=font_seredina)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=368, y1=24, x2=391, y2=34,
                               text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # # вставка атеньюация
    # menaem_parametri_na_nuznie(draw, replace_text=atenuazia_vezde, x1=531, y1=83, x2=545, y2=95,
    #                            text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка даты
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_date_protocol, x1=456, y1=3, x2=534, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # вставка времени
    time_date_protocol = datetime.strptime(time_date_protocol, "%H:%M") + timedelta(minutes=1)
    time_date_protocol = time_date_protocol.strftime("%H:%M")
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    img.save(output_path)
    # print(f"Заменено: '{search_text}' -> '{replace_text}'")
    # print(f"Сохранено в: {output_path}")
    return img


def find_and_replace_text_in_image_5(input_path, output_path, replace_text_chastota, replace_text_date_protocol,
                                     time_date_protocol,vnutrennia_power,atenuazia_vezde):
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
    time_date_protocol = datetime.strptime(time_date_protocol, "%H:%M") + timedelta(minutes=random.randint(1, 2))
    time_date_protocol = time_date_protocol.strftime("%H:%M")
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # # вставка атеньюация
    # menaem_parametri_na_nuznie(draw, replace_text=atenuazia_vezde, x1=85, y1=44, x2=99, y2=56,
    #                            text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
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
                                     time_date_protocol,vnutrennia_power,atenuazia_vezde):
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
    time_date_protocol = datetime.strptime(time_date_protocol, "%H:%M") + timedelta(minutes=random.randint(2, 3))
    time_date_protocol = time_date_protocol.strftime("%H:%M")
    menaem_parametri_na_nuznie(draw, replace_text=time_date_protocol, x1=548, y1=3, x2=594, y2=15,
                               text_color=(250, 250, 222), bg_color=(0, 0, 24), font=font_date)
    # # вставка атеньюация
    # menaem_parametri_na_nuznie(draw, replace_text=atenuazia_vezde, x1=85, y1=44, x2=99, y2=56,
    #                            text_color=(0, 0, 0), bg_color=(189, 190, 189), font=font_seredina)
    # вставка частота
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_chastota, x1=66, y1=425, x2=99, y2=439,
                               text_color=(250, 250, 250), bg_color=(0, 0, 0), font=font_seredina)
    # вставка внутренней мощьности
    vnutrennia_power2 = round(vnutrennia_power - random.randint(1, 10) / 10, 2)
    menaem_parametri_na_nuznie(draw, replace_text=vnutrennia_power2, x1=143, y1=64, x2=174, y2=74,
                               text_color=(247, 243, 16), bg_color=(0, 48, 123), font=font_seredina2)
    # =======вставка рандомных расчетов==========
    # =====Freq====
    freq1 = round(random.randint(7000000, 9000000) / 1000000, 6)
    freq1_str = f"{freq1:.6f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"  -{freq1_str}", x1=232, y1=124, x2=297, y2=135,
                               text_color=(255, 255, 255), bg_color=(0, 81, 206), font=font_seredina2)
    freq2 = round(random.randint(4000000, 5000000) / 1000000, 6)
    freq2_str = f"{freq2:.6f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"  -{freq2_str}", x1=232, y1=144, x2=297, y2=157,
                               text_color=(255, 255, 255), bg_color=(0, 48, 123), font=font_seredina2)
    freq3 = round(random.randint(4000000, 5000000) / 1000000, 6)
    freq3_str = f"{freq3:.6f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"   {freq3_str}", x1=232, y1=164, x2=297, y2=177,
                               text_color=(255, 255, 255), bg_color=(0, 48, 123), font=font_seredina2)
    freq4 = round(random.randint(7000000, 9000000) / 1000000, 6)
    freq4_str = f"{freq4:.6f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"   {freq4_str}", x1=232, y1=183, x2=297, y2=197,
                               text_color=(255, 255, 255), bg_color=(0, 48, 123), font=font_seredina2)
    # =====Emission====
    emis1 = round(random.randint(11000, 13000) / 100, 2)
    emis1_str = f"{emis1:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"-{emis1_str}", x1=342, y1=124, x2=387, y2=135,
                               text_color=(255, 255, 255), bg_color=(0, 81, 206), font=font_seredina2)
    emis2 = round(random.randint(10000, 11000) / 100, 2)
    emis2_str = f"{emis2:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"-{emis2_str}", x1=342, y1=144, x2=387, y2=157,
                               text_color=(255, 255, 255), bg_color=(0, 48, 123), font=font_seredina2)
    emis3 = round(random.randint(10000, 11000) / 100, 2)
    emis3_str = f"{emis3:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"-{emis3_str}", x1=342, y1=164, x2=387, y2=177,
                               text_color=(255, 255, 255), bg_color=(0, 48, 123), font=font_seredina2)
    emis4 = round(random.randint(11000, 13000) / 100, 2)
    emis4_str = f"{emis4:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"-{emis4_str}", x1=342, y1=184, x2=387, y2=198,
                               text_color=(255, 255, 255), bg_color=(0, 48, 123), font=font_seredina2)
    # =====Attenuation====
    att1 = round(random.randint(7000, 8000) / 100, 2)
    att1_str = f"{att1:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"-{att1_str}", x1=461, y1=124, x2=499, y2=135,
                               text_color=(255, 255, 255), bg_color=(0, 81, 206), font=font_seredina2)
    att2 = round(random.randint(5000, 6000) / 100, 2)
    att2_str = f"{att2:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"-{att2_str}", x1=461, y1=144, x2=499, y2=157,
                               text_color=(255, 255, 255), bg_color=(0, 48, 123), font=font_seredina2)
    att3 = round(random.randint(5000, 6000) / 100, 2)
    att3_str = f"{att3:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"-{att3_str}", x1=461, y1=164, x2=499, y2=177,
                               text_color=(255, 255, 255), bg_color=(0, 48, 123), font=font_seredina2)
    att4 = round(random.randint(7000, 8000) / 100, 2)
    att4_str = f"{att4:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"-{att4_str}", x1=461, y1=184, x2=499, y2=198,
                               text_color=(255, 255, 255), bg_color=(0, 48, 123), font=font_seredina2)
    # =====Margin====
    mar1 = round(random.randint(1000, 1999) / 100, 2)
    mar1_str = f"{mar1:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"{mar1_str}", x1=568, y1=124, x2=599, y2=135,
                               text_color=(0, 223, 0), bg_color=(0, 81, 206), font=font_seredina2)
    mar2 = round(random.randint(1000, 1999) / 100, 2)
    mar2_str = f"{mar2:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"{mar2_str}", x1=568, y1=144, x2=599, y2=157,
                               text_color=(0, 223, 0), bg_color=(0, 48, 123), font=font_seredina2)
    mar3 = round(random.randint(1000, 1999) / 100, 2)
    mar3_str = f"{mar3:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"{mar3_str}", x1=568, y1=164, x2=599, y2=177,
                               text_color=(0, 223, 0), bg_color=(0, 48, 123), font=font_seredina2)
    mar4 = round(random.randint(1000, 1999) / 100, 2)
    mar4_str = f"{mar4:.2f}"
    menaem_parametri_na_nuznie(draw, replace_text=f"{mar4_str}", x1=568, y1=184, x2=599, y2=198,
                               text_color=(0, 223, 0), bg_color=(0, 48, 123), font=font_seredina2)

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
                               text_color=(0, 15, 27), bg_color=(256, 256, 256), font=font_seredina)
    # вставка аттенюация
    menaem_parametri_na_nuznie(draw, replace_text=replace_text_atenuazia, x1=1086, y1=801, x2=1144, y2=826,
                               text_color=(0, 15, 27), bg_color=(256, 256, 256), font=font_seredina)
    img.save(output_path)
    return img


if __name__ == "__main__":
    pass
    # # =========До начала изменения пропишу все параметры чтобы не запутаться=========
    # replace_text_date_protocol = "10/07/2026"
    # replace_text_chastota = 555
    # replace_text_neravnomernost_achh = 0.9
    # replace_text_MER = "40.9"
    # replace_text_MER_niznie = round(float(replace_text_MER) - float(random.randint(2, 15) / 10), 1)
    # replace_text_frequency_offset = "-0.4"
    # replace_text_frequency_niznie = round(float(replace_text_frequency_offset) - float(random.randint(1, 4) / 10), 1)
    # time_date_protocol = f"{random.randint(12, 15)}:{random.randint(10, 57)}"
    # replace_text_power = 20.5
    # replace_text_atenuazia = random.randint(45, 55)
    # vnutrennia_power = round(random.randint(-1402, -1002) / 100, 1)
    # # =========До начала изменения пропишу все параметры чтобы не запутаться=========
    # # переделывание 1 картинки
    # input_image_1 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux2/1.png"
    # output_image_1 = "output_modified.png"
    # find_and_replace_text_in_image_1(input_path=input_image_1, output_path=output_image_1,
    #                                  replace_text_date_protocol=replace_text_date_protocol,
    #                                  replace_text_chastota=replace_text_chastota,
    #                                  replace_text_frequency_offset=replace_text_frequency_offset,
    #                                  time_date_protocol=time_date_protocol, replace_text_MER=replace_text_MER,
    #                                  replace_text_MER_niznie=replace_text_MER_niznie,vnutrennia_power=vnutrennia_power)
    # # переделывание 2 картинки
    # input_image_2 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux2/2.png"
    # output_image_2 = "output_modified_2.png"
    # find_and_replace_text_in_image_2(input_path=input_image_2, output_path=output_image_2,
    #                                  replace_text_date_protocol=replace_text_date_protocol,
    #                                  replace_text_chastota=replace_text_chastota, replace_text_MER=replace_text_MER,
    #                                  replace_text_MER_niznie=replace_text_MER_niznie,
    #                                  replace_text_frequency_niznie=replace_text_frequency_niznie,
    #                                  time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)
    # # переделывание 3 картинки
    # input_image_3 = f"/home/sem/py/pdf_name/data_base_py/3_etalon.png"
    # output_image_3 = "output_modified_3.png"
    # find_and_replace_text_in_image_3(input_path=input_image_3, output_path=output_image_3,
    #                                  replace_text_date_protocol=replace_text_date_protocol,
    #                                  replace_text_chastota=replace_text_chastota, replace_text_MER=replace_text_MER,
    #                                  time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)
    #
    # # переделывание 4 картинки
    # input_image_4 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux2/4.png"
    # output_image_4 = "output_modified_4.png"
    # find_and_replace_text_in_image_4(input_path=input_image_4, output_path=output_image_4,
    #                                  replace_text_neravnomernost_achh=replace_text_neravnomernost_achh,
    #                                  replace_text_MER=replace_text_MER, replace_text_chastota=replace_text_chastota,
    #                                  replace_text_date_protocol=replace_text_date_protocol,
    #                                  time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)
    # # переделывание 5 картинки
    # input_image_5 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux2/5.png"
    # output_image_5 = "output_modified_5.png"
    # find_and_replace_text_in_image_5(input_path=input_image_5, output_path=output_image_5,
    #                                  replace_text_chastota=replace_text_chastota,
    #                                  replace_text_date_protocol=replace_text_date_protocol,
    #                                  time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)
    # # переделывание 6 картинки
    # input_image_6 = "do_nachalo_new_protocol/2026-06-15 Кункас/mux2/6.png"
    # output_image_6 = "output_modified_6.png"
    # find_and_replace_text_in_image_6(input_path=input_image_6, output_path=output_image_6,
    #                                  replace_text_chastota=replace_text_chastota,
    #                                  replace_text_date_protocol=replace_text_date_protocol,
    #                                  time_date_protocol=time_date_protocol,vnutrennia_power=vnutrennia_power)
    # # переделывание power
    # input_image_p = f"/home/sem/py/pdf_name/data_base_py/power_etalon.png"
    # output_image_p = "output_modified_power.png"
    # find_and_replace_text_in_image_7(input_path=input_image_p, output_path=output_image_p,
    #                                  replace_text_chastota=replace_text_chastota, replace_text_power=replace_text_power,
    #                                  replace_text_atenuazia=replace_text_atenuazia)
