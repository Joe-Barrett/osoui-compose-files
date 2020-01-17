import unittest
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class WebjiveE2EPubSubTest(unittest.TestCase):
    polling_period = 0.5
    USERNAME = 'username'
    PASSWORD = 'password'
    HOST = 'host'

    def setUp(self):
        print("\nRunning WebJive Suite Pub/Sub Test... \n")
        self.driver = self.create_driver()

        print("Loading page " + self.HOST + "... ", end=" ")
        self.driver.get(self.HOST)
        expected_title = "WebJive"
        page_load_error_msg = "FAILED. The Webjive page was not loaded correctly. Page title should contain '" \
                              + expected_title + "' but title is '" + self.driver.title + "'"
        if expected_title not in self.driver.title:
            self.fail(msg=page_load_error_msg)
        print("SUCCESS")

        self.driver.find_element(By.LINK_TEXT, 'Dashboards').click()
        print("Logging in... ", end=" ")
        if not self.login(self.driver, self.USERNAME, self.PASSWORD):
            msg = "FAILED. Could not log in"
            self.fail(msg=msg)
        print("SUCCESS")

    def tearDown(self):
        self.driver.close()

    # What was the agreed naming when talking about the whole system (webjive+tangogql)? ***
    def test_webjive_pubsub(self):
        print("Opening dashboard... ", end=" ")
        if not self.open_dashboard(self.driver, "PollingTestDashboard"):
            msg = "FAILED. Could not open dashboard PollingTestDashboard"
            self.fail(msg=msg)
        print("SUCCESS")

        self.driver.find_element_by_css_selector(".form-inline > button").click()

        print("Checking attribute... ")
        try:
            time.sleep(0.5)
            wait = WebDriverWait(self.driver, 1)
            randomattr1 = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[@id='AttributeDisplay']"))).text
        except TimeoutException:
            msg = "FAILED.  Could not find webjivetestdevice"
            self.fail(msg=msg)

        print(randomattr1)

        time.sleep(self.polling_period)
        randomattr2 = self.driver.find_element_by_css_selector(".Widget:nth-child(1) > #AttributeDisplay").text
        print(randomattr2)

        time.sleep(self.polling_period)
        randomattr3 = self.driver.find_element_by_css_selector(".Widget:nth-child(1) > #AttributeDisplay").text
        print(randomattr3)

        msg = "FAILED. Value does not change every " + str(self.polling_period) + " seconds with one attribute.\n"
        assert (randomattr1 != randomattr2 and randomattr2 != randomattr3), msg

    def test_webjive_pubsub_double_attr(self):
        """
        """
        print("Opening dashboard... ", end=" ")
        if not self.open_dashboard(self.driver, "DoubleAttributeTestDashboard"):
            msg = "FAILED. Could not open dashboard DoubleAttributeTestDashboard"
            self.fail(msg=msg)
        print("SUCCESS")

        self.driver.find_element_by_css_selector(".form-inline > button").click()
        time.sleep(1)
        self.driver.find_element_by_css_selector(".form-inline > button").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector(".form-inline > button").click()
        time.sleep(0.7)
        self.driver.find_element_by_css_selector(".form-inline > button").click()
        time.sleep(0.6)
        self.driver.find_element_by_css_selector(".form-inline > button").click()

        print("Checking attribute... ")
        try:
            time.sleep(0.5)
            wait = WebDriverWait(self.driver, 1)
            randomattr1 = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[@id='AttributeDisplay']"))).text
        except TimeoutException:
            msg = "FAILED.  Could not find webjivetestdevice"
            self.fail(msg=msg)

        print(randomattr1)

        time.sleep(self.polling_period*2)
        randomattr2 = self.driver.find_element_by_css_selector(".Widget:nth-child(1) > #AttributeDisplay").text
        print(randomattr2)

        assert randomattr1 != randomattr2, "FAILED. Value does not change every " + str(self.polling_period) + \
                                           " seconds with two attributes.\n"

    def create_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)
        return driver


    def login(self, driver, username, password):
        """Logs the given user in through WebJive GUI using the given username and password.
        Returns True for successful login and False if login fails
        """

        # wait until Log In button is visible
        wait = WebDriverWait(driver, 5)
        logged_in_as = wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class='LogInOut']"))).text
        if username in logged_in_as:
            return True

        try:
            driver.find_element(By.LINK_TEXT, 'Log In').click()
        except NoSuchElementException:
            return False

        # find and populate username and password fields
        username_field = driver.find_element_by_css_selector(".form-group:nth-child(1) > .form-control")
        username_field.send_keys(username)
        password_field = driver.find_element_by_css_selector(".form-group:nth-child(2) > .form-control")
        password_field.send_keys(password)

        driver.find_element_by_css_selector(".btn-primary").click()
        logged_in_as = wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class='LogInOut']"))).text
        expected_welcome_message = "Logged in as " + username
        if expected_welcome_message in logged_in_as:
            return True
        else:
            return False

    def open_dashboard(self, driver, dashboard_name):
        driver.find_element_by_css_selector(".toggle-button-right").click()
        try:
            driver.find_element(By.LINK_TEXT, dashboard_name).click()
        except NoSuchElementException:
            return False
        return True


if __name__ == "__main__":
    test_status = []
    if len(sys.argv) != 4:
        print("Username, password and host address required as arguments")
    else:
        WebjiveE2EPubSubTest.HOST = sys.argv.pop()
        WebjiveE2EPubSubTest.PASSWORD = sys.argv.pop()
        WebjiveE2EPubSubTest.USERNAME = sys.argv.pop()
        unittest.main()
