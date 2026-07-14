from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np


def replace_carrier_frequency_offset(input_image_path, output_image_path, new_value="0.7"):
    """
    Заменяет значение Carrier Frequency Offset на изображении
    """
    # Открываем изображение
    img = Image.open(input_image_path)
    draw = ImageDraw.Draw(img)

    # Координаты области значения Carrier Frequency Offset
    # (настройте под ваше изображение)
    # Примерные координаты для вашего скриншота:
    x1, y1 = 520, 395  # левый верхний угол
    x2, y2 = 620, 420  # правый нижний угол

    # Цвет фона (серый, как на изображении)
    bg_color = (210, 210, 210)  # светло-серый

    # Закрашиваем область старым значением
    draw.rectangle([x1, y1, x2, y2], fill=bg_color)

    # Пробуем загрузить шрифт (можно изменить на свой)
    try:
        # Для Linux
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except:
        try:
            # Для Windows
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
        except:
            # Стандартный шрифт
            font = ImageFont.load_default()

    # Текст с новым значением
    text = f"{new_value} Hz"
    text_color = (0, 0, 180)  # темно-синий, как на оригинальном изображении

    # Вычисляем позицию для центрирования текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x_text = x1 + (x2 - x1 - text_width) // 2
    y_text = y1 + (y2 - y1 - text_height) // 2

    # Рисуем новый текст
    draw.text((x_text, y_text), text, fill=text_color, font=font)

    # Сохраняем результат
    img.save(output_image_path)
    print(f"Изображение сохранено: {output_image_path}")
    return img


def replace_carrier_frequency_offset_auto(input_image_path, output_image_path, new_value="0.7"):
    """
    Автоматический поиск и замена значения Carrier Frequency Offset
    с использованием OpenCV и шаблонов
    """
    # Открываем изображение
    img = Image.open(input_image_path)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    draw = ImageDraw.Draw(img)

    # Ищем строку "Carrier Frequency Offset"
    # Координаты примерные - нужно настроить или использовать OCR
    label_y = 395  # Y-координата строки

    # Область где находится значение (справа от метки)
    value_x_start = 520
    value_x_end = 620
    value_y_start = 395
    value_y_end = 420

    # Закрашиваем старое значение
    bg_color = (210, 210, 210)
    draw.rectangle([value_x_start, value_y_start, value_x_end, value_y_end], fill=bg_color)

    # Загружаем шрифт
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
        except:
            font = ImageFont.load_default()

    # Новый текст
    text = f"{new_value} Hz"
    text_color = (0, 0, 180)

    # Позиция текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x_text = value_x_start + (value_x_end - value_x_start - text_width) // 2
    y_text = value_y_start + (value_y_end - value_y_start - text_height) // 2

    draw.text((x_text, y_text), text, fill=text_color, font=font)

    # Сохраняем
    img.save(output_image_path)
    print(f"Изображение сохранено: {output_image_path}")
    return img


def find_and_replace_text_in_image(input_path, output_path, search_text="304.7", replace_text="0.7", unit="Hz"):
    """
    Универсальная функция поиска и замены текста на изображении
    """
    from PIL import Image, ImageDraw, ImageFont

    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)

    # Для вашего конкретного изображения - координаты
    # Carrier Frequency Offset находится примерно на строке 11 таблицы

    # Координаты значения (настройте под ваше изображение)
    coords = {
        'x1': 520,
        'y1': 395,
        'x2': 620,
        'y2': 420
    }

    # Закрашиваем область
    bg_color = (210, 210, 210)
    draw.rectangle([coords['x1'], coords['y1'], coords['x2'], coords['y2']], fill=bg_color)

    # Шрифт
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except:
        font = ImageFont.load_default()

    # Новый текст
    text = f"{replace_text} {unit}"
    text_color = (0, 0, 180)

    # Центрирование
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x_text = coords['x1'] + (coords['x2'] - coords['x1'] - text_width) // 2
    y_text = coords['y1'] + (coords['y2'] - coords['y1'] - text_height) // 2

    draw.text((x_text, y_text), text, fill=text_color, font=font)

    img.save(output_path)
    print(f"Заменено: '{search_text}' -> '{replace_text}'")
    print(f"Сохранено в: {output_path}")

    return img


# Основной код
if __name__ == "__main__":
    input_image = "do_nachalo_new_protocol/2026-06-15 Кункас/mux1/01.png"
    output_image = "output_modified.png"

    # Проверяем существование файла
    import os

    if os.path.exists(input_image):
        # Заменяем значение
        result_img = find_and_replace_text_in_image(
            input_image,
            output_image,
            search_text="304.7",
            replace_text="0.7",
            unit="Hz"
        )

        print("\nГотово! Значение Carrier Frequency Offset изменено на 0.7 Hz")
    else:
        print(f"Файл не найден: {input_image}")