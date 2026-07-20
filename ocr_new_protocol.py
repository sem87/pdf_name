import os
import re
import shutil
from pathlib import Path
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Параметры
INPUT_FOLDER = "do_nachalo_new_protocol/2026-06-15 Кункас/mux1/1.png"
DPI = 300
TESSERACT_LANG = 'eng'
TESSERACT_CONFIG = '--psm 6'


def create_ocr_optimized_image(image_path):
    """
    Создает оптимизированную для OCR версию изображения (ч/б, бинаризованная)
    """
    # Открываем изображение
    img = Image.open(image_path)
    img_array = np.array(img)

    # Если изображение цветное, конвертируем в оттенки серого
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array

    # Применяем бинаризацию (пороговую обработку)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Увеличиваем резкость
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(binary, -1, kernel)

    return Image.fromarray(sharpened)


def recognize_text_from_image(image_path, lang=TESSERACT_LANG, config=TESSERACT_CONFIG):
    """
    Распознавание текста с изображения
    Возвращает: текст, данные bounding boxes, оригинальное цветное изображение
    """
    # Открываем оригинальное цветное изображение
    original_img = Image.open(image_path)
    original_img.info['dpi'] = (DPI, DPI)

    # Создаем оптимизированную версию для OCR
    ocr_img = create_ocr_optimized_image(image_path)

    # Распознавание текста с обработанного изображения
    text = pytesseract.image_to_string(
        ocr_img,
        lang=lang,
        config=config
    )

    # Получаем данные о bounding boxes
    data = pytesseract.image_to_data(
        ocr_img,
        lang=lang,
        config=config,
        output_type=pytesseract.Output.DICT
    )

    return text, data, original_img


def extract_parameters(text):
    """
    Извлечение параметров из распознанного текста
    """
    parameters = {}

    # Частота
    freq_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:MHz|kHz|Hz)', text)
    if freq_match:
        parameters['frequency'] = freq_match.group(0)

    # Мощность
    power_match = re.search(r'(-?\d+(?:\.\d+)?)\s*dBm', text)
    if power_match:
        parameters['power'] = power_match.group(0)

    # HEX значения
    hex_match = re.search(r'HEX\s*([0-9A-F]+)', text, re.IGNORECASE)
    if hex_match:
        parameters['hex'] = hex_match.group(1)

    return parameters


def replace_image_in_pdf(pdf_path, page_num, new_image_path, output_path, position=(100, 100, 500, 400)):
    """
    Замена/вставка изображения в PDF
    Использует PyMuPDF (fitz)
    """
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(pdf_path)
        page = doc[page_num]

        # Создаем прямоугольник для вставки
        rect = fitz.Rect(position)

        # Вставляем изображение
        page.insert_image(rect, filename=new_image_path)

        # Сохраняем
        doc.save(output_path)
        doc.close()

        print(f"PDF сохранен: {output_path}")
        return True
    except ImportError:
        print("Установите PyMuPDF: pip install PyMuPDF")
        return False
    except Exception as e:
        print(f"Ошибка при замене изображения в PDF: {e}")
        return False


def process_and_save_image(input_path, output_path=None, dpi=DPI):
    """
    Основная функция обработки изображения
    Возвращает распознанный текст и параметры
    """
    if output_path is None:
        output_path = "output_color_image.png"

    # Распознаем текст
    recognized_text, data, original_img = recognize_text_from_image(input_path)

    # Сохраняем оригинальное цветное изображение
    original_img.save(output_path, dpi=(dpi, dpi))
    print(f"Цветное изображение сохранено: {output_path}")

    # Извлекаем параметры
    params = extract_parameters(recognized_text)

    return recognized_text, params, data, original_img


# Основной код
if __name__ == "__main__":
    # Проверяем существование файла
    if not os.path.exists(INPUT_FOLDER):
        print(f"Файл не найден: {INPUT_FOLDER}")
    else:
        print("=" * 60)
        print(f"ОБРАБОТКА ФАЙЛА: {INPUT_FOLDER}")
        print("=" * 60)

        # Обрабатываем и сохраняем цветное изображение
        recognized_text, params, data, original_img = process_and_save_image(
            INPUT_FOLDER,
            output_path="output_color_image.png"
        )

        print("\n" + "=" * 60)
        print("РАСПОЗНАННЫЙ ТЕКСТ:")
        print("=" * 60)
        print(recognized_text)
        print("=" * 60)

        print("\nИЗВЛЕЧЕННЫЕ ПАРАМЕТРЫ:")
        print("-" * 60)
        if params:
            for key, value in params.items():
                print(f"{key:20}: {value}")
        else:
            print("Параметры не найдены")
        print("-" * 60)

        # Пример замены изображения в PDF (раскомментируйте и заполните данные)
        # pdf_file = "your_document.pdf"
        # output_pdf = "document_with_new_image.pdf"
        # replace_image_in_pdf(pdf_file, 0, "output_color_image.png", output_pdf)