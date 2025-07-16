import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        self.setup_layout()

    def setup_layout(self):
        self.bg_image = Image.open("./assets/background.png").convert("RGBA")
        self.logo_image = Image.open("./assets/logo.png").resize((100, 100))
        self.button_image = Image.open("./assets/button.png").resize((200, 50)).convert("RGBA")
        
        self.bg_img = ImageTk.PhotoImage(self.bg_image)
        self.logo_img = ImageTk.PhotoImage(self.logo_image)
        self.button_img = ImageTk.PhotoImage(self.button_image)
        
        self.bg_item = self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        self.logo_item = self.canvas.create_image(0, 0, image=self.logo_img, anchor="nw")
        self.title_text = self.canvas.create_text(0, 0, text="Register", fill="#2f4f12", font=("Inter", 28, "bold"))
        
        self.nama_label = tk.Label(self, text="Nama", font=("Inter", 14, "bold"), bg="white", fg="#2f4f12")
        
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

        self.nim_label = tk.Label(self, text="NIM", font=("Inter", 14, "bold"), bg="white", fg="#2f4f12")

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
        
        self.cancel_btn = tk.Button(self, image=self.button_img, text="Cancel", font=("Inter", 12, "bold"), fg="#2f4f12",
                                   compound="center", bd=0, bg="white", activebackground="white",
                                   command=lambda: self.controller.show_frame("StartPage"))
        
        self.register_btn = tk.Button(self, image=self.button_img, text="Register", font=("Inter", 12, "bold"), fg="#2f4f12",
                                     compound="center", bd=0, bg="white", activebackground="white",
                                     command=self.register_user)
        
        self.update_layout()

    def on_canvas_resize(self, event):
        self.update_layout()

    def update_layout(self):
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        bg_width, bg_height = self.bg_image.size
        scale_x = width / bg_width
        scale_y = height / bg_height
        scale = min(scale_x, scale_y)
        
        new_width = int(bg_width * scale)
        new_height = int(bg_height * scale)
        
        scaled_bg = self.bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(scaled_bg)
        
        self.canvas.itemconfig(self.bg_item, image=self.bg_img)
        self.canvas.coords(self.bg_item, width, height)
        self.canvas.itemconfig(self.bg_item, anchor="se")
        
        logo_margin = max(20, width * 0.02)
        self.canvas.coords(self.logo_item, logo_margin, logo_margin)
        
        center_x = width // 2
        title_y = height * 0.28
        self.canvas.coords(self.title_text, center_x, title_y)
        
        form_width = min(450, width * 0.6)
        form_x = (width - form_width) // 2
        
        name_label_y = height * 0.38
        name_entry_y = height * 0.43
        
        self.nama_label.place(x=form_x + 10, y=name_label_y)
        self.nama_entry.place(x=form_x, y=name_entry_y, width=form_width, height=40)
        
        nim_label_y = height * 0.52
        nim_entry_y = height * 0.57
        
        self.nim_label.place(x=form_x + 10, y=nim_label_y)
        self.nim_entry.place(x=form_x, y=nim_entry_y, width=form_width, height=40)
        
        button_y = height - 70
        button_margin = max(80, width * 0.08)
        
        self.cancel_btn.place(x=button_margin, y=button_y, width=200, height=50)
        self.register_btn.place(x=width - button_margin - 200, y=button_y, width=200, height=50)

    def reset_form(self):
        self.nama_entry.delete(0, tk.END)
        self.nim_entry.delete(0, tk.END)

    def register_user(self):
        nama = self.nama_entry.get().strip()
        nim = self.nim_entry.get().strip()
        
        if not nama or not nim:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, message = self.controller.db.register_user(nama, nim)
        
        if success:
            messagebox.showinfo("Success", message)
            self.reset_form()
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Error", message)

    def validate_letters(self, text):
        return text.replace(" ", "").isalpha() or text == "" 

    def validate_numbers(self, text):
        return text.isdigit() or text == "" 