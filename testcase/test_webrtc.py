import pytest
from helper.util import get_driver, sleep, get_file_script_context, stop_browser_app
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.webrtc import Webrtc


class TestWebrtc(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["192.168.0.100", "10.0.1.12"])
    def test_privite_ip(self, value):
        """
        测试 强制设置 stun 协议获得的局域网 IP
        """
        settings = FPBrowserSettings()

        webrtc = Webrtc() \
            .set_privite_ip(value) \
            .set_public_ip("8.8.8.8") \
            .set_host_name("sasasa")

        settings.add_module(webrtc)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/webrtc.js')
        value = self.driver.execute_script(script).get('privite_ip_addr')
        setting_value = self.config.get('webrtc.privite-ip')

        print("设置 强制设置 stun 协议获得的局域网 IP:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["8.8.8.8", "220.102.10.87"])
    def test_public_ip(self, value):
        """
        测试 强制设置 stun 协议获得的外网 IP
        """
        settings = FPBrowserSettings()

        webrtc = Webrtc() \
            .set_privite_ip("192.168.0.11") \
            .set_public_ip(value) \
            .set_host_name("sasasa")

        settings.add_module(webrtc)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/webrtc.js')
        value = self.driver.execute_script(script).get('public_ip_addr')
        setting_value = self.config.get('webrtc.public-ip')

        print("设置 强制设置 stun 协议获得的外网 IP:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()
