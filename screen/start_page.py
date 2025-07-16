import tkinter as tk
from PIL import Image, ImageTk

class StartPage(tk.Frame):
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
        self.welcome_text = self.canvas.create_text(0, 0, text="Welcome to", fill="#2f4f12", font=("Inter", 28, "bold"))
        self.title_text = self.canvas.create_text(0, 0, text="TRASHLINK PRO", fill="#2f4f12", font=("Inter", 32, "bold"))
        
        self.login_btn = tk.Button(self, image=self.button_img, text="Login", font=("Inter", 12, "bold"), fg="#2f4f12",
                                  compound="center", bd=0, bg="white", activebackground="white",
                                  command=lambda: self.controller.show_frame("LoginPage"))
        
        self.register_btn = tk.Button(self, image=self.button_img, text="Register", font=("Inter", 12, "bold"), fg="#2f4f12",
                                     compound="center", bd=0, bg="white", activebackground="white",
                                     command=lambda: self.controller.show_frame("RegisterPage"))
        
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
        welcome_y = height * 0.45
        self.canvas.coords(self.welcome_text, center_x, welcome_y)
        
        title_y = height * 0.53
        self.canvas.coords(self.title_text, center_x, title_y)
        
        button_y = height - 70
        button_margin = max(80, width * 0.08)
        
        self.login_btn.place(x=button_margin, y=button_y, width=200, height=50)
        self.register_btn.place(x=width - button_margin - 200, y=button_y, width=200, height=50)