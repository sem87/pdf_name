from PIL import Image, ImageDraw, ImageFont

fonts = {
    "Share Tech Mono": "/home/sem/.fonts/ShareTechMono-Regular.ttf",
    "Space Mono": "/home/sem/.fonts/SpaceMono-Regular.ttf",
    "DejaVu Sans Mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "Hack": "/usr/share/fonts/truetype/hack/Hack-Regular.ttf",
    "Ubuntu Mono": "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
}

img = Image.new('RGB', (600, 300), color='black')
draw = ImageDraw.Draw(img)

y = 10
for name, path in fonts.items():
    try:
        font = ImageFont.truetype(path, size=18)
        draw.text((10, y), f"{name}: ROHDE & SCHWARZ", fill='white', font=font)
        y += 50
    except Exception as e:
        print(f"Ошибка с {name}: {e}")

img.save('font_test.png')
print("Тест шрифтов сохранён: font_test.png")