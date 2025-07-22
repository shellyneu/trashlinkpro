import tkinter as tk
from screen.start_page import StartPage
from screen.login import LoginPage
from screen.register import RegisterPage
from screen.input_botol import InputPage
from screen.loop import LoopPage
from screen.end_page import EndPage
from database.neon_db import NeonDatabase

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("1024x600")
        self.minsize(800, 480) 
        self.configure(bg="white")
        self.title("Trashlink Pro")
        
        self.resizable(True, True)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize Neon database
        self.db = NeonDatabase()
        
        # Initialize database tables
        self.db.init_database()
        
        # Current user tracking
        self.current_user_nim = None
        self.current_user_name = None
        self.current_bottles = 0

        self.container = tk.Frame(self, bg="white")
        self.container.grid(row=0, column=0, sticky="nsew")
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LoginPage, RegisterPage, InputPage, LoopPage, EndPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        if hasattr(frame, 'reset_form'):
            frame.reset_form()
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()