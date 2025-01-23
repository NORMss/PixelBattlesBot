import tkinter as tk
import json

colors = [
    "deepcarmine", "flame", "yelloworange", "naplesyellow", "mediumseagreen", "emerald",
    "inchworm", "myrtlegreen", "verdigris", "cyancobaltblue", "unitednationsblue", "mediumskyblue",
    "oceanblue", "VeryLightBlue", "grape", "purpleplum", "darkpink", "mauvelous",
    "coffee", "coconut", "black", "philippinegray", "lightsilver", "white", "transparent"
]
palette = [
    "#ae233d", "#ec5427", "#f4ab3c", "#f9d759", "#48a06d", "#5cc87f", "#9ae96c",
    "#317270", "#469ca8", "#2d519e", "#4d90e3", "#7ee6f2", "#4440ba", "#6662f6",
    "#772b99", "#a754ba", "#eb4e81", "#f19eab", "#684a34", "#956a34", "#000000",
    "#898d90", "#d5d7d9", "#ffffff", "#919191"  # Transparent color
]

class PixelArtEditor:
    def __init__(self, root, rows=24, cols=24):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.matrix = [["skip" for _ in range(cols)] for _ in range(rows)]
        self.current_color = "skip"
        self.zoom_factor = 1  # начальный масштаб

        self.create_controls()
        self.create_palette()
        self.create_canvas()

    def create_controls(self):
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(side=tk.TOP)

        self.size_label = tk.Label(controls_frame, text=f"Размер: {self.rows}x{self.cols}")
        self.size_label.pack(side=tk.LEFT)

        # Кнопки для изменения размера холста
        self.increase_button = tk.Button(controls_frame, text="Увеличить", command=self.increase_size)
        self.increase_button.pack(side=tk.LEFT)
        self.decrease_button = tk.Button(controls_frame, text="Уменьшить", command=self.decrease_size)
        self.decrease_button.pack(side=tk.LEFT)

        # Кнопки для изменения масштаба
        self.zoom_in_button = tk.Button(controls_frame, text="Приблизить", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT)
        self.zoom_out_button = tk.Button(controls_frame, text="Отдалить", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT)

    def create_palette(self):
        palette_frame = tk.Frame(self.root)
        palette_frame.pack(side=tk.TOP)

        for i, color in enumerate(colors):
            button = tk.Button(
                palette_frame, bg=palette[i], width=3, height=1,
                command=lambda c=color: self.set_color(c)
            )
            button.pack(side=tk.LEFT)

    def create_canvas(self):
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack()

        self.buttons = []
        for y in range(self.rows):
            row = []
            for x in range(self.cols):
                button = tk.Button(
                    self.canvas_frame, bg="white", width=4, height=2,
                    command=lambda r=y, c=x: self.set_pixel(r, c)
                )
                button.grid(row=y, column=x)
                row.append(button)
            self.buttons.append(row)

    def set_color(self, color):
        self.current_color = color

    def set_pixel(self, row, col):
        self.matrix[row][col] = self.current_color
        hex_color = palette[colors.index(self.current_color)] if self.current_color != "transparent" else "#ffffff00"
        self.buttons[row][col].configure(bg=hex_color)

    def increase_size(self):
        self.rows += 1
        self.cols += 1
        self.update_canvas_size()

    def decrease_size(self):
        if self.rows > 1 and self.cols > 1:
            self.rows -= 1
            self.cols -= 1
            self.update_canvas_size()

    def update_canvas_size(self):
        # Обновление размеров холста
        for row in self.buttons:
            for button in row:
                button.grid_forget()

        self.buttons = []
        for y in range(self.rows):
            row = []
            for x in range(self.cols):
                button = tk.Button(
                    self.canvas_frame, bg="white", width=4, height=2,
                    command=lambda r=y, c=x: self.set_pixel(r, c)
                )
                button.grid(row=y, column=x)
                row.append(button)
            self.buttons.append(row)

        self.size_label.config(text=f"Размер: {self.rows}x{self.cols}")

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_zoom()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_zoom()

    def update_zoom(self):
        for row in self.buttons:
            for button in row:
                new_width = int(4 * self.zoom_factor)
                new_height = int(2 * self.zoom_factor)
                button.config(width=new_width, height=new_height)

    def save_json(self):
        with open("output.json", "w") as f:
            json.dump(self.matrix, f, indent=4)
        print("JSON-матрица сохранена в файл output.json")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pixel Art Editor")
    editor = PixelArtEditor(root)

    save_button = tk.Button(root, text="Сохранить", command=editor.save_json)
    save_button.pack()

    root.mainloop()
