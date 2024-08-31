import re
import os
import csv

from urllib.parse import urlparse
from requests.exceptions import HTTPError

class Utils:

    @staticmethod
    def cookie_string_to_dict(cookie: str) -> dict:
        array = re.findall(r"([^;]+)", cookie)
        objects = {}
        for string in array:
            string = string.strip()
            string_array = string.split("=")
            objects[string_array[0]] = "=".join(string_array[1:])
        return objects

    @staticmethod
    def cookie_dict_to_string(cookie: dict) -> str:
        return ";".join(["%s=%s"%(name, values) for name,values in cookie.items()])

    @staticmethod
    def load_cookie_from_csv(file: str):
        cookies = dict()
        with open(file, "r", encoding="utf-8") as f:
            data = list(csv.DictReader(f))
            for item in data:
                item = dict((name.lower(), value) for name, value in item.items())
                name = item.get("name", item.get("names"))
                value = item.get("value", item.get("values"))
                if isinstance(name, str) and isinstance(value, str):
                    cookies[name] = value
            f.close()
        return cookies
    
    @staticmethod
    def get_file_list_from_dir(dir: str):
        result = []
        for file in os.listdir(dir):
            file = os.path.join(dir, file)
            if os.path.isdir(file):
                result+= Utils.get_file_list_from_dir(file)
            else:
                result.append(file)
        return result
    
    @staticmethod
    def get_error_msg_from_http_error(error: HTTPError) -> str:
        try:
            msg = error.response.json()["resource_response"]["error"]["message"]
        except:
            msg = str(error)

        return msg
    
    
    @staticmethod
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
