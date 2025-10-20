# 套件 Selenium : 等待 WebDriverWait
# 匯入套件
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

# 開啟用於自動控制的瀏覽器
driver = webdriver.Chrome()

try:
    # 最多等 15 秒
    driver.implicitly_wait(15)

    # 走訪網址
    driver.get('https://tw.yahoo.com/')

    # 取得元素
    element = driver.find_element(
        By.CSS_SELECTOR,
        'a#header-logo'
    )

    # 印出超連結 ( 透過 .get_attribute('屬性') 來取得屬性的值 )
    print(element.get_attribute('href'))
except NoSuchElementException:
    print("找不到元素!")
finally:
    # 關閉瀏覽器
    driver.quit()
