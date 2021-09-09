import unittest
from secrets import ACCOUNT
from time import sleep

import HtmlTestRunner

from utils import ANDROID_SETTING_CAPS, CS_APP_CAPS, GOOGLE_STORE_CAPS
from users import User, CSUser
from xpaths import ADVENTUREPAGE, ANDROID_SETTING, HOMEPAGE, SIGNUPPAGE


class TestGeneralSignin(unittest.TestCase):
    def setUp(self):
        self.user = User(CS_APP_CAPS)
        self.cs_user = CSUser(self.user)

    def tearDown(self):
        self.user.driver.quit()

    def test_sign_up(self):
        self.cs_user.sign_up(
            lastname="test12",
            firstname="test",
            email="test12@test.com",
            password="00000000",
            password_confirmed="00000000",
        )
        sign_up_finish = self.cs_user.element_selector(
            SIGNUPPAGE["interested_theme_finish"]
        )
        self.assertEqual(sign_up_finish.get_attribute("clickable"), "true")

    def test_sign_in(self):
        self.cs_user.sign_in("test2@test.com", "00000000")
        account_page = self.cs_user.element_selector(HOMEPAGE["account"])
        self.assertEqual(account_page.get_attribute("clickable"), "true")


class TestThirdPartySignin(unittest.TestCase):
    def setUp(self):
        self.user = User(CS_APP_CAPS)
        self.cs_user = CSUser(self.user)

    def tearDown(self):
        self.user.driver.quit()

    def test_1_clear_storage(self):
        self.user = User(ANDROID_SETTING_CAPS)
        self.cs_user = CSUser(self.user)
        self.cs_user.clear_chrome_storage()
        self.user = User(GOOGLE_STORE_CAPS)
        self.cs_user = CSUser(self.user)
        self.cs_user.clear_google_storage()

    def test_facebook_sign_in(self):
        self.cs_user.facebook_sign_in(
            email=ACCOUNT["facebook_email"], password=ACCOUNT["facebook_password"]
        )
        account_page = self.cs_user.element_selector(HOMEPAGE["account"])
        self.assertEqual(account_page.get_attribute("clickable"), "true")

    def test_line_sign_in(self):
        self.cs_user.line_sign_in(
            email=ACCOUNT["line_email"], password=ACCOUNT["line_password"]
        )
        account_page = self.cs_user.element_selector(HOMEPAGE["account"])
        self.assertEqual(account_page.get_attribute("clickable"), "true")

    def test_google_sign_in(self):
        self.cs_user.google_sign_in(
            email=ACCOUNT["google_email"], password=ACCOUNT["google_password"]
        )
        account_page = self.cs_user.element_selector(HOMEPAGE["account"])
        self.assertEqual(account_page.get_attribute("clickable"), "true")


class TestAdventure(unittest.TestCase):
    def setUp(self):
        self.user = User(CS_APP_CAPS)
        self.cs_user = CSUser(self.user)

    def test_early_bird_list(self):
        self.cs_user.early_bird_list()
        early_bird_title = self.cs_user.element_selector("+android.widget.TextView+早鳥首賣")
        self.assertEqual(early_bird_title.get_attribute("text"), "早鳥首賣")

    def test_early_bird_product_page(self):
        self.cs_user.early_bird_prudoct_page()


if __name__ == "__main__":
    test_runner = HtmlTestRunner.HTMLTestRunner(
        output="./report",
        open_in_browser=False,
        report_title="CSApp functonal test report",
    )
    unittest.main(testRunner=test_runner)
