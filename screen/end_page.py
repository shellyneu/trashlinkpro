import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from utils.printer import receipt_printer

class EndPage(tk.Frame):
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
        
        self.points_text = self.canvas.create_text(0, 0, text="Poinmu = 0", fill="#2f4f12", font=("Inter", 28, "bold"))
        self.question_text = self.canvas.create_text(0, 0, text="Cetak voucher?", fill="#2f4f12", font=("Inter", 32, "bold"))

        self.close_btn = tk.Button(self, image=self.button_img, text="Tidak", font=("Inter", 12, "bold"), fg="#2f4f12",
                                  compound="center", bd=0, bg="white", activebackground="white",
                                  command=self.logout_user)
        
        self.print_btn = tk.Button(self, image=self.button_img, text="Cetak", font=("Inter", 12, "bold"), fg="#2f4f12",
                                  compound="center", bd=0, bg="white", activebackground="white",
                                  command=self.print_voucher)
        
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
        points_y = height * 0.45
        question_y = height * 0.53
        
        self.canvas.coords(self.points_text, center_x, points_y)
        self.canvas.coords(self.question_text, center_x, question_y)
        
        button_y = height - 70
        button_margin = max(80, width * 0.08)
        
        self.close_btn.place(x=button_margin, y=button_y, width=200, height=50)
        self.print_btn.place(x=width - button_margin - 200, y=button_y, width=200, height=50)

    def update_display(self):
        if self.controller.current_user_nim:
            total_bottles = self.controller.db.get_user_bottles(self.controller.current_user_nim)
            points = total_bottles * 10  
            self.canvas.itemconfig(self.points_text, text=f"Poinmu = {points}")

    def print_voucher(self):
        """Print the voucher receipt with user points and information"""
        if not self.controller.current_user_nim:
            messagebox.showerror("Error", "No user logged in")
            return
        
        try:
            # Get user information
            user_nim = self.controller.current_user_nim
            user_name = self.controller.current_user_name
            
            # Get total bottles and calculate points
            total_bottles = self.controller.db.get_user_bottles(user_nim)
            points = total_bottles * 10
            
            # Show confirmation dialog
            result = messagebox.askyesno(
                "Confirm Print", 
                f"Print voucher for {user_name}?\n\n"
                f"NIM: {user_nim}\n"
                f"Total Bottles: {total_bottles}\n"
                f"Points: {points}\n\n"
                f"Make sure printer is connected and has paper."
            )
            
            if not result:
                return
            
            # Print the receipt
            success, message = receipt_printer.print_receipt(
                user_name=user_name,
                user_nim=user_nim, 
                points=points,
                total_bottles=total_bottles
            )
            
            if success:
                messagebox.showinfo("Success", message)
                # After successful print, logout user
                self.logout_user()
            else:
                messagebox.showerror("Print Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print voucher: {str(e)}")

    def logout_user(self):
        self.controller.current_user_nim = None
        self.controller.current_user_name = None
        self.controller.current_bottles = 0
        self.controller.show_frame("StartPage")

    def reset_form(self):
        self.update_display()