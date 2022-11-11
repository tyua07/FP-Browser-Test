import math
import random
import time

from helper.inject_js import scroll_to_view
from selenium.webdriver.remote.command import Command


class Move(object):
    def __init__(self, driver, ele):
        self.driver = driver
        self.ele = ele

    @property
    def _offset(self):
        """
        生产一个随机的 offset
        """
        return random.randint(300, 400)

    @property
    def scroll_after_sleep(self):
        """
        滑动完随机 sleep 一下
        """
        return round(random.randint(700, 2000) / 1000, 2)

    def scroll_top(self):
        """
        获得滚动条距离
        """
        result = self.driver.execute_script("return document.documentElement.scrollTop || document.body.scrollTop;")
        if result is None:
            return 0
        else:
            return int(result)

    def scroll(self, y):
        if y > 0:
            print('向下滑动一次')
        else:
            print('向上滑动一次')

        self.driver.execute(Command.TOUCH_SCROLL, {
            'element': self.ele.id,
            'xoffset': 0,
            'yoffset': y,
            'speed': random.randint(100, 400),
            'repeatCount': 0,
            'repeatDelayMs': self.scroll_after_sleep,
        })

        # 随机 sleep 一下
        time.sleep(self.scroll_after_sleep)

    def move_once(self, num):
        """
        循环滑上滑下
        """
        for i in range(num):
            offset = self._offset

            self.scroll(y=offset)

            self.scroll(y=-offset)

    def move_loop(self, num):
        """
        短距离滑下多次，然后再滑上
        """
        offset = self._offset

        for i in range(num):
            self.scroll(y=offset)

        for i in range(num):
            scroll_top_num = self.scroll_top()

            # 如果为 null，则不滑动
            if scroll_top_num < 15:
                return
            else:
                self.scroll(y=-offset)

    def handle(self, num=0):
        """
        滑动
        """
        if num <= 0:
            # 滑动到指定元素
            scroll_to_view(driver=self.driver, ele=self.ele)
            return

        print('Scroll Total Number = {}'.format(num))

        if num == 1:
            self.scroll(y=self._offset)
        else:
            loop_number = math.floor(num / 2)

            if num <= 4:
                self.move_loop(num=loop_number)
            else:
                self.move_once(num=loop_number)

            # 如果是单数,则再次滑动一下
            if num % 2 != 0:
                self.scroll(y=self._offset)

        # 滑动到指定元素
        scroll_to_view(driver=self.driver, ele=self.ele)
