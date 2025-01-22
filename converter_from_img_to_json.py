from PIL import Image, ImageDraw
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

# Функция для поиска ближайшего цвета
def closest_color(hex_color):
    def hex_to_rgb(h):
        return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

    rgb_color = hex_to_rgb(hex_color)
    min_distance = float("inf")
    best_match = None

    for i, hex_code in enumerate(palette):
        palette_rgb = hex_to_rgb(hex_code)
        distance = sum((rgb_color[j] - palette_rgb[j]) ** 2 for j in range(3))
        if distance < min_distance:
            min_distance = distance
            best_match = colors[i]

    return best_match

# Генерация JSON-матрицы из изображения
def generate_json_from_image(image_path, skip_color="#ffffff"):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    pixels = image.load()

    json_matrix = []
    color_matrix = []
    for y in range(height):
        row = []
        color_row = []
        for x in range(width):
            r, g, b = pixels[x, y]
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            color_name = closest_color(hex_color)
            row.append(color_name if hex_color != skip_color else "skip")
            color_row.append(hex_color if hex_color != skip_color else skip_color)
        json_matrix.append(row)
        color_matrix.append(color_row)

    return json_matrix, color_matrix

# Сохранение JSON-матрицы в файл
def save_json(matrix, output_file):
    with open(output_file, "w") as f:
        json.dump(matrix, f, indent=4)

# Генерация изображения на основе JSON-матрицы
def generate_image_from_matrix(color_matrix, output_image_path, skip_color="#ffffff"):
    height = len(color_matrix)
    width = len(color_matrix[0]) if height > 0 else 0

    new_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(new_image)

    for y in range(height):
        for x in range(width):
            hex_color = color_matrix[y][x]
            if hex_color != skip_color:
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
                draw.point((x, y), fill=rgb_color)

    new_image.save(output_image_path)
    print(f"Изображение сохранено в файл {output_image_path}")

# Пример использования
image_path = "download.png"  # Путь к изображению
output_json_file = "output.json"  # Путь для сохранения JSON
output_image_file = "output_image.bmp"  # Путь для сохранения нового изображения

matrix, color_matrix = generate_json_from_image(image_path)
save_json(matrix, output_json_file)
generate_image_from_matrix(color_matrix, output_image_file)

print(f"JSON-матрица сохранена в файл {output_json_file}")
