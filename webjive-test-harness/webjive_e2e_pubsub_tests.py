import unittest
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
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

    def test_webjive_dashboard_home(self):
        print('Testing test_webjive_dashboard_home')
        element = self.driver.find_element_by_css_selector('.dashboard-menu > .dashboard-menu-button')

        assert (True == element.get_property('disabled'))

    def test_webjive_click_dashboard(self):
        print('Testing test_webjive_click_dashbaord')

        self.driver.find_element(By.LINK_TEXT, 'Dashboards').click()

        element = self.driver.find_element_by_css_selector('.dashboard-menu > .dashboard-menu-button')

        assert (True == element.get_property('enabled'))



    def test_webjive_pubsub(self):
        """
        Test Webjive Suite pub/sub functionality works for one attribute subscribed to change event
        """
        print("Opening dashboard... ", end=" ")
        if not self.open_dashboard(self.driver, "PollingTestDashboard"):
            msg = "FAILED. Could not open dashboard PollingTestDashboard"
            self.fail(msg=msg)
        print("SUCCESS")

        self.driver.find_element_by_css_selector(".form-inline > button").click()

        print("Checking pub/sub with one attribute... ")
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
        Check Webjive Suite pub/sub functionality works when there are more than one attribute subscribed
        to the change event on the dashboard.
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

        print("Checking pub/sub with two attributes... ")
        try:
            time.sleep(0.5)
            wait = WebDriverWait(self.driver, 1)
            first_randomattr = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[@id='AttributeDisplay']"))).text
        except TimeoutException:
            msg = "FAILED.  Could not find webjivetestdevice"
            self.fail(msg=msg)
        first_randomattr2 = self.driver.find_element_by_css_selector(".Widget:nth-child(2) > #AttributeDisplay").text

        print(first_randomattr)
        print(first_randomattr2)
        print("Sleep for " + str(self.polling_period*2) + " seconds")
        time.sleep(self.polling_period*2)
        second_randomattr = self.driver.find_element_by_css_selector(".Widget:nth-child(1) > #AttributeDisplay").text
        second_randomattr2 = self.driver.find_element_by_css_selector(".Widget:nth-child(2) > #AttributeDisplay").text
        print(second_randomattr)
        print(second_randomattr2)

        assert (first_randomattr != second_randomattr) and (first_randomattr2 != second_randomattr2), "FAILED. Value(s) does not change every " + str(self.polling_period) + \
                                           " seconds with two attributes.\n"

    def test_webjive_pubsub_above_50hz(self):
        """
        Function to test the Pub-sub feature at frequency higher than 50hz with single attribute.
        Currently, it is checking unique attribute value at every 10ms(100hz frequency).
        """
        polling_period = 0.01
        attribute_value_list = []

        print("Opening dashboard... ", end=" ")
        if not self.open_dashboard(self.driver, "PubSubTestAbove50hz"):
            msg = "FAILED. Could not open dashboard PubSubTestAbove50hz"
            self.fail(msg=msg)
        print("SUCCESS")

        # find and click start button on dashboard
        self.driver.find_element_by_css_selector(".form-inline > button").click()
        print("Checking pub/sub with one attribute at frequency 100hz... ")
        try:
            time.sleep(polling_period*2)
            # wait until attribute value is visible
            wait = WebDriverWait(self.driver, 1)
            randomattr = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[@id='AttributeDisplay']"))).text
            attribute_value_list.append(randomattr.split(":")[1]);
        except TimeoutException:
            msg = "FAILED.  Could not find webjivetestdevice"
            self.fail(msg=msg)
        print(randomattr)

        for i in range(15):
            print("Sleep for " + str(polling_period) + " seconds")
            time.sleep(polling_period)
            randomattr1 = self.driver.find_element_by_css_selector(".Widget:nth-child(1) > #AttributeDisplay").text
            print(randomattr1)
            attribute_value_list.append(randomattr1.split(":")[1]);

        msg = "FAILED. Value does not change every " + str(polling_period) + " seconds with one attribute.\n"
        assert (len(attribute_value_list) == len(set(attribute_value_list))),msg

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
