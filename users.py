from time import sleep
from appium import webdriver

from selenium.common.exceptions import NoSuchElementException

from xpaths import (
    ACCOUNTPAGE,
    ADVENTUREPAGE,
    ANDROID_SETTING,
    FACEBOOK_SIGNIN,
    GOOGLE_SIGNIN,
    HOMEPAGE,
    LINE_SIGNIN,
    SIGNINPAGE,
    SIGNUPPAGE,
)


class DriverManager:
    def __init__(self, desired_cap):
        self.desired_cap = desired_cap
        self._remote()

    def _remote(self):
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.desired_cap)
        self.driver.implicitly_wait(10)


class User:
    def element_selector(self, string):
        pass

    def _find_element_by_id(self, id_):
        return self.manager.driver.find_element_by_id(id_)

    def _find_element_by_id_and_click(self, id_):
        self.manager.driver.find_element_by_id(id_).click()

    def _find_element_by_id_and_send_keys(self, id_, key):
        self.manager.driver.find_element_by_id(id_).send_keys(key)

    def _find_element_by_xpath(self, xpath):
        return self.manager.driver.find_element_by_xpath(xpath)

    def _find_element_by_xpath_and_click(self, xpath):
        self.manager.driver.find_element_by_xpath(xpath).click()

    def _find_element_by_xpath_and_send_keys(self, xpath, key):
        self.manager.driver.find_element_by_xpath(xpath).send_keys(key)

    def _find_element_by_classname(self, className):
        return self.manager.driver.find_element_by_class_name(className)

    def _find_element_by_class_and_text(self, className, text):
        return self.manager.driver.find_element_by_android_uiautomator(
            f'.className("{className}").text("{text}")'
        )

    def _find_element_by_class_and_text_and_click(self, className, text):
        self._find_element_by_class_and_text(className, text).click()

    def _find_elements_by_id(self, id_):
        return self.manager.driver.find_elements_by_id(id_)

    def _find_elements_by_classname(self, className):
        return self.manager.driver.find_elements_by_class_name(className)

    def _swipe_up(self):
        screen_width = self.manager.driver.get_window_size()["width"]
        screen_height = self.manager.driver.get_window_size()["height"]
        start_point = [screen_width * 0.5, screen_height * 0.75]
        end_point = [screen_width * 0.5, screen_height * 0.25]
        self.manager.driver.swipe(
            start_point[0], start_point[1], end_point[0], end_point[1]
        )

    def _swipe_down(self):
        screen_width = self.manager.driver.get_window_size()["width"]
        screen_height = self.manager.driver.get_window_size()["height"]
        start_point = [screen_width * 0.5, screen_height * 0.25]
        end_point = [screen_width * 0.5, screen_height * 0.75]
        self.manager.driver.swipe(
            start_point[0], start_point[1], end_point[0], end_point[1]
        )

    def _swipe_left(self):
        screen_width = self.manager.driver.get_window_size()["width"]
        screen_height = self.manager.driver.get_window_size()["height"]
        start_point = [screen_width * 0.75, screen_height * 0.5]
        end_point = [screen_width * 0.25, screen_height * 0.5]
        self.manager.driver.swipe(
            start_point[0], start_point[1], end_point[0], end_point[1]
        )

    def _swipe_right(self):
        screen_width = self.manager.driver.get_window_size()["width"]
        screen_height = self.manager.driver.get_window_size()["height"]
        start_point = [screen_width * 0.25, screen_height * 0.5]
        end_point = [screen_width * 0.75, screen_height * 0.5]
        self.manager.driver.swipe(
            start_point[0], start_point[1], end_point[0], end_point[1]
        )


class CSUser(User):
    def __init__(self, manager):
        self.manager = manager

    def adventure_page(self):
        self._find_element_by_xpath_and_click(HOMEPAGE["adventure"])

    def search_page(self):
        self._find_element_by_xpath_and_click(HOMEPAGE["search"])

    def favorite_page(self):
        self._find_element_by_xpath_and_click(HOMEPAGE["favorite"])

    def account_page(self):
        self._find_element_by_xpath_and_click(HOMEPAGE["account"])

    def early_bird_list(self):
        while True:
            try:
                self._find_element_by_class_and_text_and_click(
                    className="android.widget.TextView", text="看全部早鳥首賣"
                )
                break
            except NoSuchElementException:
                self._swipe_up()

    def early_bird_prudoct_page(self):
        self.early_bird_list()
        for looking_early_product in range(20):
            button_list = self._find_elements_by_classname("android.widget.TextView")
            for button in button_list:
                if "金額" in str(button.get_attribute("text")):
                    button.click()

    def sign_up_page(self):
        self.account_page()
        self._find_element_by_xpath_and_click(ACCOUNTPAGE["sign_up_page"])

    def sign_in_page(self):
        self.account_page()
        self._find_element_by_xpath_and_click(ACCOUNTPAGE["sign_in_normal"])

    def sign_up(self, lastname, firstname, email, password, password_confirmed):
        self.sign_up_page()
        self._find_element_by_xpath_and_send_keys(SIGNUPPAGE["last_name"], lastname)
        self._find_element_by_xpath_and_send_keys(SIGNUPPAGE["first_name"], firstname)
        self._find_element_by_xpath_and_send_keys(SIGNUPPAGE["email"], email)
        self._find_element_by_xpath_and_send_keys(SIGNUPPAGE["password"], password)
        self._find_element_by_xpath_and_send_keys(
            SIGNUPPAGE["password_confirmed"], password_confirmed
        )
        self._find_element_by_xpath_and_click(SIGNUPPAGE["sign_up"])

    def sign_in(self, email, password):
        self.sign_in_page()
        self._find_element_by_xpath_and_send_keys(SIGNINPAGE["email"], email)
        self._find_element_by_xpath_and_send_keys(SIGNINPAGE["password"], password)
        self._find_element_by_xpath_and_click(SIGNINPAGE["sign_in"])

    def clear_chrome_storage(self):
        self._find_element_by_xpath_and_click(ANDROID_SETTING["app & notifications"])
        self._find_element_by_id_and_click("com.android.settings:id/header_details")
        sleep(1)
        app_list = self._find_elements_by_id("android:id/title")
        for app in app_list:
            app_name = app.get_attribute("text")
            if "Chrome" in str(app_name):
                app.click()
                sleep(1)
                self._find_element_by_xpath_and_click(
                    ANDROID_SETTING["Storage & Cache"]
                )
                self._find_element_by_xpath_and_click(ANDROID_SETTING["Clear Storage"])
                self._find_element_by_xpath_and_click(
                    ANDROID_SETTING["Google Chrome Clear All Data"]
                )
                self._find_element_by_xpath_and_click(
                    ANDROID_SETTING["Google Chrome OK"]
                )
                break

    def clear_google_storage(self):
        try:
            storepage_button_list = self._find_elements_by_id(
                "com.android.vending:id/0_resource_name_obfuscated"
            )
            for button in storepage_button_list:
                button_content = button.get_attribute("content-desc")
                if "Open account menu" in str(button_content):
                    button.click()
                    break
            sleep(1)
            account_button_list = self._find_elements_by_id(
                "com.android.vending:id/0_resource_name_obfuscated"
            )
            for button in account_button_list:
                button_text = button.get_attribute("text")
                if "Manage accounts on this device" in str(button_text):
                    button.click()
                    break
            sleep(3)
            device_account_list = self._find_elements_by_id("android:id/summary")
            for account in device_account_list:
                if (
                    account.get_attribute("text")
                    == "Let apps refresh data automatically"
                ):
                    break
                else:
                    account.click()
                    sleep(1)
                    self._find_element_by_id_and_click("com.android.settings:id/button")
                    self._find_element_by_id_and_click("android:id/button1")
        except Exception:
            pass

    def facebook_sign_in(self, email, password):
        self.account_page()
        self._find_element_by_xpath_and_click(ACCOUNTPAGE["sign_in_facebook"])
        sleep(2)
        try:
            self._find_element_by_id_and_click("com.android.chrome:id/terms_accept")
            self._find_element_by_id_and_click("com.android.chrome:id/negative_button")
        except NoSuchElementException:
            pass
        sleep(2)
        try:
            self._find_element_by_xpath_and_send_keys(FACEBOOK_SIGNIN["email"], email)
        except NoSuchElementException:
            self._find_element_by_xpath_and_click(FACEBOOK_SIGNIN["continue"])
            return
        self._find_element_by_xpath_and_send_keys(FACEBOOK_SIGNIN["password"], password)
        self._find_element_by_xpath_and_click(FACEBOOK_SIGNIN["enter"])
        sleep(2)
        try:
            self._find_element_by_xpath(HOMEPAGE["account"])
        except NoSuchElementException:
            self._find_element_by_xpath_and_click(FACEBOOK_SIGNIN["continue"])

    def line_sign_in(self, email, password):
        self.account_page()
        self._find_element_by_xpath_and_click(ACCOUNTPAGE["sign_in_line"])
        self._find_element_by_xpath_and_send_keys(LINE_SIGNIN["email"], email)
        self._find_element_by_xpath_and_send_keys(LINE_SIGNIN["password"], password)
        self._find_element_by_xpath_and_click(LINE_SIGNIN["enter"])
        sleep(1)
        self._find_element_by_xpath_and_click(LINE_SIGNIN["allow_access"])

    def google_sign_in(self, email, password):
        self.account_page()
        self._find_element_by_xpath_and_click(ACCOUNTPAGE["sign_in_google"])
        sleep(3)
        try:
            self._find_element_by_xpath_and_send_keys(GOOGLE_SIGNIN["email"], email)
            self._find_element_by_xpath_and_click(GOOGLE_SIGNIN["email_next"])
            sleep(2)
            self._find_element_by_xpath_and_send_keys(
                GOOGLE_SIGNIN["password"], password
            )
            self._find_element_by_xpath_and_click(GOOGLE_SIGNIN["password_next"])
            sleep(3)
            self._find_element_by_xpath_and_click(GOOGLE_SIGNIN["agree_button"])
            sleep(3)
            switch = self._find_element_by_xpath(GOOGLE_SIGNIN["switch"])
            if switch.text == "ON":
                switch.click()
                sleep(2)
            else:
                pass
            self._find_element_by_xpath_and_click(GOOGLE_SIGNIN["accept"])
        except NoSuchElementException:
            self._find_element_by_xpath_and_click(GOOGLE_SIGNIN["signed_account"])
            pass
