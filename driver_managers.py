from appium import webdriver


class DriverManager:
    def __init__(self, desired_cap):
        self.desired_cap = desired_cap
        self._remote()

    def _remote(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_cap)
        self.driver.implicitly_wait(10)
