import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from PyQt5.QtCore import pyqtSignal, QObject

class WhatsApp(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.options = Options()
        self.options.add_argument("--user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data")
        self.options.add_argument("--profile 3")
        self.options.add_argument("--disable-tflite-xnnpack")

    def setup_browser(self):
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.options)
            self.driver.get("https://web.whatsapp.com/")
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@title='New chat']")))
            return self.driver
        except Exception as e:
            return None
        
    def on_message_sent(self):
        self.finished.emit()

    def send_message(self, message, phone):
        self.driver = self.setup_browser()
        if self.driver is None:
            self.finished.emit()
            return
        self.start_send_message(message, phone)

    def start_send_message(self, message, phone):
        driver = self.driver
        try:
            new_chat_button = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@title='New chat']"))
            )
            time.sleep(5)
            print(new_chat_button.get_attribute('innerHTML'))
            new_chat_button.click()
            phone_number_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search name or number']"))
            )
            phone_number_input.send_keys(phone)
            chats_xpath = "//div[contains(text(), 'Contacts on WhatsApp')]"
            chat_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, chats_xpath))
            )
            _element = chat_element.find_element(By.XPATH, "ancestor::*[2]")
            parent_element = _element.find_element(By.XPATH, "ancestor::*[1]")
            WebDriverWait(driver, 30).until(EC.visibility_of(parent_element))
            time.sleep(5)

            direct_child_divs = parent_element.find_elements(By.XPATH, "div")
            last_child_div = direct_child_divs[-1]
            time.sleep(5)
            last_child_div.click()

            time.sleep(5)
            type_a_message = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Type a message']"))
            )
            type_a_message.click()

            actions = ActionChains(driver)
            actions.send_keys_to_element(type_a_message, message)
            actions.perform()
            time.sleep(5)
            send_button_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button [@aria-label='Send']"))
            )
            send_button_div.click()
            time.sleep(5)
            self.on_message_sent()
            return "success"
        except Exception as e:
            self.on_message_sent()
            return e