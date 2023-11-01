import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# 帮助文档: https://zhuanlan.zhihu.com/p/111859925


driver_path = "/Users/dujian/workspace/tools/driver"


def login():
    driver = webdriver.Chrome()
    driver.get("https://hax.co.id/login")
    driver.maximize_window()
    print(driver.page_source)
    # 查询cookie弹窗
    consent = driver.find_element(by=By.CSS_SELECTOR, value="button[class*='fc-cta-consent']")
    # 接受cookie
    if consent:
        # print(content.location["x"], content.location["y"])
        # ActionChains(driver).move_to_element(to_element=content).click_and_hold(content)
        consent.click()
    driver.save_screenshot("screen.png")
    time.sleep(100)
    driver.close()


if __name__ == '__main__':
    login()
