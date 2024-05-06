import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util_ocr import identify_code_analysis
from util_ocr import identify_code_find
from selenium.webdriver.support.select import Select


class Driver(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://bangumi.tv")
        self.driver.maximize_window()

    def login_page_enter(self):
        # 进入登录界面
        login_btn = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[3]/div/a[1]')
        login_btn.click()

        # 显式等待表单出现并可交互
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.element_to_be_clickable((By.ID, "email")))

        # 填写表单
        email = "spicy135135@gmail.com"
        password = "spicy135135"
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)

    def login(self):
        self.login_page_enter()
        while 1:
            code_img_url = identify_code_find(self.driver, 1)
            res = identify_code_analysis(self.driver, code_img_url, 1)
            if res:
                break
        print("success")

    def search_anime(self, anime_name):
        # 定位下拉框
        self.driver.implicitly_wait(1)
        select_element = self.driver.find_element_by_id("siteSearchSelect")
        select_list = Select(select_element)

        # 选择动画
        select_list.select_by_visible_text("动画")

        # 搜索
        self.driver.find_element_by_id("search_text").send_keys(anime_name)
        self.driver.find_element_by_xpath('//*[@id="headerSearch"]/form/div/input[2]').click()

        # 找到匹配的结果
        self.driver.find_element_by_link_text(anime_name).click()

    def mark(self):
        # 点击看过
        self.driver.find_element_by_xpath('//*[@id="SecTab"]/ul/li[2]/a/span').click()

        # 等待弹框加载完毕
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.presence_of_all_elements_located((By.ID, "TB_ajaxContent")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rating"]')))
        wait.until(EC.element_to_be_clickable((By.ID, "comment")))

        # 打分并输入评价
        self.driver.find_element_by_xpath('//*[@id="rating"]/a').click()
        self.driver.find_element_by_id("tags").send_keys("TV")
        self.driver.find_element_by_id("comment").send_keys("非常好")
        self.driver.find_element_by_id("privacy").click()

        # 提交
        self.driver.find_element_by_xpath('//*[@id="submitBtnO"]/input').click()

    def post_article(self):
        # 隐式等待
        self.driver.implicitly_wait(2)

        # 鼠标移到头像上
        head_img = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[3]/a/span')
        ActionChains(self.driver).move_to_element(head_img).perform()

        # 点击日志板块
        article_module = self.driver.find_element_by_xpath('//*[@id="badgeUserPanel"]/li[2]/a').click()
        ActionChains(self.driver).click(article_module).perform()

        # 点击发表新日志
        self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div[2]/div[2]/div/span/a').click()

        # 输入内容
        self.driver.find_element_by_id("tpc_title").send_keys("test")
        self.driver.find_element_by_id("tpc_content").send_keys("图片：")

        # 加入图片
        self.driver.find_element_by_xpath('//*[@id="markItUpTpc_content"]/div/div[1]/ul/li[6]/a').click()
        alert = self.driver.switch_to.alert
        alert.send_keys("https://raw.githubusercontent.com/SpicyAndWolf/PicGo/master/20221128_001852.jpg")
        alert.accept()

        # 输入tag
        self.driver.find_element_by_id("tags").send_keys("test")

        # 提交
        self.driver.find_element_by_xpath('//*[@id="submitBtnO"]/input').click()

    def post_message(self):
        # 进入
        self.driver.find_element_by_xpath('//*[@id="navMenuNeue"]/li[1]/a/span').click()
        self.driver.find_element_by_link_text("只要英子唱起歌来，一切都会好的").click()

        # 滚到最下方
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 发表评论
        self.driver.find_element_by_id("content").send_keys("test")

        # 提交
        self.driver.find_element_by_xpath('//*[@id="submitBtnO"]/input').click()


if __name__ == "__main__":
    anime_name = "狼与香辛料"
    if len(sys.argv) > 1:
        anime_name = sys.argv[1]
    else:
        print("请输入参数——作品名，   格式如 xx.exe ’狼与香辛料'")
    driver = Driver()
    driver.login()
    driver.search_anime(anime_name)
