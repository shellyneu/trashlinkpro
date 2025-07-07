import tkinter as tk
from screen.start_page import StartPage
from screen.login import LoginPage
from screen.register import RegisterPage
from screen.input_botol import InputPage
from screen.loop import LoopPage
from screen.end_page import EndPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x600")
        self.configure(bg="white")
        self.title("Trashlink Pro")

        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

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
