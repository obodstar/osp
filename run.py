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
from titles import titles
import hashlib
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
        console = Console(log_time=False)

        def generate_random_filename(extension=".jpg"):
            """Generate random filenames with MD5 hash."""
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            return hashlib.md5(random_string.encode()).hexdigest() + extension

        def setup_chromedriver():
            """Setup ChromeDriver for Termux."""
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Headless mode
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_service = Service("/data/data/com.termux/files/usr/bin/chromedriver")  # Lokasi driver ARM
            return webdriver.Chrome(service=chrome_service, options=chrome_options)

        def get_all_images(driver):
            """Scroll halaman untuk memuat semua gambar dan mengembalikan elemen gambar dengan kualitas terbaik."""
            console.log("Proses Scroll halaman...")
            last_height = 0
            all_images = set()  # Menggunakan set untuk menghindari duplikasi
            try:
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    images = soup.find_all("img")
                    for img in images:
                        # Coba ambil URL dari atribut data-pin-media, data-src, atau src
                        high_res = img.get("data-pin-media") or img.get("data-src") or img.get("src")
                        if high_res:
                            # Jika URL mengandung resolusi rendah (misalnya 236x), ganti dengan resolusi lebih tinggi (misalnya 736x)
                            if "236x" in high_res:
                                high_res = high_res.replace("236x", "736x")
                            elif "474x" in high_res:
                                high_res = high_res.replace("474x", "736x")
                            all_images.add(high_res)

                    # Update jumlah foto yang terdeteksi
                    console.log(f"Sedang mengumpulkan  : {len(all_images)} foto")

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)  # Tambahkan waktu tunggu agar gambar HD sepenuhnya dimuat

                    # Cek apakah tinggi halaman berubah (sudah mencapai akhir)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
            except KeyboardInterrupt:
                console.log("[red]Proses dihentikan oleh pengguna.[/red]")
            finally:
                console.log(f"Total gambar yang terdeteksi: {len(all_images)}")
            return list(all_images)

        def download_images(images, download_path, max_images):
            """Unduh gambar dari daftar gambar dengan retry otomatis jika terjadi error jaringan."""
            console.log(f"Mengunduh {max_images} gambar...")
            success_count = 0

            # Membuat folder unduhan jika belum ada
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            # Mengunduh gambar
            for idx, img_url in enumerate(images[:max_images]):
                retry_count = 0
                while retry_count < 5:  # Maksimal 5 kali percobaan jika koneksi gagal
                    try:
                        img_data = requests.get(img_url, timeout=10).content
                        file_name = os.path.join(download_path, generate_random_filename())
                        with open(file_name, "wb") as f:
                            f.write(img_data)
                        success_count += 1

                        # Tampilkan panel untuk setiap foto yang berhasil diunduh
                        panel = Panel(f"[blue]Foto ke-{idx + 1} berhasil diunduh![/blue]\n[bold]Lokasi:[/bold] {file_name}",
                                    title=f"[bold cyan]Foto {idx + 1}[/bold cyan]",
                                    border_style="green")
                        console.print(panel)
                        break  # Keluar dari loop retry jika berhasil

                    except RequestException as e:
                        retry_count += 1
                        console.print(f"[yellow]Koneksi gagal saat mengunduh gambar {idx + 1}. Percobaan ulang ({retry_count}/5)...[/yellow]")
                        time.sleep(5)  # Tunggu 5 detik sebelum mencoba lagi

                    except Exception as e:
                        console.print(f"[red]Gagal mengunduh gambar {idx + 1}: {e}[/red]")
                        break

                if retry_count == 5:
                    console.print(f"[red]Gagal mengunduh gambar {idx + 1} setelah 5 kali percobaan.[/red]")

            console.log(f"Total berhasil diunduh: [green]{success_count}[/green] dari {max_images} gambar.")
        

        def input_with_validation(prompt, validation_func, error_message):
            """Meminta input dari pengguna dengan validasi."""
            while True:
                user_input = input(prompt)
                if validation_func(user_input):
                    return user_input
                else:
                    console.print(f"[red]{error_message}[/red]")

        if __name__ == "__main__":
            # Meminta URL papan dengan validasi agar tidak kosong
            board_url = input_with_validation("Masukkan URL papan Pinterest: ", lambda x: x.startswith("http"), "URL harus valid dan dimulai dengan 'http'.")

            download_path = "/storage/0003-90F4/pin"

            # Inisialisasi driver Selenium
            driver = setup_chromedriver()
            driver.get(board_url)
            time.sleep(3)  # Tunggu pemuatan awal

            # Scroll dan ambil gambar
            images = get_all_images(driver)
            driver.quit()  # Tutup browser

            total_images = len(images)
            console.print(f"Papan memiliki total [bold yellow]{total_images}[/bold yellow] foto.")

            # Meminta jumlah foto yang ingin diunduh
            while True:
                try:
                    max_images = int(input(f"jumlah foto (max {total_images}): "))
                    if 0 < max_images <= total_images:
                        break
                    else:
                        console.print("[red]Masukkan jumlah yang valid.[/red]")
                except ValueError:
                    console.print("[red]Masukkan angka yang valid.[/red]")

            # Mengunduh gambar
            download_images(images, download_path, max_images)

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
        "Lala",
        "Sueb",
        "Syfa",
        "Hanna",
        "Clara",
        "Eleanor",
        "Antonella",
        "Ciya"
    ]
        emails = [
        "rroji4027@gmail.com",
        "oobod011@gmail.com",
        "suebkosim@gmail.com",
        "oman6363123@gmail.com",
        "ssakri497@gmail.com",
        "utasueb@gmail.com",
        "sukri63sukri@gmail.com",
        "odabodab04@gmail.com",
        "ssueb517@gmail.com"
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
        self.link = None
        self.alt_text = None
        self.description = None
        self.title = None

        self.titles = titles

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
        try:
            self.title = random.choice(self.titles)  # Pilih judul secara acak dari daftar
            print(f"Judul dipilih: {self.title}")
            return True
        except KeyboardInterrupt:
            return False

    def get_description(self):
        try:
            print("\nGunakan <> sebagai baris baru\n")
            self.description = input("? Deskripsi (opsional): ").strip().replace("<>", "\n")
            return True
        except KeyboardInterrupt:
            return False

    def get_link(self):
        while True:
            try:
                self.link = input("? Link (opsional): ").strip()
                if self.link != "" and not Utils.is_valid_url(self.link):
                    print(f"{Fore.RED}Link tidak valid{Style.RESET_ALL}")
                    continue
                return True
            except KeyboardInterrupt:
                return False

    def get_alt_text(self):
        try:
            self.alt_text = input("? Teks Alternatif (opsional): ").strip()
            return True
        except KeyboardInterrupt:
            return False
            
    def create(self):
        print(f"+----------------------------------------------------+")
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
                    # Pilih judul secara acak untuk setiap foto
                    self.title = random.choice(self.titles)  # Pilih judul acak
                    kwargs = dict(
                        [
                            ("imageUrl", photo_url),
                            ("boardId", self.board_id),
                            ("title", self.title),
                            ("link", self.link),
                            ("description", self.description),
                            ("altText", self.alt_text),
                        ]
                    )
                    while True:
                        try:
                            print("Membuat pin...")
                            sleep(2)
                            response = self.request.createPin(**kwargs)
                            print(f"{Fore.GREEN}Pin telah diterbitkan dengan id{Style.RESET_ALL} ({Fore.BLUE}{response['id']}{Style.RESET_ALL})")
                            # Tambahan: Informasi foto ke-n
                            print(f"Berhasil diunggah dengan judul {Fore.BLUE}{self.title}{Style.RESET_ALL}")
                            print(f"Foto ke-{index + 1} berhasil")
                            break
                        except ConnectionError:
                            continue
                        except Exception as e:
                            print(f"{Fore.RED}Gagal ({self.request.getHtttpError(e)}){Style.RESET_ALL}")
                            break
                    print(f"+----------------------------------------------------+")
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
        print(f"+----------- Buat Papan -------------+")
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
        print(f"+------------ Privasi --------------+")
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
        print(f"+------------ Kategori -------------+")
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