from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import os, json, time

class Base:
    driver: WebDriver
    baseUrl: str = "https://id.pinterest.com"

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def url(self, sufix: str = "/"):
        return self.baseUrl + sufix

    def waitVisible(self, xpath: str, timeout: int = 20) -> WebElement:
        return WebDriverWait(self.driver, timeout) \
            .until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def waitClickable(self, xpath: str, timeout: int = 20) -> WebElement:
        return WebDriverWait(self.driver, timeout) \
            .until(EC.element_to_be_clickable((By.XPATH, xpath)))
    
    def ignoreCaseEqualsXPath(self, attribute: str, value: str) -> str:
        return "translate(%s, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='%s'"%(
            attribute,
            value.lower().replace("'", "\\'")
        )

    def click(self, xpath: str) -> None:
        self.waitClickable(xpath).click()

    def sendKeys(self, xpath: str, value: str):
        try:
            el = self.driver.find_element(By.XPATH, xpath)
            el.send_keys(value)
        except NoSuchElementException:
            el = self.waitVisible(xpath)
            el.send_keys(value)

    def syncSession(self, file: str):
        if (os.path.exists(file)):
            try:
                self.driver.get(self.url())

                time.sleep(3)

                data = json.loads(open(file, "r").read())
                for item in data:
                    name, value = [item.get("name"), item.get("value")]
                    if (isinstance(name, str) and isinstance(value, str)):
                        self.driver.add_cookie({"name": name, "value": value, "domain": "pinterest.com"})
            except json.decoder.JSONDecodeError:
                os.remove(file)
