import os
import asynctkinter as at
import customtkinter as ctk
import tkinter.filedialog as filedialog

from . import (progressbar, BaseFrameWidget)
from requests.exceptions import (ConnectionError, HTTPError)

from typing import Callable
from watchpoints import watch
from functools import partial
from CTkListbox import CTkListbox

class Result(BaseFrameWidget):
    def __init__(
        self,
        root,
        fg_color: str = "transparent",
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 3), weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.result_lists = []
        self.rows = dict()

        watch(self.result_lists, callback=self._cb_results_change)

        self.progress_bar = progressbar.Widget(self)

        label = ctk.CTkFrame(self, fg_color="gray15", corner_radius=0)
        label.grid_columnconfigure((0, 1, 2, 3), weight=1)
        label.grid_rowconfigure(0, weight=1)
        label.grid(row=1, column=0, padx=(13, 25), sticky="we")

        ctk.CTkLabel(label, text="STATUS", font=("Normal", 15, "bold")).grid(row=0, column=0, sticky="we")
        ctk.CTkLabel(label, text="ID", font=("Normal", 15, "bold")).grid(row=0, column=1, sticky="we")
        ctk.CTkLabel(label, text="FOTO", font=("Normal", 15, "bold")).grid(row=0, column=2, sticky="we")
        ctk.CTkLabel(label, text="ERROR", font=("Normal", 15, "bold")).grid(row=0, column=3, sticky="we")

        self.result_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", label_fg_color="transparent", label_text="Berhasil (0) - Gagal (0)", label_font=("Courier", 17), corner_radius=0)
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid(row=2, column=0, pady=(10, 0), sticky="nsew")

        self.btn = ctk.CTkButton(self, text="Reset Hasil", corner_radius=50, command=self.reset)
        self.btn.grid(row=3, column=0, pady=(10, 5))

    def reset(self) -> None:
        self.result_lists = []

    def update(self, status: bool, file: str, id: str|None = None, error_msg: str|None = None) -> None:
        self.result_lists.append(dict([
            ("status", status),
            ("file", file),
            ("id", (id or "-")),
            ("error_msg", (error_msg or "-")),
        ]))

    def update_progress(self, value: int) -> None:
        self.progress_bar.update(value)

    def set_visibility_progress(self, visibility: bool):
        if visibility:
            self.progress_bar.grid(row=0, column=0, pady=10, padx=(13, 25), sticky="we")
        else:
            self.progress_bar.pack_forget()

    def get_values(self) -> list:
        return self.result_lists

    def _cb_results_change(self, *args):
        success = len(list(filter(lambda x: x["status"], self.result_lists)))
        failed = len(self.result_lists) - success
        self.result_frame.configure(label_text="Berhasil (%s) - Gagal (%s)"%(success, failed))

        row_keys = list(self.rows.keys())
        is_result_exists = len(self.result_lists)
        self.btn.configure(state="normal" if is_result_exists else "disabled")

        if not is_result_exists:
            for key in row_keys: self.rows[key].destroy()
            self.rows = dict()

        for index, item in enumerate(self.result_lists[::-1]):
            bg_color    = ("gray20" if index % 2 == 0 else "gray15")
            text_color  = ("green" if item["status"] else "red")
            status_text = ("berhasil" if item["status"] else "gagal")
            filename = os.path.basename(item["file"])
            if index in row_keys:
                row = self.rows[index].winfo_children()
                row[0].configure(text=status_text)
                row[1].configure(text=item["id"])
                row[2].configure(text=filename)
                row[3].configure(text=item["error_msg"])
            else:
                self.rows[index] = ctk.CTkFrame(self.result_frame, fg_color=bg_color, corner_radius=0)
                self.rows[index].grid_columnconfigure((0, 1, 2), weight=1)
                self.rows[index].grid(row=index, column=0, pady=2, padx=10, sticky="we")
                ctk.CTkLabel(self.rows[index], text=status_text, text_color=text_color, bg_color=bg_color, wraplength=80) \
                    .grid(row=0, column=0, sticky="we", pady=5, padx=5)
                ctk.CTkLabel(self.rows[index], text=item["id"], bg_color=bg_color, wraplength=80) \
                    .grid(row=0, column=1, sticky="we", pady=5, padx=5)
                ctk.CTkLabel(self.rows[index], text=filename, bg_color=bg_color, wraplength=80) \
                    .grid(row=0, column=2, sticky="we", pady=5, padx=5)
                ctk.CTkLabel(self.rows[index], text=item["error_msg"], bg_color=bg_color, text_color="red", wraplength=80) \
                    .grid(row=0, column=3, sticky="we", pady=5, padx=5)

class Image(BaseFrameWidget):
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

        self.rows = dict()
        self.images = dict()

        watch(self.images, callback=self._cb_images_change)

        self.frame = ctk.CTkScrollableFrame(self, label_text="Foto (0)", label_fg_color="transparent", label_font=("Courier", 17), fg_color="gray15", border_color="gray", border_width=2)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.btn = ctk.CTkButton(self, text="Pilih Foto", height=30, corner_radius=50, command=self._open_file_dialog)
        self.btn.grid(row=1, column=0, pady=(10, 5))

    def _open_file_dialog(self):
        self.reset()
        images = list(
            filedialog.askopenfilenames(parent=self, title="Pilih Foto / Vidio", filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.gif"), ("Videos", "*.mp4")
            ])
        )
        self.images = dict((key, value) for key, value in enumerate(images))

    def _cb_images_change(self, *args):
        count = len(self.get_values())
        self.frame.configure(label_text="Foto (%s)"%(count))
        if count == 0:
            self.reset()

        for key, value in list(self.images.items()):
            filename = os.path.basename(value)
            if key in list(self.rows.keys()):
                self.rows[key].configure(text=filename)
            else:
                btn = ctk.CTkButton(self.frame, text=filename, corner_radius=5, fg_color="transparent", command=partial(self.delete_by_key, key))
                btn._text_label.configure(wraplength=200)
                btn.pack(fill="x", pady=5)
                self.rows[key] = btn

    def delete_by_key(self, key: str|int):
        if key in list(self.rows.keys()) and key in list(self.images.keys()):
            self.rows[key].destroy()
            del self.rows[key]
            del self.images[key]

    def reset(self):
        [self.rows[key].destroy() for key in self.rows.keys() if self.rows[key].winfo_exists()]
        self.rows = dict()
        self.images = dict()

    def get_values(self) -> list:
        return list(self.images.items())
    
class Form(BaseFrameWidget):
    def __init__(
        self,
        root,
        fg_color: str = "transparent",
        start_command: Callable = None,
        stop_command: Callable = None ,
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color, **kwargs)
        self.entry_title = ctk.StringVar()
        self.entry_link = ctk.StringVar()
        self.entry_alt_text = ctk.StringVar() 
        self.entry_description = ctk.StringVar() 
        self.entry_board = ctk.StringVar()
        self.entry_delay = ctk.StringVar(value="3")
        self.board_lists = []

        self.start_command = start_command
        self.stop_command = stop_command

        watch(self.board_lists, callback=self._cb_boards_change)

        ctk.CTkLabel(self, text="Delay (detik)").pack()
        ctk.CTkEntry(self, textvariable=self.entry_delay, fg_color="gray15", height=40, corner_radius=10) \
            .pack(fill="x", pady=10)

        ctk.CTkLabel(self, text="Judul").pack()
        ctk.CTkEntry(self, textvariable=self.entry_title, fg_color="gray15", height=40, corner_radius=10) \
            .pack(fill="x", pady=10)

        ctk.CTkLabel(self, text="Link").pack()
        ctk.CTkEntry(self, textvariable=self.entry_link, fg_color="gray15", height=40, corner_radius=10) \
            .pack(fill="x", pady=10)

        ctk.CTkLabel(self, text="Teks Alternatif").pack()
        ctk.CTkEntry(self, textvariable=self.entry_alt_text, fg_color="gray15", height=40, corner_radius=10) \
            .pack(fill="x", pady=10)

        ctk.CTkLabel(self, text="Papan (Board)").pack()
        self.boards = CTkListbox(self, command=lambda v: self.entry_board.set(v), fg_color="gray15", justify="center")
        self.boards.pack(fill="x", pady=10)

        ctk.CTkLabel(self, text="Deskripsi").pack()

        description = ctk.CTkTextbox(self, height=120, corner_radius=10, fg_color="gray15", border_width=2)
        description.pack(fill="x", pady=10)
        description.bind("<KeyPress>", lambda x: self.entry_description.set(
            description.get(1.0, ctk.END)
        ))

        btn_wrapper = ctk.CTkFrame(self, fg_color="transparent", height=30)
        btn_wrapper.grid_columnconfigure((0, 1), weight=1)
        btn_wrapper.pack(fill="x", pady=10)

        self.btn_start = ctk.CTkButton(btn_wrapper, text="Mulai", height=30, corner_radius=10, command=self._start)
        self.btn_start.grid(row=0, column=0, padx=5, sticky="we")

        self.btn_stop = ctk.CTkButton(btn_wrapper, text="Stop", height=30, fg_color="#ab0c2e", state="disabled", hover_color="#8a0a25", corner_radius=10, command=self._stop)
        self.btn_stop.grid(row=0, column=1, padx=5, sticky="we")
    
    def mount(self):
        at.start(self._load_boards())

    def _start(self):
        if self.start_command:
            self.start_command(self.get_values())

    def _stop(self):
        if self.stop_command:
            self.stop_command(self.get_values())

    def _cb_boards_change(self, *args):
        if len(self.boards.buttons.items()) > 0:
            self.boards.delete("all")
        for index, item in enumerate(self.board_lists):
            self.boards.insert(index, item["name"])

    async def _load_boards(self):
        while True:
            try:
                self.board_lists = [] # reset board lists to trigger _cb_boards_change
                self.boards.insert(0, "Memuat Papan, tunggu sebentar...", True, state="disabled")
                self.board_lists = await at.run_in_thread(lambda: self.request.getAllBoards("me"), after=self.after)
                if len(self.board_lists) == 0: raise Exception()
                break
            except ConnectionError:
                continue
            except Exception:
                self.boards.delete(0)
                break

    def _get_board_id_by_name(self, name) -> str|None:
        for item in self.board_lists:
            if item["name"] == name:
                return item["id"]
        return None

    def get_values(self) -> dict:
        return dict(
            [
                ("delay", self.entry_delay.get()),
                ("title", self.entry_title.get()),
                ("link", self.entry_link.get()),
                ("alt_text", self.entry_alt_text.get()),
                ("description", self.entry_description.get()),
                ("board", self._get_board_id_by_name(self.entry_board.get())),
            ]
        )
    
    def reset(self):
        self.entry_delay.set("3")
        self.entry_title.set("")
        self.entry_alt_text.set("")
        self.entry_description.set("")
        self.entry_link.set("")
        self.entry_board.set("")

    def set_disable_btn_start(self, disabled: bool):
        self.btn_start.configure(state="disabled" if disabled else "normal")

    def set_disable_btn_stop(self, disabled: bool):
        self.btn_stop.configure(state="disabled" if disabled else "normal")

class Widget(BaseFrameWidget):
    def __init__(
        self,
        root,
        fg_color: str = "transparent",
        **kwargs
    ):
        super().__init__(master=root, fg_color=fg_color, **kwargs)

        self.is_processing = False
        self.sleep = partial(at.sleep, self.after)

        watch(self.is_processing, callback=self._cb_is_processing_change)

        if self.winfo_toplevel().winfo_screenwidth() < 1000:
            self._init_mobile_view()
        else:
            self._init_desktop_view()

    def _init_desktop_view(self):
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        form_frame_wrapper = ctk.CTkScrollableFrame(self, fg_color="transparent", width=400)
        form_frame_wrapper.grid_columnconfigure(0, weight=1)
        form_frame_wrapper.grid_rowconfigure(0, weight=1)
        form_frame_wrapper.grid(row=0, column=1, sticky="nsew")

        self.image_frame = Image(self)
        self.image_frame.grid(row=0, column=0, padx=10, sticky="nsew")

        self.form_frame = Form(form_frame_wrapper, start_command=lambda values: at.start(self.start(values)), stop_command=self.stop)
        self.form_frame.grid(row=0, column=0, padx=10, sticky="nsew")

        self.result_frame = Result(self)
        self.result_frame.grid(row=0, column=2,  padx=10, sticky="nsew")

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=1, column=1, sticky="we")

    def _init_mobile_view(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        wrapper = ctk.CTkScrollableFrame(self, fg_color="transparent")
        wrapper.grid_rowconfigure((0, 1, 2), weight=1)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid(row=0, column=0, sticky="nsew")

        self.image_frame = Image(wrapper)
        self.image_frame.grid(row=0, column=0, padx=25, sticky="nsew")

        self.form_frame = Form(wrapper, start_command=lambda values: at.start(self.start(values)), stop_command=self.stop)
        self.form_frame.grid(row=1, column=0, padx=25, sticky="nsew")

        self.result_frame = Result(wrapper)
        self.result_frame.grid(row=2, column=0, padx=15, pady=(20, 5), sticky="nsew")

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=1, column=0)

    async def start(self, values):
        self.error_label.configure(text="")
        delay: str = values["delay"]
        images = self.image_frame.get_values()
        if not values["board"]:
            self.error_label.configure(text="Papan (Board) wajib diisi")
            return
        if not delay.isnumeric():
            self.error_label.configure(text="Delay wajib diisi dan harus berupa angka yang benar")
            return
        if len(images) < 1:
            self.error_label.configure(text="Foto wajib diisi")
            return

        self.result_frame.update_progress(0)
        self.result_frame.set_visibility_progress(True)
        delay = (int(values["delay"]) * 1000)
        progress_inter_step = 1 / len(images)
        progress_step = progress_inter_step
        self.is_processing = True

        for id, file in self.image_frame.get_values():
            if not self.is_processing:
                break
            if not os.path.isfile(file):
                self.result_frame.update(status=False, file=file, error_msg="File tidak valid")
            else:
                response, error_msg = [None, None]
                while True:
                    if not self.is_processing:
                        break
        
                    kwargs = dict(
                        [
                            ("imageFile", file),
                            ("boardId", values["board"]),
                            ("title", values["title"]),
                            ("link", values["link"]),
                            ("description", values["description"]),
                            ("altText", values["alt_text"]),
                        ]
                    )

                    try:
                        response = await at.run_in_thread(lambda: self.request.uploadPin(**kwargs), after=self.after)
                        break
                    except ConnectionError:
                        continue
                    except HTTPError as err:
                        error_msg = self._get_error_msg_from_http_error(err)
                        break
                    except Exception as e:
                        error_msg = str(e)
                        break
                if isinstance(response, dict) and error_msg is None:
                    self.result_frame.update(status=True, file=file, id=response["id"])
                else:
                    self.result_frame.update(status=False, file=file, error_msg=error_msg)

            self.result_frame.update_progress(progress_step)
            progress_step += progress_inter_step
            self.image_frame.delete_by_key(id)
            await at.sleep(duration=delay, after=self.after)

        self.is_processing = False

    def stop(self, values):
        self.is_processing = False

    def reset(self):
        self.is_processing = False
        self.result_frame.reset()
        self.image_frame.reset()
        self.form_frame.reset()

    def _cb_is_processing_change(self, *args):
        self.form_frame.set_disable_btn_start(self.is_processing == True)
        self.form_frame.set_disable_btn_stop(self.is_processing == False)

    def _sleep(self, value: int):
        return at.sleep(duration=value, after=self.after)

    def _get_error_msg_from_http_error(self, err: HTTPError) -> str:
        try:
            return err.response.json()["resource_response"]["error"]["message_detail"]
        except:
            return str(err)