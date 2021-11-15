import unittest
from secrets import ACCOUNT
from time import sleep

import HtmlTestRunner

from utils import ANDROID_SETTING_CAPS, CS_APP_CAPS, GOOGLE_STORE_CAPS
from users import User, CSUser
from xpaths import DISCOVERYPAGE, ANDROID_SETTING, HOMEPAGE, SIGNUPPAGE


class TestGeneralSignin(unittest.TestCase):
    def setUp(self):
        self.user = User(CS_APP_CAPS)
        self.cs_user = CSUser(self.user)

    def tearDown(self):
        self.user.driver.quit()

    def test_sign_up_with_all_fields_filled(self):
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
        self.cs_user.sign_in(email="test2@test.com", password="00000000")
        account_page = self.cs_user.element_selector(HOMEPAGE["account"])
        self.assertEqual(account_page.get_attribute("clickable"), "true")

    def test_sign_in_with_empty_email(self):
        self.cs_user.sign_in(email="", password="00000000")
        email_field = self.cs_user.element_selector(
            "+android.widget.TextView+請填寫 email"
        )
        self.assertEqual(email_field.get_attribute("displayed"), "true")

    def test_sign_in_with_empty_password(self):
        self.cs_user.sign_in(email="test2@test.com", password="")
        password_field = self.cs_user.element_selector("+android.widget.TextView+請輸入密碼")
        self.assertEqual(password_field.get_attribute("displayed"), "true")

    def test_sign_in_with_empty_email_and_password(self):
        self.cs_user.sign_in(email="", password="")
        email_field = self.cs_user.element_selector(
            "+android.widget.TextView+請填寫 email"
        )
        password_field = self.cs_user.element_selector("+android.widget.TextView+請輸入密碼")
        self.assertEqual(email_field.get_attribute("displayed"), "true")
        self.assertEqual(password_field.get_attribute("displayed"), "true")

    def test_sign_in_with_invalid_syntax_of_email(self):
        bad_email = self.cs_user.get_random_string()
        self.cs_user.sign_in(email=bad_email, password="00000000")
        email_field = self.cs_user.element_selector(
            "+android.widget.TextView+email 格式錯誤"
        )
        self.assertEqual(email_field.get_attribute("displayed"), "true")

    def test_sign_in_with_invalid_syntax_of_password(self):
        bad_password = self.cs_user.get_random_num()
        self.cs_user.sign_in(email="test2@test.com", password=bad_password)
        password_field = self.cs_user.element_selector(
            "+android.widget.TextView+密碼長度必須大於8碼"
        )
        self.assertEqual(password_field.get_attribute("displayed"), "true")

    def test_sign_in_with_invalid_syntax_of_email_and_password(self):
        bad_email = self.cs_user.get_random_string()
        bad_password = self.cs_user.get_random_num()
        self.cs_user.sign_in(email=bad_email, password=bad_password)
        email_field = self.cs_user.element_selector(
            "+android.widget.TextView+email 格式錯誤"
        )
        password_field = self.cs_user.element_selector(
            "+android.widget.TextView+密碼長度必須大於8碼"
        )
        self.assertEqual(email_field.get_attribute("displayed"), "true")
        self.assertEqual(password_field.get_attribute("displayed"), "true")

    def test_sign_in_with_wrong_email(self):
        wrong_email = self.cs_user.get_random_string() + "@gmail.com"
        self.cs_user.sign_in(email=wrong_email, password="00000000")
        alert_field = self.cs_user.element_selector("@android:id/message")
        self.assertEqual(alert_field.get_attribute("text"), "請輸入正確的 Email 及密碼")

    def test_sign_in_with_wrong_password(self):
        wrong_password = "0000000000"
        self.cs_user.sign_in(email="test2@test.com", password=wrong_password)
        alert_field = self.cs_user.element_selector("@android:id/message")
        self.assertEqual(alert_field.get_attribute("text"), "請輸入正確的 Email 及密碼")

    def test_sign_in_with_wrong_email_and_password(self):
        wrong_email = self.cs_user.get_random_string() + "@gmail.com"
        wrong_password = "0000000000"
        self.cs_user.sign_in(email=wrong_email, password=wrong_password)
        alert_field = self.cs_user.element_selector("@android:id/message")
        self.assertEqual(alert_field.get_attribute("text"), "請輸入正確的 Email 及密碼")


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


class TestAccountManaging(unittestt.TestCase):
    def setUp(self):
        self.user = User(CS_APP_CAPS)
        self.cs_user = CSUser(self.user)
        self.cs_user.google_sign_in(
            email=ACCOUNT["google_email"], password=ACCOUNT["google_password"]
        )

    def tearDown(self):
        self.user.driver.quit()


if __name__ == "__main__":
    test_runner = HtmlTestRunner.HTMLTestRunner(
        output="./report",
        open_in_browser=False,
        report_title="citiesocial app test report",
    )
    unittest.main(testRunner=test_runner)
