# -*- coding: utf-8 -*-
import scrapy
import time
import base64
from mouse import move, click

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


from zheye import zheye


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def start_requests(self):
        chrome_option = Options()
        """
        手动启动Chrome,避免被反爬识别
        Chrome安装目录下，命令行执行：chrome.exe --remote-debugging-port=9222
        验证启动是否成功：http://127.0.0.1:9222/json
        """
        chrome_option.add_argument("--disable-extensions")
        chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        browser = webdriver.Chrome(chrome_options=chrome_option)
        try:
            browser.maximize_window()
        except:
            pass
        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13662241324")
        time.sleep(2)
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("root050350")
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(3)
        login_success = False

        if login_success:
            cookies_list = browser.get_cookies()
            print(cookies_list)
            cookie_dict = {}
            import pickle
            for cookie in cookies_list:
                # 写入文件
                f = open('./Article_Spider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
                pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
            browser.close()
            return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

        while not login_success:
            try:
                browser.find_element_by_class_name("Popover PushNotifications AppHeader-notifications")
                login_success = True

                cookies_list = browser.get_cookies()
                print(cookies_list)
                cookie_dict = {}
                for cookie in cookies_list:
                    # 写入文件
                    f = open('./Article_Spider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
                    import pickle
                    pickle.dump(cookie, f)
                    f.close()
                    cookie_dict[cookie['name']] = cookie['value']
                browser.close()
                return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
            except:
                pass

            try:
                english_captcha_element = browser.find_element_by_class_name("Captcha-englishImg")
            except:
                english_captcha_element = None
            try:
                chinese_captcha_element = browser.find_element_by_class_name("Captcha-chineseImg")
            except:
                chinese_captcha_element = None

            # 识别中文倒立汉字
            if chinese_captcha_element:
                ele_postion = chinese_captcha_element.location
                x_relative = ele_postion["x"]
                y_relative = ele_postion["y"]
                browser_navigation_panel_height = browser.execute_script(
                    'return window.outerHeight - window.innerHeight;')
                base64_text = chinese_captcha_element.get_attribute("src")

                code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")
                fh = open("verify_code.jpeg", "wb")
                fh.write(base64.b64decode(code))
                fh.close()

                z = zheye()
                positions = z.Recognize('verify_code.jpeg')
                last_position = []
                if len(positions) == 2:
                    if positions[0][1] > positions[1][1]:
                        last_position.append([positions[1][1], positions[1][0]])
                        last_position.append([positions[0][1], positions[0][0]])
                    else:
                        last_position.append([positions[0][1], positions[0][0]])
                        last_position.append([positions[1][1], positions[1][0]])
                    first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                    second_position = [int(last_position[1][0] / 2), int(last_position[1][1] / 2)]
                    move(x_relative + first_position[0], y_relative+browser_navigation_panel_height+first_position[1])
                    click()
                    time.sleep(3)
                    move(x_relative + second_position[0],
                         y_relative + browser_navigation_panel_height + second_position[1])
                    click()
                else:
                    last_position.append([positions[0][1], positions[0][0]])
                    first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                    move(x_relative + first_position[0],
                         y_relative + browser_navigation_panel_height + first_position[1])
                    click()

                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13662241324")
                time.sleep(2)
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys("root0503")

                move(911, 643)
                click()

            # 识别英语字母验证码
            if english_captcha_element:
                base64_text = english_captcha_element.get_attribute("src")
                code = base64_text.replace('data:image/jpg;base64,', '').replace("%0A", "")
                # print code
                fh = open("yzm_en.jpeg", "wb")
                fh.write(base64.b64decode(code))
                fh.close()

                from tools.yundama_requests import YDMHttp
                yundama = YDMHttp("xxx", "xxx", 3129, "xxx")
                code = yundama.decode("yzm_en.jpeg", 5000, 60)
                while True:
                    if code == "":
                        code = yundama.decode("yzm_en.jpeg", 5000, 60)
                    else:
                        break

                browser.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(Keys.CONTROL + "a")
                browser.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(
                    code)

                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    "xxx")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys("xxx")
                move(895, 603)
                click()

    def parse(self, response):
        print(response.text)
