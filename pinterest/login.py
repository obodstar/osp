from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from .base import Base

import json

class Login(Base):
    def __init__(self, driver: WebDriver, sessionFile: str):
        super(Login, self).__init__(driver)

        self.sessionFile = sessionFile

    def attempt(self, email: str, password: str) -> bool:
        cookies = self.login(email, password)
        if cookies:
            open(self.sessionFile, "w").write(json.dumps(cookies, indent=4))
        
        return bool(cookies)

    def login(self, email: str, password: str) -> dict | None:
        try:
            self.driver.get(self.url("/login"))
            self.driver.implicitly_wait(5)
            try:
                self.waitVisible("//div[@data-test-id='header-profile']", 5)
            except:
                self.sendKeys("//input[@id='email']", email)
                self.sendKeys("//input[@id='password']", password)

                sleep(3)

                self.click("//div[@data-test-id='registerFormSubmitButton']/button")

                WebDriverWait(self.driver, 20) \
                    .until(lambda driver: ("/login" not in driver.current_url))

                cookies = self.driver.get_cookies()
                cookie_keys = list(map(lambda x: x["name"], cookies))

                isLogin = ("__Secure-s_a" in cookie_keys)
                if isLogin:
                    return cookies
                return None
            else:
                raise Exception("Already logged in")
        except TimeoutException:
            return None
        finally:
            self.driver.quit()