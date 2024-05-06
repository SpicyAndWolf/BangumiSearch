from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util_ocr import identify_code_analysis
from util_ocr import identify_code_find


class Driver(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://bangumi.tv")
        self.driver.maximize_window()

    def register_page_enter(self):
        # 进入注册界面
        register_btn = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[3]/div/a[2]')
        register_btn.click()
        self.driver.find_element_by_xpath('//*[@id="loginSelection"]/ul/li[2]/a').click()

        # 显式等待表单出现并可交互
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.element_to_be_clickable((By.ID, "email")))

        # 填写表单
        email = "spicy135135@gmail.com"
        password = "spicy135135"
        nickname = "spicy135135"
        guideline = "不提供"
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("password2").send_keys(password)
        self.driver.find_element_by_id("nickname").send_keys(nickname)
        self.driver.find_element_by_id("guideline").send_keys(guideline)

    def register(self):
        self.register_page_enter()
        while 1:
            code_img_url = identify_code_find(self.driver, 0)
            res = identify_code_analysis(self.driver, code_img_url, 0)
            if res:
                break
        print("success")


if __name__ == "__main__":
    driver = Driver()
    driver.register()
