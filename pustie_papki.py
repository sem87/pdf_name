import os
import shutil
import random

# Словар=ь: название -> дата
# data = {
#     "Уфа": "2026-10-05",
#     "Новокуктово": "2026-10-06",
#     "Старогусево": "2026-11-16",
# }
data = {

    "Абдрахимово": "2026-10-06",

    "Абдуллино": "2026-07-15",

    "Абдулово": "2026-08-19",

    "Абзаково": "2026-10-05",

    "Абзаново": "2026-08-19",

    "Аксаитово": "2026-07-06"
}
SRC_DIR = "/home/sem/py/pdf_name/data_base_py/fhoto_data_base"
BASE_DIR = "/home/sem/py/pdf_name/pustie"

# Все png файлы в источнике
all_files = [f for f in os.listdir(SRC_DIR) if f.endswith(".png")]

for name, date in data.items():
    # Создаём папку с названием
    project_dir = os.path.join(BASE_DIR, f"{date} {name}")
    os.makedirs(project_dir, exist_ok=True)

    for mux in ["1mux", "2mux"]:
        mux_dir = os.path.join(project_dir, mux)
        os.makedirs(mux_dir, exist_ok=True)

        # ========================================
        # Рандомно выбираем 6 файлов
        # chosen = random.sample(all_files, 6)
        #
        # for i, src_file in enumerate(chosen, start=1):
        #     dst = os.path.join(mux_dir, f"{i}.png")
        #     shutil.copy2(os.path.join(SRC_DIR, src_file), dst)
        #     print(f"{mux_dir}: {src_file} -> {i}.png")

        num = random.randint(1, 5)

        for i in range(1, 7):
            src_file = f"{num}{i}.png"
            src_path = os.path.join(SRC_DIR, src_file)
            dst = os.path.join(mux_dir, f"{i}.png")

            if os.path.exists(src_path):
                shutil.copy2(src_path, dst)
                print(f"{mux_dir}: {src_file} -> {i}.png")
            else:
                print(f"Файл {src_file} не найден в {SRC_DIR}")

print("Готово.")
