import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class WebjiveE2ETest:
    polling_period = 0.5

    # What was the agreed naming when talking about the whole system (webjive+tangogql)? ***
    def test_webjive_pubsub(self, username, password, host):
        """ Compare three values of a randomattr of webjivetestdevice with polling period 0.5
        """

        print("\nRunning WebJive Suite Pub/Sub Test... \n")
        driver = self.create_driver()

        print("Loading page " + host + "... ", end=" ")
        driver.get(host)
        expected_title = "WebJive"
        page_load_error_msg = "FAILED. The Webjive page was not loaded correctly. Page title should contain '" \
                              + expected_title + "' but title is '" + driver.title + "'"
        if expected_title not in driver.title:
            print(page_load_error_msg)
            return False
        print("SUCCESS")

        driver.find_element(By.LINK_TEXT, 'Dashboards').click()
        print("Logging in... ", end=" ")
        if not self.login(driver, username, password):
            print("FAILED. Could not log in")
            return False
        print("SUCCESS")

        print("Opening dashboard... ", end=" ")
        if not self.open_dashboard(driver, "PollingTestDashboard"):
            print("FAILED. Could not open dashboard PollingTestDashboard")
            return False
        print("SUCCESS")

        driver.find_element_by_css_selector(".form-inline > button").click()

        print("Checking attribute polling... ")
        try:
            time.sleep(0.1)
            wait = WebDriverWait(driver, 1)
            randomattr1 = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[@id='AttributeDisplay']"))).text
        except TimeoutException:
            print("FAILED.  Could not find webjivetestdevice")
            return False

        print(randomattr1)

        time.sleep(self.polling_period)
        randomattr2 = driver.find_element_by_css_selector(".Widget:nth-child(1) > #AttributeDisplay").text
        print(randomattr2)

        time.sleep(self.polling_period)
        randomattr3 = driver.find_element_by_css_selector(".Widget:nth-child(1) > #AttributeDisplay").text
        print(randomattr3)

        if randomattr1 == randomattr2 or randomattr2 == randomattr3:
            print("FAILED. Value does not change every " + str(self.polling_period) + " seconds.\n")
            return False
        print("SUCCESS\n")
        return True

    def create_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def close_driver(self, driver):
        driver.close()

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
        test_status.append(False)
    else:
        test_status.append(WebjiveE2ETest().test_webjive_pubsub(sys.argv[1], sys.argv[2], sys.argv[3]))
    total = len(test_status)
    passed = sum(test_status)
    failed = total - passed
    print("Ran " + str(total) + " tests.  " + str(passed) + " passed and " + str(failed) + " failed.\n")
