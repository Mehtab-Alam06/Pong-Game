import tkinter as tk
from PIL import Image, ImageTk

def start_screen():
    def on_option_selected(option):
        print(f"Selected: {option}")
        root.destroy()

    # Initialize window
    root = tk.Tk()
    root.title("Retro Start Screen")

    # Load background image
    bg_image = Image.open("pixel-art-design-outdoor-landscape-background-ui-colorful-arcade-screen-game-banner-button-start-concept-retro-style-196261037")
    bg_image = bg_image.resize((800, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create canvas for background
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Options from the existing program
    options = ["Start Game", "Settings", "Credits", "Exit"]

    # Create buttons with retro styling
    button_font = ("Press Start 2P", 20)
    button_color = "#FFD700"

    for i, option in enumerate(options):
        btn = tk.Button(root, text=option, font=button_font, bg=button_color, command=lambda opt=option: on_option_selected(opt))
        btn_window = canvas.create_window(300, 300 + i * 60, anchor="nw", window=btn)

    root.mainloop()

start_screen()