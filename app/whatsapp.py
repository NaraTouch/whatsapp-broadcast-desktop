import random
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PyQt5.QtCore import pyqtSignal, QObject
from .random_message import RandomMessage

class WhatsApp(QObject):
    finished = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # self.options.add_argument("--user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data")
        # self.options.add_argument("--profile 3")
        # self.options.add_argument("--disable-tflite-xnnpack")

    def setup_browser(self, user_data_dir, profile):
        try:
            self.options = Options()
            self.options.add_argument(f"--user-data-dir={user_data_dir}")
            self.options.add_argument(f"--{profile}")
            self.options.add_argument("--disable-tflite-xnnpack")
            # self.options.add_argument('headless')
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.options)
            self.driver.get("https://web.whatsapp.com/")
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@title='New chat']")))
            return self.driver
        except Exception as e:
            return None
        
    def on_message_sent(self, status):
        self.finished.emit(status)

    def send_message(self, messages, phone_number_list, user_data_dir, profile):
        self.driver = self.setup_browser(user_data_dir, profile)
        if self.driver is None:
            # self.finished.emit()
            self.on_message_sent("Before start please exit chrome browser at first")
            return "Before start please exit chrome browser at first"
        return self.start_send_message(messages, phone_number_list)
    
    def random_message(self, messages):
        random_message_generator = RandomMessage(messages)
        return random_message_generator.random_message()
    
    def find_contact(self, driver):

        chats_xpath = "//div[contains(text(), 'Contacts on WhatsApp')]"
        chat_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, chats_xpath))
        )
        _element = chat_element.find_element(By.XPATH, "ancestor::*[2]")
        parent_element = _element.find_element(By.XPATH, "ancestor::*[1]")
        WebDriverWait(driver, 30).until(EC.visibility_of(parent_element))
        time.sleep(3)

        try:
            direct_child_divs = parent_element.find_elements(By.XPATH, "div")
            contact = direct_child_divs[-1]
            time.sleep(3)
            contact.click()
            print("Click successful!: Contacts on WhatsApp")
        except Exception as e:
            chats_xpath = "//div[contains(text(), 'Not in your contacts')]"
            chat_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, chats_xpath))
            )
            _element = chat_element.find_element(By.XPATH, "ancestor::*[1]")
            direct_child_divs = _element.find_elements(By.XPATH, "div")
            last_child_div = direct_child_divs[-1]
            second_div = last_child_div.find_element(By.XPATH, "div[2]")
            time.sleep(3)
            second_div.click()
            print("Click successful!: Not in your contacts")
        return driver
    
    def start_send_message(self, messages, phone_number_list):
        driver = self.driver
        for phone in phone_number_list:
            message = self.random_message(messages)
            try:
                new_chat_button = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@title='New chat']"))
                )
                time.sleep(5)
                # print(new_chat_button.get_attribute('innerHTML'))
                new_chat_button.click()
                
                # Start New verion
                phone_number_input = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search name or number']"))
                )
                phone_number_input.click()
                pyperclip.copy(phone)
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                # End New verion

                # Start Old verion
                # phone_number_input = WebDriverWait(driver, 60).until(
                #     EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search name or number']"))
                # )
                # phone_number_input.send_keys(phone)
                # End Old verion

                driver = self.find_contact(driver)
                time.sleep(3)
                type_a_message = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Type a message']"))
                )
                type_a_message.click()

                # Copy the message
                pyperclip.copy(message)

                # Paste the message
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

                send_button_div = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button [@aria-label='Send']"))
                )
                send_button_div.click()
                time.sleep(3)
                self.on_message_sent("success on phone number : " + phone)
            except Exception as e:
                self.on_message_sent("failed on phone number : " + phone)
                continue

        self.on_message_sent("All phone number successfully sent")
        return "All phone number successfully sent"