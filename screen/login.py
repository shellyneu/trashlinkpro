import tkinter as tk
from PIL import Image, ImageTk

class LoginPage(tk.Frame):
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

        canvas.create_text(500, 170, text="Login", fill="#2f4f12", font=("Inter", 28, "bold"))
        
        nim_label = tk.Label(self, text="NIM", font=("Inter", 14, "bold"), bg="white", fg="#2f4f12")
        nim_label.place(x=305, y=275)

        vcmd = (self.register(self.validate_numbers), "%P")
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
            validatecommand=vcmd
        )
        self.nim_entry.place(x=295, y=305, width=450, height=40)

        
        button_img = Image.open("./assets/button.png").resize((200, 50)).convert("RGBA")
        canvas.button = ImageTk.PhotoImage(button_img)
        
        cancel_btn = tk.Button(self, image=canvas.button, text="Cancel", font=("Inter", 12, "bold"), fg="#2f4f12",
                                compound="center", bd=0, bg="white", activebackground="white",
                                command=lambda: controller.show_frame("StartPage"))
        cancel_btn.place(x=80, y=480, width=200, height=50)

        input_ = tk.Button(self, image=canvas.button, text="Login", font=("Inter", 12, "bold"), fg="#2f4f12",
                                    compound="center", bd=0, bg="white", activebackground="white",
                                    command=lambda: controller.show_frame("InputPage"))
        input_.place(x=750, y=480, width=200, height=50)

    def reset_form(self):
        self.nim_entry.delete(0, tk.END)

    def validate_numbers(self, text):
        return text.isdigit() or text == ""