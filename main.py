from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

SIMILAR_ACCOUNT = os.getenv("SIMILAR_ACCOUNT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

class InstaFollower:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        wait = WebDriverWait(self.driver, 15)

        try:
            cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Only allow essential cookies']")))
            cookie_button.click()
        except:
            pass

        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        self.driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.ENTER)
        time.sleep(4)

        try:
            not_now_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]")))
            not_now_btn.click()
        except:
            pass

        try:
            notifications_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]")))
            notifications_btn.click()
        except:
            pass

    def find_followers(self):
        wait = WebDriverWait(self.driver, 15)
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        time.sleep(2)

        followers_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/followers')]")))
        followers_link.click()

        try:
            modal = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@role='dialog']//div[contains(@style,'overflow')]")
            ))
            for _ in range(5):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(2)
        except TimeoutException:
            print("❌ Followers modal not found.")
            return

    def follow(self):
        time.sleep(2)
        follow_buttons = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//button[div/div[text()='Follow']]")
        print(f"Found {len(follow_buttons)} follow buttons.")

        for btn in follow_buttons:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.5)
                btn.click()
                print("✅ Followed a user")
                time.sleep(1.5)
            except ElementClickInterceptedException:
                try:
                    cancel_btn = self.driver.find_element(By.XPATH, "//button[text()='Cancel']")
                    cancel_btn.click()
                except:
                    pass
            except Exception as e:
                print(f"⚠️ Error while following: {e}")

if __name__ == "__main__":
    bot = InstaFollower()
    bot.login()
    bot.find_followers()
    bot.follow()
