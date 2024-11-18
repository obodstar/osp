import customtkinter as ctk
import asynctkinter as at

from CTkMessagebox import CTkMessagebox
from pin.requests import Requests
from ui import (
    login,
    loading,
    main,
    BaseFrameWidget
)
from requests.exceptions import (
    ConnectionError
)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        if screen_width < 1000:
            sizes = (screen_width, screen_height)
            self.minsize(screen_width, screen_height)
        else:
            sizes = (1100, 620)
            self.minsize(720, 600)

        padx = int((screen_width / 2) - (sizes[0] / 2))
        pady = int((screen_height / 2) - (sizes[1] / 2))

        self.request = Requests()
        self.user_overview = dict()
        self.geometry(f"{sizes[0]}x{sizes[1]}+{padx}+{pady}")
        self.title("Pinterest Auto Posting")

        self.root = BaseFrameWidget(master=self, fg_color="transparent")
        self.root.pack(expand=True, fill="both", pady=20, padx=20)

        self.root.event.on("login", self.on_login_event)
        self.root.event.on("logout", self.on_logout_event)

        self.loading_widget = loading.Widget(self.root, text="Loading....")
        self.login_widget   = login.Widget(self.root, fg_color="#383b3b", corner_radius=20)
        self.main_widget    = main.Widget(self.root, fg_color="#383b3b", corner_radius=20)

        self.root.controller.add(
            id="loading",
            call="pack",
            frame=self.loading_widget,
            expand=True,
            fill="both"
        )
        self.root.controller.add(
            id="login",
            call="pack",
            frame=self.login_widget,
            expand=True,
            fill="both"
        )
        self.root.controller.add(
            id="main",
            call="pack",
            frame=self.main_widget,
            expand=True,
            fill="both"
        )

        at.start(self.check_login())

    async def check_login(self):
        if self.request.isAuth():
            self.root.controller.go("loading")
            self.user_overview = await self.load_user()
        if self.user_overview:
            self.root.controller.go("main")
        else:
            self.root.controller.go("login")

    def on_login_event(self, event):
        CTkMessagebox(self, title="Login Berhasil", message="Hai.. %s selamat datang :)"%(event["name"]), icon="check", option_1="OK").wait_window()
        self.root.controller.go("main")

    def on_logout_event(self, *event):
        self.root.controller.go("login")

    async def load_user(self):
         while True:
            try:
                return await at.run_in_thread(lambda: self.request.getUserOverview("me"), after=self.after)
            except ConnectionError:
                None
            except:
                return None

if __name__ == "__main__":
    try:
        App().mainloop()
    except KeyboardInterrupt:
        pass