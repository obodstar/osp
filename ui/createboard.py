import customtkinter as ctk
import asynctkinter as at
import re

from . import BaseFrameWidget
from requests.exceptions import HTTPError
from CTkMessagebox import CTkMessagebox

class Widget(BaseFrameWidget):
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

        self.entry_name = ctk.StringVar()
        self.entry_description = ctk.StringVar()
        self.entry_privacy = ctk.StringVar(value="Publik (public)")
        self.entry_category = ctk.StringVar(value="Lainnya (other)")

        wrapper = ctk.CTkScrollableFrame(self, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="nsew", padx=50)

        ctk.CTkLabel(wrapper, text="Nama Papan").pack()
        ctk.CTkEntry(wrapper, textvariable=self.entry_name, fg_color="gray15", height=40) \
            .pack(fill="x", pady=10)
    
        ctk.CTkLabel(wrapper, text="Privasi").pack()
        ctk.CTkOptionMenu(wrapper, values=self.request.board_privacy, variable=self.entry_privacy, height=40) \
            .pack(fill="x", pady=10)

        ctk.CTkLabel(wrapper, text="Kategory").pack()
        ctk.CTkOptionMenu(wrapper, values=self.request.board_category, variable=self.entry_category, height=40) \
            .pack(fill="x", pady=10)

        ctk.CTkLabel(wrapper, text="Deskripsi").pack()
        description = ctk.CTkTextbox(wrapper, height=120, corner_radius=10, fg_color="gray15", border_width=2)
        description.pack(fill="x", pady=10)
        description.bind("<KeyPress>", lambda x: self.entry_description.set(
            description.get(1.0, ctk.END)
        ))

        self.btn = ctk.CTkButton(wrapper, text="Buat Papan", height=40, corner_radius=50, command=lambda: at.start(self._create()))
        self.btn.pack(pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Normal", 15), wraplength=280, justify="center")
        self.error_label.grid(row=1, column=0, pady=(5, 20), sticky="nsew")

    async def _create(self):
        self.error_label.configure(text="")
        name = self.entry_name.get().strip()
        description = self.entry_description.get().strip()
        privacy = self._get_option_value(self.entry_privacy)
        category = self._get_option_value(self.entry_category)
        if not name:
            self.error_label.configure(text="Nama wajib diisi")
            return
        try:
            self.btn.configure(state="disabled", text="Membuat Pin...")
            await at.run_in_thread(lambda: self.request.createBoard(
                name=name, description=description, privacy=privacy, category=category
            ), after=self.after)
            CTkMessagebox(master=self, title="Berhasil", message="Papan Berhasil dibuat!").wait_window()
        except HTTPError as err:
            self.error_label.configure(text=self._get_error_msg_from_http_error(err))
        except Exception as err:
            self.error_label.configure(text=str(err))
        finally:
            self.btn.configure(state="normal", text="Buat Pin")

    def _get_error_msg_from_http_error(self, err: HTTPError) -> str:
        try:
            return err.response.json()["resource_response"]["error"]["message"]
        except:
            return str(err)

    def _get_option_value(self, variable: ctk.StringVar):
        return re.search(r"\((.*?)\)", variable.get().strip()).group(1)
        
