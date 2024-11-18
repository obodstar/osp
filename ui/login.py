import tkinter.filedialog as filedialog
import customtkinter as ctk
import asynctkinter as at
import base64
import csv

from requests.exceptions import HTTPError
from pin.utils import Utils
from . import BaseFrameWidget

class Cookie(BaseFrameWidget):
    def __init__(
        self,
        root,
        fg_color = "transparent",
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.entry_cookie = ctk.StringVar()

        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="we")

        ctk.CTkLabel(wrapper, text="Masuk dengan cookie Pinterst kamu !!", font=("Courier", 20), wraplength=380) \
            .pack(pady=10)
        
        ctk.CTkButton(wrapper, text="Muat Dari File .csv", fg_color="gray30", hover_color="gray25", corner_radius=20, command=self._load_from_csv) \
            .pack(pady=20)

        ctk.CTkLabel(wrapper, text="Cookie") \
            .pack(fill="x")
        ctk.CTkEntry(wrapper, textvariable=self.entry_cookie, placeholder_text="Cookie", height=40, corner_radius=50) \
            .pack(fill="x", pady=10)
        
        self.btn = ctk.CTkButton(wrapper, text="Masuk", height=40, corner_radius=50, command=lambda: at.start(self._login()))
        self.btn.pack(pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Normal", 15), wraplength=280, justify="center")
        self.error_label.grid(row=1, column=0, pady=(5, 20), sticky="nsew")

    async def _login(self):
        self.error_label.configure(text="")
        values = self.get_values()

        if not values["cookie"].strip():
            self.error_label.configure(text="Cookie wajib diisi")
            return

        try:
            self.btn.configure(state="disabled", text="Sedang Masuk...")
            cookies = Utils.cookie_string_to_dict(values["cookie"])
            self.request.cookies.clear()
            self.request.cookies.update(cookies)
            response = await at.run_in_thread(lambda: self.request.getUserOverview("me"), after=self.after)
            self.request.writeSession(cookies)
            event_args = dict([
                ("cookies", cookies),
                ("name", response["full_name"]),
                ("id", response["id"]),
                ("image", response["image_xlarge_url"])
            ])
            self.event.emit("login", event_args)
        except HTTPError as err:
            code = err.response.status_code
            self.error_label.configure(text="Cookie salah atau tidak valid" if code == 404 else "Gagal masuk coba lagi. code(%s)"%(code))
        except Exception as err:
            self.error_label.configure(text=str(err))
        finally:
            self.btn.configure(state="normal", text="Masuk")

    def _load_from_csv(self):
        file = filedialog.askopenfilename(parent=self, title="Cookie CSV", filetypes=[
            ("CSV Files", "*.csv")
        ])

        cookies = Utils.load_cookie_from_csv(file)

        if not cookies:
            self.error_label.configure(text="File cookie tidak valid. pastikan memiliki header (Name, Value)")
        else:
            self.entry_cookie.set(Utils.cookie_dict_to_string(cookies))
            at.start(self._login())

    def get_values(self) -> dict:
        return dict([
            ("cookie", self.entry_cookie.get())
        ])

class Credential(BaseFrameWidget):
    def __init__(
        self,
        root,
        fg_color = "transparent",
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.entry_email = ctk.StringVar()
        self.entry_password = ctk.StringVar()

        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="we")

        ctk.CTkLabel(wrapper, text="Masuk dengan akun Pinterst kamu !!", font=("Courier", 20), wraplength=380) \
            .pack(pady=10)

        ctk.CTkLabel(wrapper, text="Email") \
            .pack(fill="x")
        ctk.CTkEntry(wrapper, textvariable=self.entry_email, height=40, corner_radius=50) \
            .pack(fill="x", pady=10)

        ctk.CTkLabel(wrapper, text="Kata Sandi") \
            .pack(fill="x")
        ctk.CTkEntry(wrapper, textvariable=self.entry_password, height=40, corner_radius=50) \
            .pack(fill="x", pady=10)
        
        self.btn = ctk.CTkButton(wrapper, text="Masuk", height=40, corner_radius=50, command=lambda: at.start(self._login()))
        self.btn.pack(pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Normal", 15), wraplength=280, justify="center")
        self.error_label.grid(row=1, column=0, pady=(5, 20), sticky="nsew")

    async def _login(self):
        self.error_label.configure(text="")
        values = self.get_values()
        email: str = values["email"]
        password: str = values["password"]

        if not email.strip():
            self.error_label.configure(text="Email wajib diisi")
            return
        
        if not password.strip():
            self.error_label.configure(text="Kata sandi wajib diisi")
            return

        try:
            self.btn.configure(state="disabled", text="Sedang Masuk...")
            response = await at.run_in_thread(lambda: self.request.createSession(email, password), after=self.after)
            self.request.writeSession(response["cookies"])
            event_args = dict([
                ("cookies", response["cookies"]),
                ("name", response["user"]["full_name"]),
                ("id", base64.b64decode(response["user"]["node_id"]).decode().split(":")[1]),
                ("image", response["user"]["image_large_url"])
            ])
            self.event.emit("login", event_args)
        except HTTPError as err:
            code = err.response.status_code
            self.error_label.configure(text="Email atau Kata sandi salah" if code == 401 else "Gagal masuk coba lagi. code(%s)"%(code))
        except Exception as err:
            self.error_label.configure(text=str(err))
        finally:
            self.btn.configure(state="normal", text="Masuk")

    def get_values(self) -> dict:
        return dict([
            ("email", self.entry_email.get()),
            ("password", self.entry_password.get())
        ])

class Widget(BaseFrameWidget):
    def __init__(
        self,
        root,
        fg_color = "transparent",
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.credential_widget = Credential(self)
        self.cookie_widget = Cookie(self)

        self.controller.add(
            id="Login Dengan Kredensial",
            call="grid",
            frame=self.credential_widget,
            row=1,
            column=0,
            sticky="nsew",
            pady=20,
            padx=200
        )
        self.controller.add(
            id="Login Dengan Cookie",
            call="grid",
            frame=self.cookie_widget,
            row=1,
            column=0,
            sticky="nsew",
            pady=20,
            padx=200
        )

        option = ctk.CTkSegmentedButton(self, values=["Login Dengan Kredensial", "Login Dengan Cookie"], height=40, corner_radius=50, command=self._change_option)
        option.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
        option.set("Login Dengan Kredensial", from_button_callback=True)

    def _change_option(self, name):
        self.controller.go(name)