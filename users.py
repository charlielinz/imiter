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


class User:
    """
    this is a mobile user
    """

    def __init__(self, desired_cap):
        self.desired_cap = desired_cap
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.desired_cap)
        self.driver.implicitly_wait(10)

    def element_selector(self, string):
        """
        customized element selector- select element according to the prefix of string
        the given string needs to start with a prefix, the rules are below:
            "@" = by id
            "#" = by class
            "/" = by xpath
            "+" = by class & text
        """
        prefix = string[:1]
        if prefix == "@":
            id_ = string.replace("@", "", 1)
            return self.user.driver.find_element_by_id(id_)
        if prefix == "#":
            class_ = string.replace("#", "", 1)
            return self.user.driver.find_element_by_class_name(class_)
        if prefix == "/":
            xpath = string
            return self.user.driver.find_element_by_xpath(xpath)
        if prefix == "+":
            original_string = string.replace("+", "", 1)
            attribute_list = original_string.split("+")
            class_name = attribute_list[0]
            text = attribute_list[1]
            return self.user.driver.find_element_by_android_uiautomator(
                f".className('{class_name}').text('{text}')"
            )
        raise ValueError("the string doesn't include a prefix")

    def elements_selector(self, string):
        """
        customized element selector- select elements according to the prefix of string
        the given string needs to start with a prefix, the rules are below:
            "@" = by id
            "#" = by class
            "/" = by xpath
            "+" = by class & text
        """
        prefix = string[:1]
        if prefix == "@":
            id_ = string.replace("@", "", 1)
            return self.user.driver.find_elements_by_id(id_)
        if prefix == "#":
            class_ = string.replace("#", "", 1)
            return self.user.driver.find_elements_by_class_name(class_)
        if prefix == "/":
            xpath = string
            return self.user.driver.find_elements_by_xpath(xpath)
        if prefix == "+":
            original_string = string.replace("+", "", 1)
            attribute_list = original_string.split("+")
            class_name = attribute_list[0]
            text = attribute_list[1]
            return self.user.driver.find_elements_by_android_uiautomator(
                f".className('{class_name}').text('{text}')"
            )
        raise ValueError("the string doesn't include a prefix")

    def _swipe_up(self):
        screen_width = self.user.driver.get_window_size()["width"]
        screen_height = self.user.driver.get_window_size()["height"]
        start_point = [screen_width * 0.5, screen_height * 0.75]
        end_point = [screen_width * 0.5, screen_height * 0.25]
        self.user.driver.swipe(
            start_point[0], start_point[1], end_point[0], end_point[1]
        )

    def _swipe_down(self):
        screen_width = self.user.driver.get_window_size()["width"]
        screen_height = self.user.driver.get_window_size()["height"]
        start_point = [screen_width * 0.5, screen_height * 0.25]
        end_point = [screen_width * 0.5, screen_height * 0.75]
        self.user.driver.swipe(
            start_point[0], start_point[1], end_point[0], end_point[1]
        )

    def _swipe_left(self):
        screen_width = self.user.driver.get_window_size()["width"]
        screen_height = self.user.driver.get_window_size()["height"]
        start_point = [screen_width * 0.75, screen_height * 0.5]
        end_point = [screen_width * 0.25, screen_height * 0.5]
        self.user.driver.swipe(
            start_point[0], start_point[1], end_point[0], end_point[1]
        )

    def _swipe_right(self):
        screen_width = self.user.driver.get_window_size()["width"]
        screen_height = self.user.driver.get_window_size()["height"]
        start_point = [screen_width * 0.25, screen_height * 0.5]
        end_point = [screen_width * 0.75, screen_height * 0.5]
        self.user.driver.swipe(
            start_point[0], start_point[1], end_point[0], end_point[1]
        )


class CSUser(User):
    """
    this is a CS app user
    """

    def __init__(self, user):
        self.user = user

    def adventure_page(self):
        self.element_selector(HOMEPAGE["adventure"]).click()

    def search_page(self):
        self.element_selector(HOMEPAGE["search"]).click()

    def favorite_page(self):
        self.element_selector(HOMEPAGE["favorite"]).click()

    def account_page(self):
        self.element_selector(HOMEPAGE["account"]).click()

    def early_bird_list(self):
        while True:
            try:
                self.element_selector("+android.widget.TextView+看全部早鳥首賣")
                break
            except NoSuchElementException:
                self._swipe_up()

    # def early_bird_prudoct_page(self):
    #     self.early_bird_list()
    #     for looking_early_product in range(20):
    #         button_list = self._find_elements_by_classname("android.widget.TextView")
    #         for button in button_list:
    #             if "金額" in str(button.get_attribute("text")):
    #                 button.click()

    def sign_up_page(self):
        self.account_page()
        self.element_selector(ACCOUNTPAGE["sign_up_page"]).click()

    def sign_in_page(self):
        self.account_page()
        self.element_selector(ACCOUNTPAGE["sign_in_normal"]).click()

    def sign_up(self, lastname, firstname, email, password, password_confirmed):
        self.sign_up_page()
        self.element_selector(SIGNUPPAGE["last_name"]).send_keys(lastname)
        self.element_selector(SIGNUPPAGE["first_name"]).send_keys(firstname)
        self.element_selector(SIGNUPPAGE["email"]).send_keys(email)
        self.element_selector(SIGNUPPAGE["password"]).send_keys(password)
        self.element_selector(SIGNUPPAGE["password_confirmed"]).send_keys(
            password_confirmed
        )
        self.element_selector(SIGNUPPAGE["sign_up"]).click()

    def sign_in(self, email, password):
        self.sign_in_page()
        self.element_selector(SIGNINPAGE["email"]).send_keys(email)
        self.element_selector(SIGNINPAGE["password"]).send_keys(password)
        self.element_selector(SIGNINPAGE["sign_in"]).click()

    def clear_chrome_storage(self):
        self.element_selector(ANDROID_SETTING["app & notifications"]).click()
        self.element_selector("@com.android.settings:id/header_details").click()
        sleep(1)
        app_list = self.elements_selector("@android:id/title")
        for app in app_list:
            app_name = app.get_attribute("text")
            if "Chrome" in str(app_name):
                app.click()
                sleep(1)
                self.element_selector(ANDROID_SETTING["Storage & Cache"]).click()
                self.element_selector(ANDROID_SETTING["Clear Storage"]).click()
                self.element_selector(
                    ANDROID_SETTING["Google Chrome Clear All Data"]
                ).click()
                self.element_selector(ANDROID_SETTING["Google Chrome OK"]).click()
                break

    def clear_google_storage(self):
        try:
            storepage_button_list = self.elements_selector(
                "@com.android.vending:id/0_resource_name_obfuscated"
            )
            for button in storepage_button_list:
                button_content = button.get_attribute("content-desc")
                if "Open account menu" in str(button_content):
                    button.click()
                    break
            sleep(1)
            account_button_list = self.elements_selector(
                "@com.android.vending:id/0_resource_name_obfuscated"
            )
            for button in account_button_list:
                button_text = button.get_attribute("text")
                if "Manage accounts on this device" in str(button_text):
                    button.click()
                    break
            sleep(3)
            device_account_list = self.elements_selector("@android:id/summary")
            for account in device_account_list:
                if (
                    account.get_attribute("text")
                    == "Let apps refresh data automatically"
                ):
                    break
                else:
                    account.click()
                    sleep(1)
                    self.element_selector("@com.android.settings:id/button").click()
                    self.element_selector("@android:id/button1").click()
        except Exception:
            pass

    def facebook_sign_in(self, email, password):
        self.account_page()
        self.element_selector(ACCOUNTPAGE["sign_in_facebook"]).click()
        sleep(2)
        try:
            self.element_selector("com.android.chrome:id/terms_accept").click()
            self.element_selector("com.android.chrome:id/negative_button").click()
        except NoSuchElementException:
            pass
        sleep(2)
        try:
            self.element_selector(FACEBOOK_SIGNIN["email"]).send_keys(email)
        except NoSuchElementException:
            self.element_selector(FACEBOOK_SIGNIN["continue"]).click()
            return
        self.element_selector(FACEBOOK_SIGNIN["password"]).send_keys(password)
        self.element_selector(FACEBOOK_SIGNIN["enter"]).click()
        sleep(2)
        try:
            self.element_selector(HOMEPAGE["account"])
        except NoSuchElementException:
            self.element_selector(FACEBOOK_SIGNIN["continue"]).click()

    def line_sign_in(self, email, password):
        self.account_page()
        self.element_selector(ACCOUNTPAGE["sign_in_line"]).click()
        sleep(2)
        try:
            self.element_selector("com.android.chrome:id/terms_accept").click()
            self.element_selector("com.android.chrome:id/negative_button").click()
        except NoSuchElementException:
            pass
        sleep(2)
        self.element_selector(LINE_SIGNIN["email"]).send_keys(email)
        self.element_selector(LINE_SIGNIN["password"]).send_keys(password)
        self.element_selector(LINE_SIGNIN["enter"]).click()
        sleep(1)
        self.element_selector(LINE_SIGNIN["allow_access"]).click()

    def google_sign_in(self, email, password):
        self.account_page()
        self.element_selector(ACCOUNTPAGE["sign_in_google"]).click()
        sleep(3)
        try:
            self.element_selector(GOOGLE_SIGNIN["email"]).send_keys(email)
            self.element_selector(GOOGLE_SIGNIN["email_next"]).click()
            sleep(2)
            self.element_selector(GOOGLE_SIGNIN["password"]).send_keys(password)
            self.element_selector(GOOGLE_SIGNIN["password_next"]).click()
            sleep(3)
            self.element_selector(GOOGLE_SIGNIN["agree_button"]).click()
            sleep(3)
            switch = self.element_selector(GOOGLE_SIGNIN["switch"])
            if switch.text == "ON":
                switch.click()
                sleep(2)
            else:
                pass
            self.element_selector(GOOGLE_SIGNIN["accept"]).click()
        except NoSuchElementException:
            self.element_selector(GOOGLE_SIGNIN["signed_account"]).click()
            pass
