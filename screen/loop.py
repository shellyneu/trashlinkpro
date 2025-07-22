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

        button_img = Image.open("./assets/button.png").resize((200, 50)).convert("RGBA")
        canvas.button = ImageTk.PhotoImage(button_img)

        input_again_btn = tk.Button(self, image=canvas.button, text="Tambah Lagi", font=("Inter", 12, "bold"), fg="#2f4f12",
                                        compound="center", bd=0, bg="white", activebackground="white",
                                        command=lambda: controller.show_frame("InputPage"))
        input_again_btn.place(x=80, y=520, width=200, height=50)

        finish_btn = tk.Button(self, image=canvas.button, text="Selesai", font=("Inter", 12, "bold"), fg="#2f4f12",
                                        compound="center", bd=0, bg="white", activebackground="white",
                                        command=lambda: controller.show_frame("EndPage"))
        finish_btn.place(x=750, y=520, width=200, height=50)

