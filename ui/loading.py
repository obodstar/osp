import customtkinter as ctk
from . import (progressbar, BaseFrameWidget)

class Widget(BaseFrameWidget):
    def __init__(
        self,
        root,
        text: str,
        fg_color: str = "transparent",
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.progress = progressbar.Widget(self, text=text, mode="indeterminate", **kwargs)
        self.progress.grid(row=0, column=0)

        self.bind("<Map>", command=lambda e: self.progress.progress.start())
        self.bind("<Unmap>", command=lambda e: self.progress.progress.stop())

    def update_label(self, text: str):
        self.progress.label.configure(text=text)