chats_xpath = "//div[contains(text(), 'Not in your contacts')]"
chat_element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, chats_xpath))
)
print(chat_element.get_attribute('innerHTML'))
_element = chat_element.find_element(By.XPATH, "ancestor::*[1]")
print(_element.get_attribute('innerHTML'))
direct_child_divs = _element.find_elements(By.XPATH, "div")
last_child_div = direct_child_divs[-1]
print(last_child_div.get_attribute('innerHTML'))
time.sleep(3)