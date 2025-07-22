import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class InputPage(tk.Frame):
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
        
        self.input_label = tk.Label(self, text="Mau masukkan berapa botol?", font=("Inter", 14, "bold"), bg="white", fg="#2f4f12")

        vcmd = (self.register(self.validate_numbers), "%P")
        self.input_entry = tk.Entry(
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
        
        self.sensor_frame = tk.LabelFrame(self, text="Sensor Data (0=present, 1=not present)", 
                                         font=("Inter", 12, "bold"), bg="white", fg="#2f4f12")
        
        self.sensor1_label = tk.Label(self.sensor_frame, text="Sensor 1:", font=("Inter", 12), bg="white", fg="#2f4f12")
        self.sensor1_var = tk.StringVar(value="0")
        self.sensor1_frame = tk.Frame(self.sensor_frame, bg="white")
        self.sensor1_radio0 = tk.Radiobutton(self.sensor1_frame, text="0 (Present)", variable=self.sensor1_var, 
                                           value="0", bg="white", fg="#2f4f12", font=("Inter", 10))
        self.sensor1_radio1 = tk.Radiobutton(self.sensor1_frame, text="1 (Not Present)", variable=self.sensor1_var, 
                                           value="1", bg="white", fg="#2f4f12", font=("Inter", 10))
        
        self.sensor2_label = tk.Label(self.sensor_frame, text="Sensor 2:", font=("Inter", 12), bg="white", fg="#2f4f12")
        self.sensor2_var = tk.StringVar(value="0")
        self.sensor2_frame = tk.Frame(self.sensor_frame, bg="white")
        self.sensor2_radio0 = tk.Radiobutton(self.sensor2_frame, text="0 (Present)", variable=self.sensor2_var, 
                                           value="0", bg="white", fg="#2f4f12", font=("Inter", 10))
        self.sensor2_radio1 = tk.Radiobutton(self.sensor2_frame, text="1 (Not Present)", variable=self.sensor2_var, 
                                           value="1", bg="white", fg="#2f4f12", font=("Inter", 10))
        
        self.sensor3_label = tk.Label(self.sensor_frame, text="Sensor 3:", font=("Inter", 12), bg="white", fg="#2f4f12")
        self.sensor3_var = tk.StringVar(value="0")
        self.sensor3_frame = tk.Frame(self.sensor_frame, bg="white")
        self.sensor3_radio0 = tk.Radiobutton(self.sensor3_frame, text="0 (Present)", variable=self.sensor3_var, 
                                           value="0", bg="white", fg="#2f4f12", font=("Inter", 10))
        self.sensor3_radio1 = tk.Radiobutton(self.sensor3_frame, text="1 (Not Present)", variable=self.sensor3_var, 
                                           value="1", bg="white", fg="#2f4f12", font=("Inter", 10))
        
        self.sensor1_radio0.pack(side=tk.LEFT, padx=5)
        self.sensor1_radio1.pack(side=tk.LEFT, padx=5)
        self.sensor2_radio0.pack(side=tk.LEFT, padx=5)
        self.sensor2_radio1.pack(side=tk.LEFT, padx=5)
        self.sensor3_radio0.pack(side=tk.LEFT, padx=5)
        self.sensor3_radio1.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = tk.Button(self, image=self.button_img, text="Cancel", font=("Inter", 12, "bold"), fg="#2f4f12",
                                   compound="center", bd=0, bg="white", activebackground="white",
                                   command=lambda: self.controller.show_frame("StartPage"))
        
        self.submit_btn = tk.Button(self, image=self.button_img, text="Submit", font=("Inter", 12, "bold"), fg="#2f4f12",
                                   compound="center", bd=0, bg="white", activebackground="white",
                                   command=self.submit_bottles)
        
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
        
        form_width = min(500, width * 0.7)
        form_x = (width - form_width) // 2
        
        label_y = height * 0.25
        entry_y = height * 0.3
        
        self.input_label.place(x=form_x + 10, y=label_y)
        self.input_entry.place(x=form_x, y=entry_y, width=form_width, height=40)
        
        sensor_y = height * 0.4
        sensor_height = 150
        self.sensor_frame.place(x=form_x, y=sensor_y, width=form_width, height=sensor_height)
        
        self.sensor1_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.sensor1_frame.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        self.sensor2_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.sensor2_frame.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        self.sensor3_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.sensor3_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        button_y = height - 70
        button_margin = max(80, width * 0.08)
        
        self.cancel_btn.place(x=button_margin, y=button_y, width=200, height=50)
        self.submit_btn.place(x=width - button_margin - 200, y=button_y, width=200, height=50)

    def reset_form(self):
        self.input_entry.delete(0, tk.END)
        self.sensor1_var.set("0")
        self.sensor2_var.set("0")
        self.sensor3_var.set("0")

    def submit_bottles(self):
        bottle_count = self.input_entry.get().strip()
        
        if not bottle_count:
            messagebox.showerror("Error", "Please enter the number of bottles")
            return
        
        try:
            bottles = int(bottle_count)
            if bottles <= 0:
                messagebox.showerror("Error", "Please enter a positive number")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return
        
        if not self.controller.current_user_nim:
            messagebox.showerror("Error", "No user logged in")
            return
        
        sensor1 = int(self.sensor1_var.get())
        sensor2 = int(self.sensor2_var.get())
        sensor3 = int(self.sensor3_var.get())
        
        success, message = self.controller.db.add_bottles(
            self.controller.current_user_nim, 
            bottles, 
            sensor1, 
            sensor2, 
            sensor3
        )
        
        if success:
            self.controller.current_bottles += bottles
            result = messagebox.askyesno("Success", 
                f"Added {bottles} bottles successfully!\nSensor data: S1={sensor1}, S2={sensor2}, S3={sensor3}\n\nDo you want to add more bottles?")
            
            if result:  
                self.reset_form()
            else:  
                self.reset_form()
                self.controller.show_frame("EndPage")
        else:
            messagebox.showerror("Error", message)

    def validate_numbers(self, text):
        return text.isdigit() or text == ""