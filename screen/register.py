import tkinter as tk
from PIL import Image, ImageTk

class RegisterPage(tk.Frame):
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

        canvas.create_text(512, 170, text="Register", fill="#2f4f12", font=("Inter", 28, "bold"))
        
        nama_label = tk.Label(self, text="Nama", font=("Inter", 14, "bold"), bg="white", fg="#2f4f12")
        nama_label.place(x=305, y=230)
        
        vcmd_letters = (self.register(self.validate_letters), "%P")
        self.nama_entry = tk.Entry(
            self,
            font=("Inter", 14),
            bg="white",
            fg="#2f4f12",
            bd=0,
            highlightthickness=2,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
            relief="flat",
            insertbackground="#2E8B57",
            validate="key",
            validatecommand=vcmd_letters
        )
        self.nama_entry.place(x=295, y=260, width=450, height=40)

        nim_label = tk.Label(self, text="NIM", font=("Inter", 14, "bold"), bg="white", fg="#2f4f12")
        nim_label.place(x=305, y=315)

        vcmd_numbers = (self.register(self.validate_numbers), "%P")
        self.nim_entry = tk.Entry(
            self,
            font=("Inter", 14),
            bg="white",
            fg="#2f4f12",
            bd=0,
            highlightthickness=2,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
            relief="flat",
            insertbackground="#2E8B57",
            validate="key",
            validatecommand=vcmd_numbers
        )
        self.nim_entry.place(x=295, y=345, width=450, height=40)

        
        button_img = Image.open("./assets/button.png").resize((200, 50)).convert("RGBA")
        canvas.button = ImageTk.PhotoImage(button_img)
        
        cancel_btn = tk.Button(self, image=canvas.button, text="Cancel", font=("Inter", 12, "bold"), fg="#2f4f12",
                                compound="center", bd=0, bg="white", activebackground="white",
                                command=lambda: controller.show_frame("StartPage"))
        cancel_btn.place(x=80, y=520, width=200, height=50)

        register_btn = tk.Button(self, image=canvas.button, text="Register", font=("Inter", 12, "bold"), fg="#2f4f12",
                                    compound="center", bd=0, bg="white", activebackground="white",
                                    command=lambda: controller.show_frame("LoginPage"))
        register_btn.place(x=750, y=520, width=200, height=50)

    def reset_form(self):
        self.nama_entry.delete(0, tk.END)
        self.nim_entry.delete(0, tk.END)
        pass

    def validate_letters(self, text):
        return text.isalpha() or text == "" 

    def validate_numbers(self, text):
        return text.isdigit() or text == "" 