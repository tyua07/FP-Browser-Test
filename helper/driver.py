import sys
import os
import json
import base64
from appium import webdriver
from exception.chrome_driver_error_exception import ChromeDriverErrorException
from helper.appium_system_port import AppiumSystemPort
from helper.appium_mjpeg_server_Port import AppiumMjpegServerPort
from helper.base64_util import base64_encode, base64_decode
from helper.aes import AESLibrary


class Driver(object):

    @staticmethod
    def get_wd_host(port):
        """
        获得 wd 端口
        """
        return 'http://localhost:{}/wd/hub'.format(port)

    @staticmethod
    def format_chrome_driver_options2(dict):
        """
        重新组合配置 dict
        """
        params = []

        for (key, item) in dict.items():
            params.append('--{0}={1}'.format(key, item))
        return params

    @staticmethod
    def format_chrome_driver_options(settions: dict, default_option_prefix: str, encrypt=True):
        """
        重新组合配置 dict
        """

        if encrypt is False:
            return Driver.format_chrome_driver_options2(settions)

        params = []

        result = []
        ensure_ascii = True
        for (key, item) in settions.items():
            # 强制把数字类型转成字符串
            if isinstance(item, (int, float)):
                item = str(item)
            elif isinstance(item, (list, dict)):
                # 如果是 list 或者 dict，则先转换成 json
                if isinstance(item, list) and len(item) == 0:
                    item = ""
                elif isinstance(item, dict) and len(item.keys()) == 0:
                    item = ""
                else:
                    item = json.dumps(item, ensure_ascii=ensure_ascii)

            # 全部 base64，防止中文乱码
            if item and item != "":
                item = base64_encode(item)

            result.append({
                "name": "{}-{}".format(default_option_prefix, key),
                "value": item
            })
            pass

        print('')
        print(json.dumps(settions, ensure_ascii=False))
        # for item in result:
        #     print(item['name'], base64_decode(item['value']))

        cipher_text = AESLibrary().encrypt(json.dumps(result, ensure_ascii=ensure_ascii))
        # cipher_text = json.dumps(result, ensure_ascii=ensure_ascii)
        params.append('--chrome-custom-{0}={1}'.format("settings-json", AESLibrary.to_string(cipher_text)))
        # params.append('--chrome-custom-{0}={1}'.format("settings-json", cipher_text))
        return params

        # params = []
        #
        # for (key, item) in settions.items():
        #     params.append('--chrome-custom-{0}={1}'.format(key, item))
        # return params

    @staticmethod
    def get_chrome_driver(version):
        """
        获得 chrome 驱动路径
        """
        platform = sys.platform
        dir = r'./drives/' + version
        if os.path.isdir(dir):
            if platform.startswith('win32'):
                path = dir + '/chromedriver.exe'
            elif platform.startswith('darwin'):
                # 这里直接引用实时编译好了的路径
                path = dir + '/chromedriver_mac64'  # 官方的
            else:
                path = dir + '/chromedriver_linux64'

            return os.path.abspath(path)
        else:
            raise ChromeDriverErrorException()

    @staticmethod
    def android_appium_desired_caps(uuid, config, version, default_option_prefix, browser_name, encrypt):
        default_args = [
            "--disable-popup-blocking",
            "--ignore-certificate-errors",
            "--ignore-ssl-errors",
            # "--disable-web-security",
            "--disable-build-check",
            # "--enable-logging",
            # "--v=1",
            "--disable-dev-shm-usage",
            "--no-first-run",
        ]
        chrome_agrs = default_args + Driver.format_chrome_driver_options(settions=config,
                                                                         default_option_prefix=default_option_prefix,
                                                                         encrypt=encrypt)
        desired_caps = dict(
            # Platform
            platformName="Android",
            deviceName=uuid,
            udid=uuid,
            browserName=browser_name,

            # Common
            noReset=False,
            nativeWebTap=True,
            clearSystemFiles=True,
            newCommandTimeout=60 * 10,  # 最大等待时间，如果超过这个时间没有动作，则自动退出

            # Android Only
            systemPort=AppiumSystemPort.instance().get_port(),
            mjpegServerPort=AppiumMjpegServerPort.instance().get_port(),
            automationName='UiAutomator2',
            deviceReadyTimeout=100,
            skipLogcatCapture=True,
            ensureWebviewsHavePages=True,
            ignoreHiddenApiPolicyError=True,
            chromedriverDisableBuildCheck=True,
            chromedriverExecutable=Driver.get_chrome_driver(version),
            chromeOptions={
                "w3c": False,
                "args": chrome_agrs,
            },
            pageLoadStrategy='none',
        )

        return desired_caps

    @staticmethod
    def get_browser_name(package_name):
        """
        对应浏览器名称
        """
        if package_name == 'org.chromium.chrome88':
            return "chromium-browser88"
        elif package_name == 'org.chromium.chrome90':
            return "chromium-browser90"
        elif package_name == 'org.chromium.chrome93':
            return "chromium-browser93"

        return "chromium-browser"

    @staticmethod
    def handle(
            uuid,
            version,
            config,
            appium_port,
            package_name,
            encrypt,
            default_option_prefix="default-option"
    ):
        """
        获得 driver 对象
        """
        # 获得 wd host
        wd_host = Driver.get_wd_host(appium_port)

        return webdriver.Remote(
            wd_host,
            Driver.android_appium_desired_caps(
                uuid=uuid,
                config=config,
                version=version,
                default_option_prefix=default_option_prefix,
                browser_name=Driver.get_browser_name(package_name),
                encrypt=encrypt
            )
        )
