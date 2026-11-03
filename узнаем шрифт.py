from PIL import Image, ImageDraw, ImageFont
import os

# Твой список (убраны дубликаты и PFB/T1 — PIL их плохо читает)
fonts = [

"/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
"/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf",
"/usr/share/fonts/truetype/msttcorefonts/Arial_Italic.ttf",
"/usr/share/fonts/truetype/msttcorefonts/Arial_Bold_Italic.ttf",
"/usr/share/fonts/truetype/msttcorefonts/arialn.ttf",
"/usr/share/fonts/truetype/msttcorefonts/arialnb.ttf",
"/usr/share/fonts/truetype/msttcorefonts/arialni.ttf",
"/usr/share/fonts/truetype/msttcorefonts/arialnbi.ttf",

"/usr/share/fonts/truetype/msttcorefonts/ariblk.ttf",
"/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf",
"/usr/share/fonts/truetype/msttcorefonts/ariali.ttf",
"/usr/share/fonts/truetype/msttcorefonts/arialbi.ttf"
]

# Убираем дубликаты, оставляем только существующие файлы
fonts = list(dict.fromkeys(f for f in fonts if os.path.exists(f)))

# Параметры
SIZE = 16
LINE_H = 32          # высота одной строки
PAD = 10
TEST_TEXT = "1234567890 1"

# Считаем ширину по самому длинному пути + текст
max_path_len = max(len(os.path.basename(f)) for f in fonts)
W = max(900, max_path_len * 10 + 250)
H = len(fonts) * LINE_H + PAD * 2

img = Image.new('RGB', (W, H), 'white')
draw = ImageDraw.Draw(img)

y = PAD
ok = 0
err = 0

for fp in fonts:
    name = os.path.basename(fp)
    try:
        font = ImageFont.truetype(fp, SIZE)
        # Цифры
        draw.text((PAD, y), TEST_TEXT, fill='black', font=font)
        # Название шрифта — синим
        draw.text((PAD + 200, y), name, fill='blue', font=font)
        ok += 1
    except Exception as e:
        draw.text((PAD, y), f"ERR: {name} — {e}", fill='red')
        err += 1
    y += LINE_H

out = '/tmp/all_fonts.png'
img.save(out)
print(f"Готово: {out}")
print(f"OK: {ok}, ошибок: {err}, всего: {len(fonts)}")