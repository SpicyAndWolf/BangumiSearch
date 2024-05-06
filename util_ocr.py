import time
import ddddocr

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image


# type  0: register， 1：login
def identify_code_find(driver, type):
    # 显式等待验证码出现并可交互
    wait = WebDriverWait(driver, 2)
    wait.until(EC.element_to_be_clickable((By.ID, "captcha_img_code")))

    # 获取验证码图片
    current_time = time.time()
    origin_img_url = "./photos/" + str(current_time) + ".png"
    driver.save_screenshot(origin_img_url)

    # 根据注册还是登录页面确定偏移量
    register_p = [95, 20, 125, 10]
    login_p = [95, 20, 85, 10]
    p = register_p
    if type == 1:
        p = login_p

    # 定位验证码位置
    code_element = driver.find_element_by_id("captcha_img_code")
    code_x = code_element.location['x'] + p[0]
    code_x1 = code_element.size['width'] + code_x + p[1]
    code_y = code_element.location['y'] + p[2]
    code_y1 = code_element.size['height'] + code_y + p[3]

    # 扣对应位置的图
    origin_img = Image.open(origin_img_url)
    new_img = origin_img.crop((code_x, code_y, code_x1, code_y1))

    # 存储新图
    current_time = time.time()
    code_img_url = "./photos/" + str(current_time) + ".png"
    new_img.save(code_img_url)
    return code_img_url


# type  0: register， 1：login
def identify_code_analysis(driver, img_url, type):
    # 获取验证码图片，用例识别失败时重新点击
    identity_img = driver.find_element_by_id("captcha_img_code")

    # 识别验证码
    ocr = ddddocr.DdddOcr()
    with open(img_url, 'rb') as f:
        image = f.read()
    res = ocr.classification(image)

    # 输入验证码
    identify_input = driver.find_element_by_id("captcha")
    identify_input.send_keys(res)

    # 提交
    submit_name = "regsubmit"
    if type == 1:
        submit_name = "loginsubmit"
    driver.find_element_by_name(submit_name).click()

    # 判断是否成功
    error_website_register = "https://bangumi.tv/RedPill"
    error_website_login = "https://bangumi.tv/FollowTheRabbit"
    if (driver.current_url == error_website_register) or (driver.current_url == error_website_login):
        # 回退
        driver.back()

        # 等待验证码图片可点击
        wait = WebDriverWait(driver, 2)
        wait.until(EC.element_to_be_clickable((By.ID, "captcha_img_code")))
        identity_img.click()

        # 等待输入框可交互
        wait = WebDriverWait(driver, 2)
        wait.until(EC.element_to_be_clickable((By.ID, "captcha")))
        identify_input.clear()
        return 0
    else:
        return 1


if __name__ == "__main__":
    print("ocr")
