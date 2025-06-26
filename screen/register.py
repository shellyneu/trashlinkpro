import tkinter as tk

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Register Page", font=("Inter", 24, "bold"), bg="white").pack(pady=250)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage")).pack()