import customtkinter as ctk
import asynctkinter as at
from PIL import Image
from io import BytesIO

from requests.exceptions import ConnectionError
from . import (
    loading,
    BaseFrameWidget,
    PageController
)

class Layout(BaseFrameWidget):
    def __init__(
        self,
        root,
        fg_color: str = "transparent",
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")

        self.logout_btn = ctk.CTkButton(self, text="Keluar", corner_radius=50, anchor="c", width=350, command=lambda: at.start(self._logout()))
        self.logout_btn.grid(row=1, column=0)

        self.profile_cover = ctk.CTkLabel(frame, text="")
        self.profile_cover.pack(pady=(20, 5))

        self.label_name = ctk.CTkLabel(frame, text="", wraplength=400, font=("Courier", 40, "bold"))
        self.label_name.pack(pady=10)

        ctk.CTkLabel(frame, text="NAMA PENGGUNA", text_color="green", font=("Normal", 15, "bold")) \
            .pack(pady=(10, 0))
        self.label_username = ctk.CTkLabel(frame, text="-", font=("Normal", 14, "bold"))
        self.label_username.pack(pady=(0, 5))

        ctk.CTkLabel(frame, text="ID", text_color="green", font=("Normal", 15, "bold")) \
            .pack(pady=(10, 0))
        
        self.label_id = ctk.CTkLabel(frame, text="-", font=("Normal", 14, "bold"))
        self.label_id.pack(pady=(0, 5))

        ctk.CTkLabel(frame, text="STORY PIN", text_color="green", font=("Normal", 15, "bold")) \
            .pack(pady=(10, 0))
        
        self.label_story_pin = ctk.CTkLabel(frame, text="0", font=("Normal", 14, "bold"))
        self.label_story_pin.pack(pady=(0, 5))

        ctk.CTkLabel(frame, text="VIDIO PIN", text_color="green", font=("Normal", 15, "bold")) \
            .pack(pady=(10, 0))

        self.label_video_pin = ctk.CTkLabel(frame, text="0", font=("Normal", 14, "bold"))
        self.label_video_pin.pack(pady=(0, 5))

        ctk.CTkLabel(frame, text="PAPAN (BOARD)", text_color="green", font=("Normal", 15, "bold")) \
            .pack(pady=(10, 0))

        self.label_board = ctk.CTkLabel(frame, text="0", font=("Normal", 14, "bold"))
        self.label_board.pack(pady=(0, 5))

    async def _logout(self):
        self.logout_btn.configure(state="disabled", text="Sedang Keluar...")
        while True:
            try:
                await at.run_in_thread(lambda: self.request.logout(), after=self.after)
                break
            except ConnectionError:
                continue
            except Exception:
                break
            finally:
                self.logout_btn.configure(state="normal", text="Keluar")
                self.event.emit("logout")
                break

class Widget(BaseFrameWidget):
    def __init__(
        self,
        root,
        fg_color: str = "transparent",
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_widget = Layout(self)
        self.loading_widget = loading.Widget(self, text="Memuat Data...", width=300)

        self.controller = PageController()
        self.controller.add(
            id="loading",
            call="grid",
            frame=self.loading_widget,
            row=0,
            column=0,
            sticky="nsew"
        )
        self.controller.add(
            id="main",
            call="grid",
            frame=self.main_widget,
            row=0,
            column=0,
            sticky="nsew"
        )

    def mount(self):
        at.start(self._load_profile())

    async def _load_profile(self):
        self.controller.go("loading")
        self.loading_widget.update_label("Memuat Data...")

        user = await self._get_user()
        if not user:
            self.loading_widget.update_label("Ups!... Gagal Memuat Data :(")
            await at.sleep(after=self.after, duration=3000)
        else:
            image = await self._get_user_image(user["image_medium_url"])

            if image:
                self.main_widget.profile_cover.configure(image=ctk.CTkImage(
                    Image.open(BytesIO(image)),
                    size=(180, 180)
                ))

            self.main_widget.label_id.configure(text=user["id"])
            self.main_widget.label_username.configure(text=user["username"])
            self.main_widget.label_name.configure(text=user["full_name"])
            self.main_widget.label_story_pin.configure(text=user["story_pin_count"])
            self.main_widget.label_video_pin.configure(text=user["video_pin_count"])
            self.main_widget.label_board.configure(text=user["board_count"])

        self.controller.go("main")
    
    async def _get_user(self):
        while True:
            try:
                return await at.run_in_thread(lambda: self.request.getUserOverview("me"), after=self.after)
            except ConnectionError:
                continue
            except:
                return None

    async def _get_user_image(self, image_url: str):
        while True:
            try:
                return await at.run_in_thread(lambda: self.request.get(image_url, stream=True).content, after=self.after)
            except ConnectionError:
                continue
            except:
                return None