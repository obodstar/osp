from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from .create import Create
from .login import Login
from .base import Base

import os
import platform

class Pinterest(Base):
    sessionFile: str = None

    def __init__(self, sessionFile: str = None, driverOption: webdriver.ChromeOptions = None):
        if not driverOption:
            driverOption = webdriver.ChromeOptions()
            driverOption.add_argument("--lang=en")
            driverOption.add_argument("--mute-audio")
            driverOption.add_argument("--headless")
            driverOption.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36")

        arch = platform.architecture()[0]
        platformName = platform.system().lower()

        driverPath = None

        if platformName[:3] == "win":
            if arch == "64bit":
                driverPath = "driver/windows/chrome-64"
            if arch == "32bit":
                driverPath = "driver/windows/chrome-32"
        if platformName[:3] == "lin":
            if arch == "64bit":
                driverPath = "driver/linux/chrome-64"

        if not driverPath:
            raise Exception("Driver not available for your devices. platform(%s). arch(%s)"%(platformName, arch))

        driver = webdriver.Chrome(
            service = Service(os.path.abspath(driverPath)),
            options = driverOption
        )

        driver.set_window_size(860, 540)

        super(Pinterest, self).__init__(driver)
        self.sessionFile = sessionFile

        # self.setup()

    def setup(self):
        if self.sessionFile:
            self.syncSession(self.sessionFile)

    def create(self):
        return Create(self.driver)
    
    def login(self):
        return Login(self.driver, self.sessionFile)
    
    def isLoggedIn(self) -> bool:
        if not self.hasSessionExists():
            return False

        try:
            self.syncSession(self.sessionFile)
            self.driver.get(self.url("/"))
            self.driver.implicitly_wait(5)
            self.waitVisible("//div[@data-test-id='header-profile']", 5)
            return True
        except TimeoutException:
            return False

    def hasSessionExists(self) -> bool:
        return os.path.exists(self.sessionFile)

    def removeSession(self) -> None:
        if self.hasSessionExists():
            os.remove(self.sessionFile)