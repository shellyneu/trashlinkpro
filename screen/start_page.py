import tkinter as tk
from PIL import Image, ImageTk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        canvas = tk.Canvas(self, width=1024, height=550, bg="white", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        bg_image = Image.open("./assets/background.png").convert("RGBA")
        canvas.bg_img = ImageTk.PhotoImage(bg_image)
        canvas.create_image(1024, 550, image=canvas.bg_img, anchor="se")

        logo = Image.open("./assets/logo.png").resize((100, 100))
        canvas.logo = ImageTk.PhotoImage(logo)
        canvas.create_image(23, 22, image=canvas.logo, anchor="nw")

        canvas.create_text(500, 250, text="Welcome to", fill="#2f4f12", font=("Inter", 28, "bold"))
        canvas.create_text(500, 300, text="TRASHLINK PRO", fill="#2f4f12", font=("Inter", 32, "bold"))

        button_img = Image.open("./assets/button.png").resize((200, 50)).convert("RGBA")
        canvas.button = ImageTk.PhotoImage(button_img)

        login_btn = tk.Button(self, image=canvas.button, text="Login", font=("Inter", 12, "bold"), fg="#2f4f12",
                                compound="center", bd=0, bg="white", activebackground="white",
                                command=lambda: controller.show_frame("LoginPage"))
        login_btn.place(x=80, y=480, width=200, height=50)

        register_btn = tk.Button(self, image=canvas.button, text="Register", font=("Inter", 12, "bold"), fg="#2f4f12",
                                    compound="center", bd=0, bg="white", activebackground="white",
                                    command=lambda: controller.show_frame("RegisterPage"))
        register_btn.place(x=750, y=480, width=200, height=50)