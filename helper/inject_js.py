from urllib.parse import urlparse
import time


def scroll_top(driver):
    result = driver.execute_script("return document.documentElement.scrollTop || document.body.srcollTop;")
    if result is None:
        return 0
    else:
        return int(result)


def wait_page_load(driver, timeout=5):
    """
    等待页面加载完毕
    """
    now = time.time()
    while True:
        # 判断是否超时
        if time.time() - now > timeout:
            return False

        result = driver.execute_script("return document.readyState")
        if result and result == 'complete':
            return True
        else:
            print(result)


def scroll_to_view(driver, ele):
    print('scroll_to_view')
    time.sleep(2)
    script = '''
        arguments[0].scrollIntoView();
        '''
    driver.execute_script(script, ele)
