import qrcode
import json

# Палитра цветов
colors = [
    "deepcarmine", "flame", "yelloworange", "naplesyellow", "mediumseagreen", "emerald",
    "inchworm", "myrtlegreen", "verdigris", "cyancobaltblue", "unitednationsblue", "mediumskyblue",
    "oceanblue", "VeryLightBlue", "grape", "purpleplum", "darkpink", "mauvelous",
    "coffee", "coconut", "black", "philippinegray", "lightsilver", "white"
]

palette = [
    "#ae233d", "#ec5427", "#f4ab3c", "#f9d759", "#48a06d", "#5cc87f", "#9ae96c",
    "#317270", "#469ca8", "#2d519e", "#4d90e3", "#7ee6f2", "#4440ba", "#6662f6",
    "#772b99", "#a754ba", "#eb4e81", "#f19eab", "#684a34", "#956a34", "#000000",
    "#898d90", "#d5d7d9", "#ffffff"
]

# Генерация QR-кода в виде массива для JSON
def generate_qr_code(data, color_name):
    if color_name not in colors:
        raise ValueError("Указанный цвет отсутствует в палитре!")

    color_index = colors.index(color_name)
    color_hex = palette[color_index]

    qr = qrcode.QRCode(
        version=1,  # Минимальный размер QR-кода
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2
    )

    qr.add_data(data)
    qr.make(fit=True)

    # Генерация массива пикселей
    matrix = qr.modules
    json_matrix = []
    for row in matrix:
        json_row = []
        for cell in row:
            if cell:
                json_row.append("black")
            else:
                json_row.append("skip")
        json_matrix.append(json_row)

    return json_matrix

# Пример использования
if __name__ == "__main__":
    qr_data = "twitch.tv/bedros77"
    selected_color = "mediumskyblue"  # Укажите нужный цвет из палитры

    try:
        qr_json = generate_qr_code(qr_data, selected_color)
        # Сохранение в JSON-файл
        with open("qr_code.json", "w") as json_file:
            json.dump(qr_json, json_file, indent=4)

        print("QR-код успешно создан и сохранен в qr_code.json")
    except ValueError as e:
        print(e)
