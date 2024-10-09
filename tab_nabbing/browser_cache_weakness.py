from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_browser_cache_weakness(login_url, username, password, protected_page_url, logout_button_xpath):
    # Set up the WebDriver
    driver = webdriver.Chrome()  # You can use Firefox or another browser driver
    try:
        # Step 1: Log in to the application
        driver.get(login_url)
        time.sleep(2)

        # Find username and password fields, and submit login (adjust the locators)
        driver.find_element(By.NAME, "uid").send_keys(username)
        driver.find_element(By.NAME, "passw").send_keys(password)
        driver.find_element(By.ID, "LoginLink").click()
        time.sleep(3)  # Wait for login to complete

        # Step 2: Access the protected page
        driver.get(protected_page_url)
        time.sleep(2)
        protected_page_content = driver.page_source  # Store the protected page content

        # Step 3: Log out from the application
        driver.find_element(By.XPATH, logout_button_xpath).click()
        time.sleep(2)  # Wait for logout to complete

        # Step 4: Simulate pressing the back button
        driver.execute_script("window.history.go(-1)")
        time.sleep(2)  # Wait for the page to reload

        # Step 5: Check if the protected page is still accessible
        back_page_content = driver.page_source  # Capture content after pressing back

        if protected_page_content == back_page_content:
            print("Vulnerable to browser cache weakness: Protected page shown after logout")
        else:
            print("Not vulnerable: Redirected to login page or error after logout")

    finally:
        driver.quit()


# Input details for the test
login_url = "https://altoro.testfire.net/login.jsp"
protected_page_url = "https://altoro.testfire.net/bank/main.jsp"
username = "admin"
password = "admin"
logout_button_xpath = "//*[@id='LoginLink']"  # Change the XPath to match your application

# Run the test
test_browser_cache_weakness(login_url, username, password, protected_page_url, logout_button_xpath)
