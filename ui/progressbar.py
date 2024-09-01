import customtkinter as ctk
from . import BaseFrameWidget

class Widget(BaseFrameWidget):
    def __init__(
        self,
        master,
        text: str ="",
        fg_color: str = "transparent",
        **kwargs
    ):
        super().__init__(master=master, fg_color=fg_color)
        self.text = text
        self.label = ctk.CTkLabel(self, text=text, anchor="center", font=("Arial", 18))
        self.label.pack(fill="x", pady=(0, 15))
        self.progress = ctk.CTkProgressBar(self, **kwargs)
        self.progress.set(0)
        self.progress.pack(fill="x")

    def update(self, value: int):
        self.progress.set(value)
        self.progress.update()
        self.label.configure(text="{0} {1}%".format(self.text, round(self.progress.get() * 100, 1)).strip())
