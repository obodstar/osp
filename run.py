import os
import re
import time
from time import sleep
from pin.requests import Requests
from pin.utils import Utils
from colorama import Fore, Back, Style
from requests.exceptions import (ConnectionError, HTTPError)
from rich.console import Console
from rich.table import Table
import random
import hashlib
import string
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from rich.panel import Panel

#######################################################
# Name           : OSP (Obod Star Pinterest)          #
# File           : cli.py                             #
# Author         : Obod Star                          #
# Website        : https://obodstar.com/              #
# Github         : https://github.com/obodstar        #   
# Python version : 3.0                                #
#######################################################

class Pinterest:
    user_overview: dict
    request: Requests
    
    # coding baru obdstar
    def download_foto(self):
        # Nonaktifkan timestamp di log
        print("fitur belum dibuat🙏")
    def __init__(self):
        self.user_overview = dict()
        self.request = Requests()
        self.screen()
        self.init()

    def init(self):
        if self.request.isAuth() and self.check_login():
            self.main()
        else:
            self.login()

    def screen(self):
        os.system("cls" if os.name == "nt" else "clear")
        # print(f"      {Back.RED} OSP {Style.RESET_ALL}        ")
        # print(f"        {Back.BLUE} Created By Obod {Style.RESET_ALL}         ")
        # print(f"            {Back.WHITE} Version : 3.0 {Style.RESET_ALL}            ")
        # print()
        # print("+-------------------------------------+")

    
        # text dan color
        green = "\033[38;2;23;255;46m"
        bold_cyan = "\033[1;36m"
        reset = "\033[0m"   
        border_char = "*"  

        # logo
        osp_art = [
            " #####    #####   ###### ",
            "#     #  #        #     #",
            "#     #  #        #     #",
            "#     #   #####   ###### ",
            "#     #        #  #      ",
            "#     #        #  #      ",
            " #####    #####   #      "
        ]

        details = [
            "OSP (Obod Spam Pinterest)",
            "Created By Obod Star"
        ]
        
        width = 52
        border_width = width + 2 

        print(green + border_char * border_width + reset)

        for line in osp_art:
            print(green + border_char + line.center(width) + border_char + reset)

        print(green + border_char * border_width + reset)

        for detail in details:
            print(green + border_char + detail.center(width) + border_char + reset)

        print(green + border_char * border_width + reset)


    def check_login(self):
        while True:
            try:
                print(end="\rmengecek sesi login....")
                self.user_overview = self.request.getUserOverview("me")
                import json
                open("a.json", "w").write(json.dumps(self.user_overview, indent=4))
                break
            except ConnectionError:
                sleep(3)
                continue
            except:
                break

        return (self.user_overview.get("id") is not None)

    def main(self):
        console = Console(log_time=False)
        reset = "\033[0m"
        bold_cyan = "\033[1;36m"
        green = "\033[38;2;23;255;46m"
        self.screen()
    
        console = Console(log_time=False)
    
        # Konten untuk panel
        content = (
            f"[white]+ Nama         :[/white] [blue]{self.user_overview['full_name']}[/blue]\n"
            f"[white]+ Nama Pengguna:[/white] [blue]{self.user_overview['username']}[/blue]\n"
            f"[white]+ Pin          :[/white] [blue]{self.user_overview['pin_count']}[/blue]\n"
            f"[white]+ Story Pin    :[/white] [blue]{self.user_overview['story_pin_count']}[/blue]\n"
            f"[white]+ Video Pin    :[/white] [blue]{self.user_overview['video_pin_count']}[/blue]\n"
            f"[white]+ Papan        :[/white] [blue]{self.user_overview['board_count']}[/blue]\n"
            f"[white]+ Pengikut     :[/white] [blue]{self.user_overview['follower_count']}[/blue]\n"
            f"[white]+ Mengikuti    :[/white] [blue]{self.user_overview['following_count']}[/blue]"
        )

        # Membuat panel dengan border Rich
        panel = Panel(
            content,
            title="[bold cyan]Profil[/bold cyan]",
            border_style="green"
        )
        console.print(panel)

        console = Console()
    
        # Membuat tabel untuk menu
        table = Table(title="Menu", style="green")
        table.add_column("Fitur", justify="center")
        table.add_column("Deskripsi", justify="left")
        
        # Menambahkan baris menu
        table.add_row("[blue]1[/blue]", "Buat Pin")
        table.add_row("[blue]2[/blue]", "Buat Papan Board")
        table.add_row("[blue]3[/blue]", "Download Foto")
        table.add_row("[red]0[/red]", "Keluar")
        
        # Menampilkan tabel
        console.print(table,justify="center")
        while True:
            try:
                choice = int(input("Pilihan -> "))
            except ValueError:
                print(f"{Fore.RED}pilihan tidak tersedia{Style.RESET_ALL}")
                continue
            except KeyboardInterrupt:
                break
            if choice == 1:
                self.create_pin()
                break
            elif choice == 2:
                self.create_board()
                break
            elif choice == 3:
                self.download_foto()
                break
            elif choice == 0:
                self.logout()
                break
            else:
                print(f"{Fore.RED}pilihan tidak tersedia{Style.RESET_ALL}")

    def login(self):
        self.screen()
        names = [
        "Cili",
        "Sueb",
        "Syfa",
        "Hanna",
        "Clara",
        "Eleanor",
        "Antonel",
        "Ciya",
        "Eye",
        "Nguyen",
        "Cybila",
        "Zara",
        "Jenner",
        "Rossi",
        "-------",
        "Lala",
        "Moza",
        "Nia"
    ]
        emails = [
        "rroji4027@gmail.com",
        "suebkosim@gmail.com",
        "oman6363123@gmail.com",
        "ssakri497@gmail.com",
        "utasueb@gmail.com",
        "sukri63sukri@gmail.com",
        "odabodab04@gmail.com",
        "ssueb517@gmail.com",
        "eyezaixs63@gmail.com",
        "rizki63rizki@gmail.com",
        "doborat63@gmail.com",
        "konakw4001@gmail.com",
        "ucupsurucup39@gmail.com",
        "otongsurotong1000@gmail.com",
        "---------------------------",
        "oobod011@gmail.com",
        "mozamoja199@gmail.com",
        "marwaditania@gmail.com"
    ]
        
        pw="korbanhack"
    
        console = Console()
    
        # Membuat tabel untuk daftar akun email
        table = Table(title="Akun Email", style="green")
        table.add_column("Nama", justify="left")
        table.add_column("Email", justify="left")
        table.add_column("Password", justify="left")
        
        # Menambahkan baris ke tabel
        for name, email in zip(names, emails):
            table.add_row(name, email, pw)
        
        # Menampilkan tabel
        console.print(table,justify="center")
        
        print("+----------------------- Login ----------------------+")
        print(f"+ {Fore.BLUE}1{Style.RESET_ALL}. Dengan Kredensial")
        print(f"+ {Fore.BLUE}2{Style.RESET_ALL}. Dengan Cookie")
        while True:
            try:
                choice = int(input("Pilihan -> "))
            except ValueError:
                print(f"{Fore.RED}pilihan tidak tersedia{Style.RESET_ALL}")
                continue
            except KeyboardInterrupt:
                break
            if choice == 1:
                self.login_credential()
                break
            elif choice == 2:
                self.login_cookie()
                break
            else:
                print(f"{Fore.RED}pilihan tidak tersedia{Style.RESET_ALL}")

    def create_pin(self):
        CreatePin(self.main)

    def create_board(self):
        CreateBoard(self.main)

    def login_credential(self):
        print("\nLogin dengan kredensial, masukan email & password akun pinterest kamu\n")
        while True:
            try:
                email = input("? Email: ").strip()
                password = input("? Password: ")
                if not email or not password.strip():
                    print(f"{Fore.RED}Masukan data yang valid{Style.RESET_ALL}")
                    continue
                self.request.cookies.clear()
                response = self.request.createSession(email, password)
                self.user_overview = response["profile"]
                self.request.writeSession(response["cookies"])
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}Login gagal ({self.request.getHtttpError(e)}){Style.RESET_ALL}")
                continue
            else:
                print(f"Login sebagai {Fore.GREEN}{self.user_overview['full_name']}{Style.RESET_ALL}")
                input("Enter -> ")
                self.main()
                break

    def login_cookie(self):
        print("\nLogin dengan cookie, untuk mendapatkan cookie bisa menggunakan ekstensi CDN Header & Cookie")
        print("Kamu bisa memasukan file cookie ber-ekstensi .csv\n")
        while True:
            try:
                cookie = input("? Masukan cookie (atau file .csv): ").strip()
                if cookie.endswith(".csv"):
                    if not os.path.exists(cookie):
                        print(f"{Fore.RED}File '{cookie}' tidak ditemukan{Style.RESET_ALL}")
                        continue
                    else:
                        cookie = Utils.load_cookie_from_csv(cookie)
                        if not cookie:
                            print(f"{Fore.RED}file cookie tidak valid pastikan memiliki header name & value{Style.RESET_ALL}")
                            continue
                if isinstance(cookie, str):
                    cookie = Utils.cookie_string_to_dict(cookie)
                self.request.cookies.clear()
                self.request.cookies.update(cookie)
                self.user_overview = self.request.getUserOverview("me")
                self.request.writeSession(cookie)
            except KeyboardInterrupt:
                break
            except HTTPError as e:
                print(f"{Fore.RED}Cookie tidak valid ({str(e)}){Style.RESET_ALL}")
                continue
            except Exception as e:
                print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")
                continue
            else:
                print(f"Login sebagai {Fore.GREEN}{self.user_overview['full_name']}{Style.RESET_ALL}")
                input("Enter -> ")
                self.main()
                break

    def logout(self):
        ask = input("Kamu yakin ingin keluar (Y/n): ").strip().lower()
        if ask != "y": return self.main()
        print("Sedang keluar....")
        while True:
            try:
                self.request.logout()
                print(f"{Fore.GREEN}Berhasil Keluar{Style.RESET_ALL}")
                input("Enter -> ")
                self.login()
                break
            except ConnectionError:
                continue
            except Exception as e:
                print(f"{Fore.RED}{str(self.request.getHtttpError(e))}{Style.RESET_ALL}")
                input("Enter -> ")
                self.main()
                break
        

class CreatePin:
    back: callable
    request: Requests
    photos: list
    delay: int
    link:  str|None
    alt_text: str|None
    board_id: int|None
    description: str|None
    title: str|None
    boards: list
    titles : list

    def __init__(self, back: callable):
        self.back = back
        self.request = Requests()
        self.boards = []
        self.photos = []
        self.delay = 0
        self.board_id = None
        self.alt_text = None
        self.titles = []  # Inisialisasi daftar judul
        self.descriptions = []  # Inisialisasi daftar deskripsi
        self.link = None  # Inisialisasi tautan
        self.title = None  # Judul yang dipilih
        self.description = None  # Deskripsi yang dipilih
        self.main()

    def main(self):
        while True:
            try:
                self.boards = self.request.getAllBoards("me")
                break
            except ConnectionError:
                continue
            except KeyboardInterrupt:
                continue

        if len(self.boards) == 0:
            print("\nKamu tidak mempunyai papan silahkan buat papan terlebih dahulu sebelum menggunakan fitur ini\n")
            input("Kembali -> ")
            self.back()
        else:
            print(f"\n+--------------------- {Back.BLUE} Step 1 {Style.RESET_ALL} ---------------------+")
            for no, item in enumerate(self.boards):
                print(f"+ {Fore.BLUE}{str(no + 1)}{Style.RESET_ALL}. {Fore.GREEN}{item['name']}{Style.RESET_ALL} ({Fore.BLUE}{item['id']}{Style.RESET_ALL})")
            while True:
                try:
                    self.board_id = self.boards[int(input("Pilih Papan -> ")) - 1]["id"]
                    break
                except (ValueError, IndexError):
                    print(f"{Fore.RED}Papan tidak tersedia{Style.RESET_ALL}")
                    continue
                except KeyboardInterrupt:
                    return
            print(f"+--------------------- {Back.BLUE} Step 2 {Style.RESET_ALL} ---------------------+")
            if self.get_photo():
                print(f"+--------------------- {Back.BLUE} Step 3 {Style.RESET_ALL} ---------------------+")
                if self.get_delay():
                    print(f"+--------------------- {Back.BLUE} Step 4 {Style.RESET_ALL} ---------------------+")
                    if self.get_title():
                        print(f"+--------------------- {Back.BLUE} Step 5 {Style.RESET_ALL} ---------------------+")
                        if self.get_link():
                            print(f"+--------------------- {Back.BLUE} Step 6 {Style.RESET_ALL} ---------------------+")
                            if self.get_alt_text():
                                print(f"+--------------------- {Back.BLUE} Step 7 {Style.RESET_ALL} ---------------------+")
                                if self.get_description():
                                    self.create()

    def get_photo(self):
        print("Masukan folder yang berisi daftar foto untuk diposting ke pinterest secara masal\n")
        while True:
            try:
                directory = input("? Folder (contoh: /storage/0003-90F4/ ) : ")
                if not os.path.exists(directory):
                    print(f"{Fore.RED}Folder '{directory}' tidak ditemukan{Style.RESET_ALL}")
                    continue
                self.photos = list(filter(lambda x: x.split(".").pop().lower() in ["png", "jpg", "gif", "jpeg"],
                    Utils.get_file_list_from_dir(directory)
                ))
                if len(self.photos) == 0:
                    print(f"{Fore.RED}Tidak ditemukan foto yang valid dalam folder '{directory}'{Style.RESET_ALL}")
                    continue
                else:
                    print(f"Ditemukan total foto ({Fore.BLUE}{len(self.photos)}{Style.RESET_ALL})"%())
                    break
            except KeyboardInterrupt:
                break
        return len(self.photos) > 0

    def get_delay(self):
        while True:
            try:
                self.delay = int(input("? Delay (dalam detik): "))
                assert self.delay >= 1
                return True
            except (ValueError, AssertionError):
                print(f"{Fore.RED}Delay tidak valid{Style.RESET_ALL}")
                continue
            except KeyboardInterrupt:
                return False

    def get_title(self):
        while True:
            try:
                file_path = input("file judul ( /storage/0003-90F4/judul/home.txt ): ").strip()

                if not file_path:  # Jika pengguna tidak mengisi apa-apa
                    print("Judul tidak akan diisi.")
                    self.titles = []  # Kosongkan daftar judul
                    self.title = None
                    return True

                if not os.path.isfile(file_path):
                    print(f"File '{file_path}' tidak ditemukan. Silakan coba lagi.")
                    continue

                with open(file_path, 'r') as f:
                    self.titles = [line.strip() for line in f if line.strip()]  # Simpan di self.titles

                if not self.titles:
                    print("File tidak mengandung judul yang valid.")
                    continue

                print(f"Total judul dalam file: {len(self.titles)}")
                self.title = random.choice(self.titles)  # Pilih judul acak
                return True

            except KeyboardInterrupt:
                print("\nOperasi dibatalkan oleh pengguna.")
                return False
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                continue

    def get_description(self):
        while True:
            try:
                file_path = input("file deskripsi ( /storage/0003-90F4/deskripsi/home.txt ): ").strip()

                if not file_path:  # Jika pengguna tidak mengisi apa-apa
                    print("Deskripsi tidak akan diisi.")
                    self.descriptions = []  # Kosongkan daftar deskripsi
                    self.description = None
                    return True

                if not os.path.isfile(file_path):
                    print(f"File '{file_path}' tidak ditemukan. Silakan coba lagi.")
                    continue

                with open(file_path, 'r') as f:
                    self.descriptions = [line.strip() for line in f if line.strip()]  # Simpan di self.descriptions

                if not self.descriptions:
                    print("File tidak mengandung deskripsi yang valid.")
                    continue

                print(f"Total deskripsi dalam file: {len(self.descriptions)}")
                self.description = random.choice(self.descriptions)  # Pilih deskripsi acak
                return True

            except KeyboardInterrupt:
                print("\nOperasi dibatalkan oleh pengguna.")
                return False
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                continue

    def get_link(self):
        while True:
            try:
                file_path = input("file tautan ( /storage/0003-90F4/link/link.txt ): ").strip()

                if not file_path:
                    print("Tidak menggunakan tautan untuk posting.")
                    self.links = []  # Kosongkan daftar tautan
                    self.link = None
                    return True

                if not os.path.isfile(file_path):
                    print(f"File '{file_path}' tidak ditemukan. Silakan coba lagi.")
                    continue

                with open(file_path, 'r') as f:
                    self.links = [line.strip() for line in f if line.strip()]

                if not self.links:
                    print("File tidak mengandung tautan yang valid. Melanjutkan tanpa tautan.")
                    self.link = None
                    return True

                print(f"Total tautan dalam file: {len(self.links)}")
                self.link = random.choice(self.links)

                return True

            except KeyboardInterrupt:
                print("\nOperasi dibatalkan oleh pengguna.")
                return False
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                continue

    def get_alt_text(self):
        try:
            self.alt_text = input("? Teks Alternatif (opsional): ").strip()
            return True
        except KeyboardInterrupt:
            return False
            
    def create(self):
        cyan = "\033[38;2;23;255;255m"
        green = "\033[38;2;23;255;46m"
        reset = "\033[0m"
        terminal_width = os.get_terminal_size().columns
        line = cyan + '+' + cyan + '-' * (terminal_width - 2) + cyan + '+' + reset
        print(line)
        sleep(3)
        
        for index, photo in enumerate(self.photos):
            try:
                photo_url = None
                print(f"Mengunggah gambar {Fore.GREEN}{photo}{Style.RESET_ALL}")
                sleep(2)
                while True:
                    try:
                        photo_url = self.request.uploadImage(photo)["image_url"]
                        print(f"Berhasil diunggah dengan tautan {Fore.BLUE}{photo_url}{Style.RESET_ALL}")
                        sleep(2)
                        break
                    except ConnectionError:
                        continue
                    except Exception as e:
                        print(f"{Fore.RED}{self.request.getHtttpError(e)}{Style.RESET_ALL}")
                        break
                if photo_url:
                    kwargs = {
                        "imageUrl": photo_url,
                        "boardId": self.board_id,
                        "altText": self.alt_text,
                    }

                    if self.title:  # Tampilkan judul hanya jika ada
                        kwargs["title"] = self.title

                    if self.description:  # Tampilkan deskripsi hanya jika ada
                        kwargs["description"] = self.description

                    if self.link:  # Tampilkan tautan hanya jika ada
                        kwargs["link"] = self.link

                    while True:
                        try:
                            print("Membuat pin...")
                            sleep(2)
                            response = self.request.createPin(**kwargs)

                            # Pesan berhasil
                            print(f"{Fore.GREEN}Pin telah diterbitkan dengan id{Style.RESET_ALL} ({Fore.BLUE}{response['id']}{Style.RESET_ALL})")
                            if self.title:
                                self.title = random.choice(self.titles)
                                print(f"Berhasil diunggah dengan judul: {Fore.BLUE}{self.title}{Style.RESET_ALL}")
                            if self.description:
                                self.description = random.choice(self.descriptions)
                                print(f"Berhasil diunggah dengan deskripsi: {Fore.BLUE}{self.description}{Style.RESET_ALL}")
                            if self.link:
                                self.link = random.choice(self.links)
                                print(f"Berhasil diunggah dengan tautan: {Fore.BLUE}{self.link}{Style.RESET_ALL}")

                            print(f"Foto ke-{index + 1} berhasil.")
                            break
                        except ConnectionError:
                            continue
                        except Exception as e:
                            print(f"{Fore.RED}Gagal ({self.request.getHtttpError(e)}){Style.RESET_ALL}")
                            break
                    print(line)
                    if index < (len(self.photos) - 1):
                        for remaining in range(self.delay, 0, -1):
                            print(f"{Fore.YELLOW}Mengunggah dalam {remaining} detik...{Style.RESET_ALL}", end="\r", flush=True)
                            sleep(2)
                            print(" " * 50, end="\r")
            except KeyboardInterrupt:
                break
        input("Kembali -> ")
        self.back()

        
    
class CreateBoard:
    back: callable
    request: Requests
    name: str|None
    description: str|None
    privacy: str|None
    category: str|None

    def __init__(self, back: callable):
        self.request = Requests()
        self.back = back
        self.name = None
        self.description = None
        self.privacy = None
        self.category = None
        
        print(f"+------------------ Buat Papan --------------------+")
        if self.get_name():
            if self.get_description():
                if self.get_privacy():
                    if self.get_category():
                        self.create()

    def get_name(self):
        while True:
            try:
                self.name = input("? Nama: ").strip()
                if not self.name:
                    print(f"{Fore.RED}Nama wajib diisi{Style.RESET_ALL}")
                    continue
                return True
            except KeyboardInterrupt:
                return False

    def get_description(self):
        try:
            print("\nGunakan <> sebagai baris baru\n")
            self.description = input("? Deskripsi: ")
            return True
        except KeyboardInterrupt:
            return False
        
    def get_privacy(self):
        print(f"+-------------------- Privasi ---------------------+")
        for no, name in enumerate(self.request.board_privacy):
            print(f"+ {Fore.BLUE}{str(no + 1)}{Style.RESET_ALL}. {name}")
        while True:
            try:
                privacy = self.request.board_privacy[int(input("Privasi -> ")) - 1]
                self.privacy = self.get_option_value(privacy)
                return True
            except (ValueError, IndexError):
                print(f"{Fore.RED}Pilihan tidak tersedia{Style.RESET_ALL}")
                continue
            except KeyboardInterrupt:
                return False
    
    def get_category(self):
        print(f"+-------------------- Kategori --------------------+")
        for no, name in enumerate(self.request.board_category):
            print(f"+ {Fore.BLUE}{str(no + 1)}{Style.RESET_ALL}. {name}")
        while True:
            try:
                category = self.request.board_category[int(input("Kategori -> ")) - 1]
                self.category = self.get_option_value(category)
                return True
            except (ValueError, IndexError):
                print(f"{Fore.RED}Pilihan tidak tersedia{Style.RESET_ALL}")
                continue
            except KeyboardInterrupt:
                return False
            
    def get_option_value(self, value: str) -> str:
        return re.search(r"\((.*?)\)", value.strip()).group(1)
    
    def create(self):
        print("\nSedang Membuat papan...")
        while True:
            try:
                response = self.request.createBoard(
                    name=self.name,
                    description=self.description,
                    privacy=self.privacy,
                    category=self.category
                )
                print(f"Papan berhasil dibuat dengan id ({Fore.BLUE}{response['id']}{Style.RESET_ALL})")
                break
            except ConnectionError:
                continue
            except Exception as e:
                print(f"{Fore.RED}Papan gagal dibuat ({self.request.getHtttpError(e)}){Style.RESET_ALL}")
                break
        input("Enter -> ")
        self.back()


if __name__ == "__main__":
    Pinterest()
