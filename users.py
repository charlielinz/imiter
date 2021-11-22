import string
import random
from time import sleep
from appium import webdriver

from selenium.common.exceptions import NoSuchElementException

from xpaths import (
    ACCOUNTPAGE,
    DISCOVERYPAGE,
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
                f'.className({class_name}).text("{text}")'
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
            return self.user.driver.find_element_by_android_uiautomator(
                f'.className({class_name}).text("{text}")'
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

    def get_random_string(self, num):
        letters = string.ascii_lowercase
        random_string = "".join(random.choice(letters) for num in range(num))
        return random_string

    def get_random_num(self):
        random_num = random.randint(1000, 9999)
        return random_num


class CSUser(User):
    """
    this is a CS app user
    """

    def __init__(self, user):
        self.user = user

    def sign_up(self, **user):
        self.element_selector("+android.widget.TextView+帳戶").click()
        self.element_selector("+android.widget.TextView+註冊").click()
        form_fields = self.elements_selector("#android.widget.EditText")
        last_name_field, first_name_field, email_field, password_field, password_confirmed_field = form_fields
        last_name_field.send_keys(user["last_name"])
        first_name_field.send_keys(user["first_name"])
        email_field.send_keys(user["email"])
        password_field.send_keys(user["password"])
        password_confirmed_field.send_keys(user["password_confirmed"])
        self.element_selector(SIGNUPPAGE["sign_up"]).click()

    def sign_in(self, **user):
        self.element_selector("+android.widget.TextView+帳戶").click()
        self.element_selector("+android.widget.TextView+登入").click()
        form_fields = self.elements_selector("#android.widget.EditText")
        email_field, password_field = form_fields
        if user["email"]:
            email_field.send_keys(user["email"])
        if user["password"]:
            password_field.send_keys(user["password"])
        self.element_selector(SIGNINPAGE["sign_in"]).click()

    def clear_chrome_storage(self):
        self.element_selector("+android.widget.TextView+Apps & notifications").click()
        self.element_selector("@com.android.settings:id/header_details").click()
        sleep(1)
        app_list = self.elements_selector("@android:id/title")
        for app in app_list:
            app_name = app.get_attribute("text")
            if "Chrome" in str(app_name):
                app.click()
                sleep(1)
                self.element_selector(
                    "+android.widget.TextView+Storage & cache"
                ).click()
                self.element_selector("+android.widget.Button+Clear storage").click()
                self.element_selector("+android.widget.Button+CLEAR ALL DATA").click()
                self.element_selector("+android.widget.Button+OK").click()
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
        self.element_selector("+android.widget.TextView+帳戶").click()
        self.element_selector(ACCOUNTPAGE["sign_in_facebook"]).click()
        try:
            self.element_selector("@com.android.chrome:id/terms_accept").click()
            self.element_selector("@com.android.chrome:id/negative_button").click()
        except NoSuchElementException:
            pass
        try:
            self.element_selector("//android.view.View[1]/android.view.View/android.view.View/android.widget.EditText").send_keys(email)
        except NoSuchElementException:
            self.element_selector("+android.widget.Button+繼續").click()
            return
        self.element_selector("//android.view.View[2]/android.view.View[1]/android.view.View/android.widget.EditText").send_keys(password)
        self.element_selector("+android.widget.Button+Log In").click()
        try:
            self.element_selector("+android.widget.TextView+帳戶")
        except NoSuchElementException:
            self.element_selector("+android.widget.Button+繼續").click()

    def line_sign_in(self, email, password):
        self.element_selector("+android.widget.TextView+帳戶").click()
        self.element_selector(ACCOUNTPAGE["sign_in_line"]).click()
        try:
            self.element_selector("@com.android.chrome:id/terms_accept").click()
            self.element_selector("@com.android.chrome:id/negative_button").click()
        except NoSuchElementException:
            pass
        self.element_selector(LINE_SIGNIN["email"]).send_keys(email)
        self.element_selector(LINE_SIGNIN["password"]).send_keys(password)
        self.element_selector(LINE_SIGNIN["enter"]).click()
        self.element_selector(LINE_SIGNIN["allow_access"]).click()

    def google_sign_in(self, email, password):
        self.element_selector("+android.widget.TextView+帳戶").click()
        self.element_selector(ACCOUNTPAGE["sign_in_google"]).click()
        try:
            self.element_selector("//android.view.View[1]/android.widget.EditText").send_keys(email)
            self.element_selector("+android.widget.Button+Next").click()
            sleep(2)
            self.element_selector("//android.view.View[1]/android.widget.EditText").send_keys(password)
            self.element_selector("//android.view.View[1]/android.view.View[4]/android.view.View").click()
            self.element_selector("+android.widget.Button+I agree").click()
            switch = self.element_selector("@com.google.android.gms:id/sud_items_switch")
            if switch.text == "ON":
                switch.click()
            else:
                pass
            self.element_selector("+android.widget.Button+ACCEPT").click()
        except NoSuchElementException:
            account_list = self.elements_selector(
                "@com.google.android.gms:id/container"
            )
            account_index = random.randint(0, len(account_list) - 2)
            account_list[account_index].click()
            pass

    def edit_user_name(self, **user):
        last_name = user["last_name"]
        first_name = user["first_name"]
        self.element_selector("+android.widget.TextView+帳戶").click()
        self.element_selector("+android.widget.TextView+帳號管理").click()
        form_fields = self.elements_selector("#android.widget.EditText")
        last_name_field = form_fields[0]
        first_name_field = form_fields[1]
        if last_name:
            last_name_field.clear()
            last_name_field.send_keys(last_name)
        if first_name:
            first_name_field.clear()
            first_name_field.send_keys(first_name)
        self.element_selector("+android.widget.TextView+更新資料").click()

    """ waiting for a element id """
    # def edit_user_gender(self):
    #     self.element_selector("+android.widget.TextView+帳戶").click()
    #     self.element_selector("+android.widget.TextView+帳號管理").click()

    def edit_traced_themes(self):
        self.element_selector("+android.widget.TextView+帳戶").click()
        self.element_selector("+android.widget.TextView+追蹤主題").click()
        themes = [
            "日系質感",
            "歐美精選",
            "韓流生活",
            "全台獨家",
            "環保風尚",
            "硬派軍風",
            "咖啡時光",
            "居家收納",
            "科技新品",
            "露營野餐",
            "登山冒險",
            "攝影美學",
            "品酒精釀",
            "飲茶雅趣",
            "親子同樂",
        ]
        traced_theme_num = random.randint(1, 15)
        for num in range(traced_theme_num):
            theme_index = random.randint(0, 14)
            self.element_selector(
                f"+android.widget.TextView+{themes[theme_index]}"
            ).click()
        self.element_selector("+android.widget.TextView+確認").click()

    """ unknown error: pop up sign-in page after click into shipping address page"""
    # def add_new_shipping_address(self):
    #     self.element_selector("+android.widget.TextView+帳戶").click()
    #     self.element_selector("+android.widget.TextView+常用收件地址").click()
    #     self.element_selector("+android.widget.TextView++ 新增收件地址").click()

    def change_password(self, email):
        self.element_selector("+android.widget.TextView+帳戶").click()
        self.element_selector("+android.widget.TextView+變更密碼").click()
        self.element_selector("#android.widget.EditText").send_keys(email)
        self.element_selector("+android.widget.TextView+送出").click()

    def change_country(self):
        country = {"台灣", "香港", "馬來西亞", "新加玻"}
        self.element_selector("+android.widget.TextView+帳戶").click()
        self.element_selector("+android.widget.TextView+設定").click()
        self.element_selector("+android.widget.TextView+所在國家").click()
        self.element_selector("+android.widget.TextView+台灣").click()
        self.element_selector("+android.widget.TextView+確認").click()
        self.element_selector(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.ImageView"
        ).click()
        self.element_selector("+android.widget.TextView+探索")
        self.element_selector("+android.widget.TextView+看更多熱銷排行").click()
