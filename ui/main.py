import customtkinter as ctk
from . import (
    createpin,
    createboard,
    profile,
    BaseFrameWidget
)

class Widget(BaseFrameWidget):
    def __init__(
        self,
        root,
        fg_color = "transparent",
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color, **kwargs)

        self.createpin_widget = createpin.Widget(self)
        self.createboard_widget = createboard.Widget(self)
        self.profile_widget = profile.Widget(self)

        self.controller.add(
            id="Buat Pin",
            call="pack",
            frame=self.createpin_widget,
            expand=True,
            fill="both",
            pady=20,
            padx=10
        )
        self.controller.add(
            id="Buat Papan (Board)",
            call="pack",
            frame=self.createboard_widget,
            expand=True,
            fill="both",
            pady=20,
            padx=25
        )
        self.controller.add(
            id="Profile",
            call="pack",
            frame=self.profile_widget,
            expand=True,
            fill="both",
            pady=20,
            padx=25
        )

        self.segment_btn = ctk.CTkSegmentedButton(self, values=["Buat Pin", "Buat Papan (Board)", "Profile"], height=40, corner_radius=50, command=self._btn_segment_change)
        self.segment_btn.pack(fill="x", pady=10, padx=10)
        self.segment_btn.set("Buat Pin", from_button_callback=True)

    def unmount(self):
        self.createpin_widget.reset()

    def _btn_segment_change(self, segment: str):
        self.controller.go(segment)