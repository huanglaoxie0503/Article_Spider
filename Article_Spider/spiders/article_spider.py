# -*- coding: utf-8 -*-
import scrapy
import time
import base64
import re
import json
import datetime
from mouse import move, click
from urllib import parse
from scrapy.loader import ItemLoader

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from zheye import zheye

from Article_Spider.items import ArticleSpiderQuestionItem, ArticleSpiderAnswerItem


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
    headers = {
        "referer": "https://www.zhihu.com",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

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
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("xxx")
        time.sleep(2)
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("xxx")
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
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("xxx")
                time.sleep(2)
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys("xxx")

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
        # 提取出html页面中的所有url，并跟踪这些url进行进一步提取，如果提取的url中格式为/question/xxx 就下载之后直接进入解析函数
        # question/333089890/answer/743578205
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match(r"(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                request_id = match_obj.group(2)
                print(request_url, request_id)
                # 如果提取到question相关页面则下载后交由提取函数进行提取
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        # 处理question页面，从页面中提取出具体问题信息（item）
        if "QuestionHeader-title" in response.text:
            match_obj = re.match(r"(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ArticleSpiderQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("question_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-actions button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-value::text")
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")

            question_item = item_loader.load_item()
        else:
            # 处理老版本页面的item提取
            match_obj = re.match(r"(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ArticleSpiderQuestionItem(), response=response)
            # item_loader.add_css("title", ".zh-question-title h2 a::text")
            item_loader.add_xpath("title",
                                  "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("question_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")
            item_loader.add_xpath("watch_user_num", "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers, callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        # 处理question的answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ArticleSpiderAnswerItem()
            answer_item["answer_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parse_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)
