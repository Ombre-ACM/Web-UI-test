"""
    关键字驱动   将常用的操作行为用selenium进行二次封装
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait

from config.log import get_log

log = get_log()


# 不同浏览器生成
def open_browser(txt):

    try:
        # 基于反射机制，进行逻辑代码的简化
        driver = getattr(webdriver, txt)()

    except Exception as e:
        print(e)
        driver = webdriver.Chrome()

    return driver


class Key:

    # driver = webdriver.Chrome()

    def __init__(self, txt):
        try:
            log.info('初始化浏览器 {}'.format(txt))
            self.driver = open_browser(txt)
            # 隐式等待
            self.driver.implicitly_wait(5)
        except Exception as e:
            log.error('初始化浏览器失败 {}'.format(e))

    # 打开 url
    def open(self, txt):
        try:
            log.info('正在打开网站 {}'.format(txt))
            self.driver.get(txt)
        except Exception as e:
            log.error('打开网站失败 {}'.format(e))

    # 元素定位
    def locate(self, name, value):
        return self.driver.find_element(name, value)

    # 输入内容
    def input(self, name, value, txt):
        try:
            log.info('正在输入内容  {}，元素{}，元素值{}'.format(txt, name, value))
            self.locate(name, value).send_keys(txt)
        except Exception as e:
            log.error('输入内容失败 {}，元素{}，元素值{}'.format(e, name, value))

    # 点击
    def click(self, name, value):
        try:
            log.info('正在点击按钮，元素{}，元素值{}'.format(name, value))
            self.locate(name, value).click()
        except Exception as e:
            log.error('点击按钮失败 {}，元素{}，元素值{}'.format(e, name, value))

    # 显示等待
    def web_el_wait(self, name, value):
        try:
            log.info('正在显示等待，元素{}，元素值{}'.format(name, value))
            return WebDriverWait(self.driver, 10, 0.5).until(
                lambda el: self.locate(name, value), message='元素查找失败')
        except Exception as e:
            log.error('显示等待失败 {}，元素{}，元素值{}，'.format(e, name, value))

    # 强制等待
    def sleep(self, txt):
        log.info('正在强制等待 {}秒'.format(txt))
        sleep(int(txt))

    # 退出
    def quit(self):
        log.info('正在关闭')
        self.driver.quit()

    # 切换 frame
    def switch_frame(self, value, name=None):
        try:
            if name is None:
                log.info('正在切换frame, 元素值{}'.format(value))
                self.driver.switch_to.frame(value)
            else:
                log.info('正在切换frame，元素{}，元素值{}'.format(name, value))
                self.driver.switch_to.frame(self.locate(name, value))
        except Exception as e:
            log.error('切换frame失败 {}，元素{}，元素值{}，'.format(e, name, value))

    # def switch_frame_simple(self, value, name=None):
    #     self.driver.switch_to.frame(self.locate(name, value))

    # 切回去
    def switch_default(self):
        try:
            log.info('正在切回初始网页')
            self.driver.switch_to.default_content()
        except Exception as e:
            log.error('切回初始网页失败 {}'.format(e))

    # 句柄切换
    def switch_handle(self, close=False, index=1):
        try:
            log.info('正在切换句柄')
            handles = self.driver.window_handles
            if close:
                self.driver.close()
            self.driver.switch_to.window(handles[index])
        except Exception as e:
            log.error('切换句柄失败 {}'.format(e))

    # def switch_handle_1(self, index):
    #     handles = self.driver.window_handles
    #     self.driver.switch_to.window(handles[index])

    # 相对定位器
    def locator_with(self, method, value, el_name, el_value, direction):
        try:
            log.info('正在相对定位')
            el = self.locate(el_name, el_value)

            method_dict = {
                "id": By.ID,
                "xpath": By.XPATH,
                "link text": By.LINK_TEXT,
                "partial link text": By.PARTIAL_LINK_TEXT,
                "name": By.NAME,
                "tag name": By.TAG_NAME,
                "class name": By.CLASS_NAME,
                "css selector": By.CSS_SELECTOR
            }

            direction_dict = {
                'left': 'to_left_of',
                'right': 'to_right_of',
                'above': 'above',
                'below': 'below',
                'near': 'near'
            }

            return self.driver.find_element(getattr(locate_with(method_dict.get(method), value), direction_dict.get(direction))(el))
        except Exception as e:
            log.error('相对定位失败 {}'.format(e))

    # 断言文本信息
    def assert_text(self, name, value, expect):
        try:
            log.info('正在断言，预期：{}'.format(expect))
            reality = self.locate(name, value).text
            assert expect == reality, '断言失败，实际结果为：{}'.format(reality)
            return True
        except Exception as e:
            log.error('断言失败，与预期不符合：{}'.format(e))
            return False

    # 鼠标悬停   ActionChains(driver).move_to_element(element).perform()  下一步需要 locate().click()
    def mouse_stop_at(self, name, value):
        try:
            log.info('正在鼠标悬停，元素{}，元素值{}'.format(name, value))
            ActionChains(self.driver).move_to_element(self.locate(name, value)).perform()
            sleep(1)
        except Exception as e:
            log.error('鼠标悬停失败 {}，元素{}，元素值{}'.format(e, name, value))

    # 移动到指定元素
    def move_to(self, name, value):
        ActionChains(self.driver).move_to_element(self.locate(name, value)).perform()

