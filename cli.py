import os
import re
from time import sleep
from pin.requests import Requests
from pin.utils import Utils
from colorama import Fore, Back, Style
from requests.exceptions import (ConnectionError, HTTPError)

class Pinterest:
    user_overview: dict
    request: Requests

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
            "Created By Obod Star",
            "Version: 3.0"
        ]
        
        width = 40
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
        self.screen()
        print("+-------------- Profile --------------+")
        print(f"+ Nama {Fore.GREEN}{self.user_overview['full_name']}{Style.RESET_ALL}")
        print(f"+ Nama Pengguna {Fore.GREEN}{self.user_overview['username']}{Style.RESET_ALL}")
        print(f"+ Pin {Fore.BLUE}{self.user_overview['pin_count']}{Style.RESET_ALL}")
        print(f"+ Story Pin {Fore.BLUE}{self.user_overview['story_pin_count']}{Style.RESET_ALL}")
        print(f"+ Vidio Pin {Fore.BLUE}{self.user_overview['video_pin_count']}{Style.RESET_ALL}")
        print(f"+ Papan {Fore.BLUE}{self.user_overview['board_count']}{Style.RESET_ALL}")
        print(f"+ Pengikut {Fore.BLUE}{self.user_overview['follower_count']}{Style.RESET_ALL}")
        print(f"+ Mengikuti {Fore.BLUE}{self.user_overview['following_count']}{Style.RESET_ALL}")
        print("+---------------- Menu ---------------+")
        print(f"+ {Fore.BLUE}1{Style.RESET_ALL}. Buat Pin")
        print(f"+ {Fore.BLUE}2{Style.RESET_ALL}. Buat Papan Board")
        print(f"+ {Fore.RED}0{Style.RESET_ALL}. Keluar")
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
            elif choice == 0:
                self.logout()
                break
            else:
                print(f"{Fore.RED}pilihan tidak tersedia{Style.RESET_ALL}")

    def login(self):
        self.screen()
        print("+--------------- Login ---------------+")
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
            print(f"\n+------------- {Back.BLUE} Step 1 {Style.RESET_ALL} --------------+")
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
            print(f"+------------- {Back.BLUE} Step 2 {Style.RESET_ALL} --------------+")
            if self.get_photo():
                print(f"+------------- {Back.BLUE} Step 3 {Style.RESET_ALL} --------------+")
                if self.get_delay():
                    print(f"+------------- {Back.BLUE} Step 4 {Style.RESET_ALL} --------------+")
                    if self.get_title():
                        print(f"+------------- {Back.BLUE} Step 5 {Style.RESET_ALL} --------------+")
                        if self.get_link():
                            print(f"+------------- {Back.BLUE} Step 6 {Style.RESET_ALL} --------------+")
                            if self.get_alt_text():
                                print(f"+------------- {Back.BLUE} Step 7 {Style.RESET_ALL} --------------+")
                                if self.get_description():
                                    self.create()

    def get_photo(self):
        print("Masukan folder yang berisi daftar foto untuk diposting ke pinterest secara masal\n")
        while True:
            try:
                directory = input("? Folder (contoh: /sdcard/DCIM): ")
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
            self.title = input("? Judul (opsional): ").strip()
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
      print(f"+------------------------------------+")
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
                          print(f"Foto ke-{index + 1} berhasil")
                          break
                      except ConnectionError:
                          continue
                      except Exception as e:
                          print(f"{Fore.RED}Gagal ({self.request.getHtttpError(e)}){Style.RESET_ALL}")
                          break
              print(f"+------------------------------------+")
              if index < (len(self.photos) - 1):
                  sleep(self.delay)
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
    
