from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from .base import Base
from .form import Form

import json

class Create(Base):
    def __init__(self, driver: WebDriver):
        super(Create, self).__init__(driver)

    def upload(self, pin: Form) -> None:
        try:
            pin.validate()
            self.driver.get(self.url("/pin-creation-tool"))
            self.driver.implicitly_wait(5)

            self.waitVisible("//div[@data-test-id='drag-behavior-container']")
            self.sendKeys("//input[@data-test-id='storyboard-upload-input']", pin.imagePath)
            
            self._waitForSaving()

            if pin.title:
                self.sendKeys("//input[@id='storyboard-selector-title']", pin.title)
            if pin.link:
                self.sendKeys("//input[@id='WebsiteField']", pin.link)
            if pin.description:
                self.sendKeys("//div[contains(@class, 'public-DraftEditor-content')][@role='combobox']", pin.description)
            if pin.pinboard:
                try:
                    self.click("//button[@data-test-id='board-dropdown-select-button']")
                    self.sendKeys("//input[@id='pickerSearchField']", pin.pinboard.lower())
                    self.click("//div[%s]/.."%(self.ignoreCaseEqualsXPath("@data-test-id", 'board-row-' + pin.pinboard)))
                except:
                    raise Exception("Pinboard name is invalid or not found.")

            self.driver.find_elements(By.XPATH, "//div[@aria-disabled='false'][@role='button']") \
                .pop() \
                .click()

            sleep(2)

            self._setCheckbox("CommentSwitch", pin.allowComment)
            self._setCheckbox("stelaSwitch", pin.showSimilarProduct)

            sleep(2)

            self._waitForSaving()
            self.click("//div[@data-test-id='storyboard-creation-nav-done']/button")
            self.waitVisible("//div[@role='status']")
        except ValueError as e:
            raise Exception(str(e))

    def _waitForSaving(self):
        self.waitVisible("//div[@data-test-id='saving-status-saved']", 60 * 10)

    def _setCheckbox(self, id: str, value: bool):
        self.driver.execute_script((
            f"""
            const need_checked = {json.dumps(value)};
            const el = document.querySelector(\"input[id='{id}']\");
            if (el && ((el.checked && !need_checked) || (!el.checked && need_checked))) el.click();
            """
        ).strip())