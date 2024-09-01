import customtkinter as ctk
from pin.requests import Requests

_callbacks = dict()

class Event():

    @staticmethod
    def on(event_name, f):
        _callbacks[event_name] = _callbacks.get(event_name, []) + [f]
        return f

    @staticmethod
    def emit(event_name, *data):
        [f(*data) for f in _callbacks.get(event_name, [])]

    @staticmethod
    def off(event_name, f):
        _callbacks.get(event_name, []).remove(f)

class PageController:
    def __init__(self):
        self.pages = dict()

    def add(self, id: str, call: str, frame, **kwargs):
        self.pages[id] = dict(
            [
                ("frame", frame),
                ("call", call),
                ("kwargs", kwargs)
            ]
        )

    def go(self, id: str):
        self.hide_all()
        self.show(id)

    def show(self, id: str):
        args = self.get(id)
        getattr(args["frame"], args["call"])(**args["kwargs"])

    def hide(self, id: str):
        args = self.get(id)
        getattr(args["frame"], "%s_forget"%(args["call"]))()

    def hide_all(self):
        for id in list(self.pages.keys()):
            self.hide(id)
    
    def get(self, id: str):
        return self.pages[id]

class BaseFrameWidget(ctk.CTkFrame):
    event: Event = Event
    controller: PageController

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request = Requests()
        self.controller = PageController()

        self.bind("<Map>", command=self._cb_map)
        self.bind("<Unmap>", command=self._cb_unmap)

    def _cb_map(self, event):
        self.request.init()
        if hasattr(self, "mount") and callable(self.mount):
            self.mount()

    def _cb_unmap(self, event):
        if hasattr(self, "unmount") and callable(self.unmount):
            self.unmount()
