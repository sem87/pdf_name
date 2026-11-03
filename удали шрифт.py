from PIL import Image, ImageDraw, ImageFont
import subprocess
import os

# Получаем список всех шрифтов в системе
result = subprocess.run(['fc-list', '-f', '%{file}\n'], capture_output=True, text=True)
all_fonts = result.stdout.strip().split('\n')

good_fonts = []
bad_fonts = []

for font_path in all_fonts:
    font_path = font_path.strip()
    if not font_path or not os.path.exists(font_path):
        continue

    # Пропускаем курсив и italic — для данных не нужны
    lower = font_path.lower()
    if 'italic' in lower or 'oblique' in lower:
        continue

    try:
        font = ImageFont.truetype(font_path, 20)

        # Рисуем "1" и проверяем нижнюю часть
        img = Image.new('L', (30, 30), color=0)
        draw = ImageDraw.Draw(img)
        draw.text((5, 2), "1", fill=255, font=font)

        # Проверяем нижнюю строку пикселей (засечка снизу = подчёркивание)
        pixels = list(img.getdata())
        width, height = img.size
        bottom_row = pixels[(height-3)*width : (height-2)*width]

        # Если в нижних пикселях есть тёмные точки — это засечка/подчёркивание
        has_bottom = any(p > 128 for p in bottom_row)

        if not has_bottom:
            good_fonts.append(font_path)
        else:
            bad_fonts.append(font_path)

    except Exception:
        pass

print(f"\n=== ПОДХОДЯТ ({len(good_fonts)}) ===")
for f in good_fonts:
    print(f"    \"{f}\",")

print(f"\n=== НЕ ПОДХОДЯТ ({len(bad_fonts)}) ===")
for f in bad_fonts[:20]:
    print(f"    {f}")