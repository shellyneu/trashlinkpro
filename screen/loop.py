import tkinter as tk
from PIL import Image, ImageTk

class LoopPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        canvas = tk.Canvas(self, width=1024, height=600, bg="white", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        bg_image = Image.open("./assets/background.png").convert("RGBA")
        canvas.bg_img = ImageTk.PhotoImage(bg_image)
        canvas.create_image(1024, 600, image=canvas.bg_img, anchor="se")

        logo = Image.open("./assets/logo.png").resize((100, 100))
        canvas.logo = ImageTk.PhotoImage(logo)
        canvas.create_image(23, 22, image=canvas.logo, anchor="nw")

        canvas.create_text(512, 270, text="Masukkan Botol", fill="#2f4f12", font=("Inter", 28, "bold"))
        canvas.create_text(512, 320, text="Satu-Persatu", fill="#2f4f12", font=("Inter", 28, "bold"))
