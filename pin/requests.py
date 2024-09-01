from requests.structures import CaseInsensitiveDict
from requests_toolbelt import MultipartEncoder
from urllib.parse import (urlparse, parse_qsl, quote_plus)
from urllib.parse import urlencode

from .url import Url
from .bookmarkmanager import BookmarkManager

import mimetypes
import requests
import json
import time
import re
import os

class Requests(requests.Session):
    bookmarkManager: BookmarkManager
    sessionFile: str

    board_privacy: list = [
        "Jaga (potected)",
        "Rahasia (secret)",
        "Publik (public)"
    ]

    board_category = [
        "Lainnya (other)",
        "Binatang (animals)",
        "Pakaian (apparel)",
        "Arsitektur (architecture)",
        "Seni (art)",
        "Lengukan Seni (art_arch)",
        "Mobil Sepeda Motor (cars_motorcycles)",
        "Selebriti (celebrities)",
        "Selebriti Toko Publik (celebrities_public_figures)",
        "Perdagangan (commerce)",
        "Corgis (corgis)",
        "Budaya (culture)",
        "Desain (design)",
        "Kerajinan Sendiri (diy_crafts)",
        "Pendidikan (education)",
        "Semuanya (everything)",
        "Gaya (fashion)",
        "Unggulan (featured)",
        "Buku Musik Film (film_music_books)",
        "Kebugaran (fitness)",
        "Makanan Minuman (food_drink)",
        "Untuk Ayah (for_dad)",
        "Segar (fresh)",
        "Berkebun (gardening)",
        "Kutu Buku (geek)",
        "Panduan Hadiah (gift_guides)",
        "Hadiah (gifts)",
        "Kecantikan Rambut (hair_beauty)",
        "Kesehatan & Kebugaran (health_fitness)",
        "Sejarah (history)",
        "Liburan (holidays)",
        "Acara Liburan (holidays_events)",
        "Rumah (home)",
        "Dekorasi Rumah (home_decor)",
        "Perbaikan Rumah (home_improvement)",
        "Humor (humor)",
        "Ilustrasi Poster (illustrations_posters)",
        "Anak-Anak (kids)",
        "Pakaian Pria (men_apparel)",
        "Busana Pria (mens_fashion)",
        "Pakaian Wanita (women_apparel)",
        "Fashion Wanita (womens_fashion)",
        "Hidupku (mylife)",
        "Diluar Rumah (outdoors)",
        "Orang (people)",
        "Hewan Peliharaan (pets)",
        "Fotografi (photography)",
        "Populer (popular)",
        "Mencetak Poster (prints_posters)",
        "Produk (products)",
        "Kutipan (quotes)",
        "Sains (science)",
        "Ilmu Pengetahuan (science_nature)",
        "Toko (shop)",
        "Ruang Toko (shop_space)",
        "Olahraga (sports)",
        "Tato (tattoos)",
        "Teknologi (technology)",
        "Traveling (travel)",
        "Tempat Pejalanan (travel_places)",
        "Vidio (videos)",
        "Acara Pernikahan (wedding_events)",
        "Pernikahan (weddings)"
    ]

    def __init__(self):
        super(Requests, self).__init__()
        self.init()

    def init(self):
        self.bookmarkManager = BookmarkManager()
        self.sessionFile = os.path.abspath(".session")
        self.cookies.clear()
        sessionData = self.loadSession()
        if sessionData != None:
            self.cookies.update(
                sessionData
            )

    def loadSession(self):
        if not self.hasSessionExists():
            return None
        
        f = open(self.sessionFile, "r", encoding="utf-8")
        
        try:
            sessionData = json.loads(f.read())
            assert isinstance(sessionData, dict)
        except:
            sessionData = {}

        if sessionData.get("_auth") != "1":
            return None

        return {key: str(value) for key, value in list(sessionData.items())}

    def hasSessionExists(self) -> bool:
        return os.path.exists(self.sessionFile) and os.path.isfile(self.sessionFile)
    
    def isAuth(self) -> bool:
        return self.cookies.get("_auth") == "1"

    def writeSession(self, data: dict):
        if os.path.isdir(self.sessionFile):
            raise ValueError("session file is directory '%s' "%(self.sessionFile))

        f = open(self.sessionFile, "w")
        f.write(json.dumps(data, indent=4))
        f.close()

    def removeSession(self, clearCookie: bool = True):
        if self.hasSessionExists():
            os.remove(self.sessionFile)

        if clearCookie:
            self.cookies.clear()

    def logout(self, removeSessionFile: bool = True):
        params = self.makeParams({
            "disable_auth_failure_redirect": True
        })

        response = self.makeRequest("POST", Url.DELETE_SESSION_RESOURCE, data=params)
        response.raise_for_status()

        if removeSessionFile:
            self.removeSession()

    def getUserOverview(self, username: str):
        params = self.makeParams({
            "isPrefect": False,
            "username": username,
            "field_set_key": "profile"
        })

        response = self.makeRequest("GET", Url.USER_RESOURCE, params=params)
        response.raise_for_status()
        data = response.json()

        return data["resource_response"]["data"]
    
    def getBoards(self, username: str, pageSize: int = 50, resetBookmark: bool = False):
        primary = "board"
        bookmark = self.bookmarkManager.getBookmark(primary, username)

        if bookmark == "-end-":
            if resetBookmark:
                self.bookmarkManager.deleteBookmark(primary, username)
            return []

        sourceUrl = "/%s/boards/"%(username)
        params = self.makeParams({
            "page_size": pageSize,
            "privacy_filter": "all",
            "sort": "custom",
            "username": username,
            "isPrefect": False,
            "include_archived": True,
            "filed_set_key": "profile_grid_item",
            "group_by": "visibility",
            "redux_normalize_feed": True,
            "bookmarks": [bookmark]
        }, sourceUrl=sourceUrl)

        response = self.makeRequest("GET", Url.BOARD_RESOURCE, params=params)
        response.raise_for_status()
        data = response.json()

        bookmark = data["resource"]["options"]["bookmarks"][0]
        self.bookmarkManager.setBookmark(bookmark, primary, username)

        return data["resource_response"]["data"]

    def getAllBoards(self, username: str):
        boards = []
        boards_batch = self.getBoards(username)

        while len(boards_batch) > 0:
            boards += boards_batch
            boards_batch = self.getBoards(username)
        
        return boards
    
    def createBoard(
        self, name: str, description: str = "", category: str = "other", privacy: str = "public", layout: str = "default"
    ):
        # privacy (str) = protected, public, secret
        # category (str) = animals,apparel,architecture,art,art_arch,cars_motorcycles,celebrities,celebrities_public_figures,commerce,corgis,culture,design,diy_crafts,education,everything,fashion,featured,film_music_books,fitness,food_drink,for_dad,fresh,gardening,geek,gift_guides,gifts,hair_beauty,health_fitness,history,holidays,holidays_events,home,home_decor,home_improvement,humor,illustrations_posters,kids,men_apparel,mens_fashion,mylife,other,outdoors,people,pets,photography,popular,prints_posters,products,quotes,science,science_nature,shop,shop_space,sports,tattoos,technology,travel,travel_places,videos,wedding_events,weddings,women_apparel,womens_fashion

        params = self.makeParams(
            # sourceUrl = "/%s/boards/"%(email),
            data = {
                "name": name,
                "description": description,
                "category": category,
                "privacy": privacy,
                "layout": layout,
                "collab_board_email": True,
                "collaborator_invites_enabled": True,
            }
        )

        response = self.makeRequest("POST", Url.CREATE_BOARD_RESOURCE, data=params)
        response.raise_for_status()
        data = response.json()
        
        return data["resource_response"]["data"]
    
    def createSession(self, email: str, password: str):
        request = Requests() # create new request instance
        request.makeRequest("GET", Url.LOGIN_PAGE, jsRequest=False)

        time.sleep(1.5)

        try:
            captcha = request.getCaptchaToken(
                "https://www.recaptcha.net/recaptcha/enterprise/anchor?ar=1&k=6Ldx7ZkUAAAAAF3SZ05DRL2Kdh911tCa3qFP0-0r&co=aHR0cHM6Ly9pZC5waW50ZXJlc3QuY29tOjQ0Mw..&hl=en&v=9pvHvq7kSOTqqZusUzJ6ewaF&size=invisible&cb=6ef5fnhbugxh"
            )
        except Exception as err:
            raise Exception("Failed solve the captcha error(%s)"%(str(err)))

        params = self.makeParams(
            sourceUrl = "/login/",
            data = {
                "recaptchaV3Token": captcha,
                "get_user": True,
                "username_or_email": email,
                "password": password,
                "app_type_from_client": 6
            }
        )

        time.sleep(1.5)

        extraHeaders = dict(
            [
                ("X-Pinterest-Pws-Handler", "www/login.js")
            ]
        )

        response = request.makeRequest("POST", Url.CREATE_SESSION_RESOURCE, extraHeaders=extraHeaders, data=params)
        response.raise_for_status()
        
        data: dict = response.json()["resource_response"]["data"]

        profile = request.getUserOverview("me")

        data.update({"cookies": request.cookies.get_dict(), "profile": profile})
        return data
    
    def uploadPin(
        self,
        imageFile: str,
        boardId: str,
        title: str|None = None,
        link: str|None = None,
        description: str|None = None,
        altText: str|None = None,
        sectionId: str|None = None
    ):
        imageUrl = self.uploadImage(imageFile)["image_url"]

        return self.createPin(
            imageUrl=imageUrl,
            boardId=boardId,
            title=title,
            link=link,
            description=description,
            altText=altText,
            sectionId=sectionId
        )

    def createPin(
        self,
        imageUrl: str,
        boardId: str,
        title: str|None = None,
        link: str|None = None,
        description: str|None = None,
        altText: str|None = None,
        sectionId: str|None = None
    ):
        options = {
            "board_id": boardId,
            "image_url": imageUrl,
            "title": title,
            "alt_text": altText,
            "description": description,
            "section": sectionId,
            "link": link if link else imageUrl,
            "scrape_metric": {"source": "www_url_scrape"},
            "method": "uploaded",
        }

        params = self.makeParams(
            sourceUrl="/pin/find/?url=%s"%(quote_plus(imageUrl)),
            data=options
        )

        response = self.makeRequest("POST", Url.PIN_RESOURCE_CREATE, data=params)
        response.raise_for_status()
        data = response.json()

        return data["resource_response"]["data"]

    def getCaptchaToken(self, anchorUrl: str):
        parse = urlparse(anchorUrl)
        captchaType = re.search(r"\/recaptcha\/(enterprise|api2)\/anchor", parse.path)
        if not captchaType:
            raise ValueError("invalid anchor url")

        captchaType = captchaType.group(1)
        url = "https://www.google.com/recaptcha/%s/{0}"%(captchaType)
        params = dict(parse_qsl(parse.query))
        headers = CaseInsensitiveDict(
            [
                ("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
            ]
        )

        response = self.get(url.format("anchor"), headers=headers, params=params).text
        anchorToken = re.search(r"value=\"(.*?)\">", response)

        if not anchorToken:
            raise Exception("anchor token not found")

        anchorToken = anchorToken.group(1)

        time.sleep(3)

        data = dict(
            [
                ("c", anchorToken),
                ("v", params.get("v")),
                ("k", params.get("k")),
                ("co", params.get("co")),
                ("reason", "q"),
            ]
        )

        response = self.post(url.format("reload"), params={"k": params.get("k")}, data=data).text
        captchaToken = re.search(r"\"rresp\",\"(.*?)\"", response)
        if not captchaToken:
            raise Exception("captcha token not found")

        return captchaToken.group(1)

    def makeRequest(self, method: str, url: str, jsRequest: bool = True, extraHeaders: dict = dict(), **kwargs):
        headers = CaseInsensitiveDict(
            [
                ("Referer", Url.HOME_PAGE),
                ("Accept", "application/json"),
                ("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"),
                ("User-Agent", "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"),
                ("Accept-Language", "en-US;q=0.9")
            ]
        )

        if jsRequest:
            headers.update([
                ("X-Requested-With", "XMLHttpRequest"),
                ("X-Pinterest-Appstate", "active"),
                ("X-App-Version", "f8146f7")
            ])

        if (csrfToken := self.cookies.get("csrftoken")):
            headers.update([("X-CSRFToken", csrfToken)])

        if isinstance(kwargs.get("data"), dict):
            if (sourceUrl := kwargs["data"].get("source_url")):
                headers.update([("X-Pinterest-Source-Url", sourceUrl)])

        if extraHeaders:
            headers.update(extraHeaders)

        return self.request(method, url, headers=headers, **kwargs)

    def makeParams(self, data: dict, sourceUrl: str = "/", context: dict = {}) -> dict:
        return (
            {
                "_": str(int(time.time() * 1000)),
                "source_url": sourceUrl,
                "data": json.dumps({
                    "options": data,
                    "context": context
                })
            }
        )
    
    def uploadImage(self, imageFile: str):
        if not os.path.exists(imageFile):
            raise FileNotFoundError("File '%s' not found"%(imageFile))
        if not os.path.isfile(imageFile):
            raise ValueError("File '%s' is not valid")
        
        fileName = os.path.basename(imageFile)
        mimeType = mimetypes.guess_type(imageFile)[0]

        data = MultipartEncoder(
            fields={"img": (fileName, open(imageFile, "rb"), mimeType)}
        )
        headers = dict(
            [
                ("Content-Length", str(data.len)),
                ("Content-Type", data.content_type),
                ("X-UPLOAD-SOURCE", "pinner_uploader")
            ]
        )

        response = self.makeRequest("POST", Url.UPLOAD_IMAGE, extraHeaders=headers, data=data)
        response.raise_for_status()

        return response.json()
    
    def getHtttpError(self, error: Exception) -> str:
        try:
            msg = error.response.json()["resource_response"]["error"]["message"]
        except:
            msg = str(error)

        return msg