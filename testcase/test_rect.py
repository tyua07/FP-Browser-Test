import pytest
from helper.util import get_driver, sleep, get_chromium_version, stop_browser_app
from fp_browser_sdk.ext.screen import Screen
from fp_browser_sdk.ext.browser_enum import  BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk import ConfigConvertSetting


class TestRect(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [ './config/redmi_6a.json'])
    def test_width(self, value):
        """
        测试 可视区域页面宽度
        """
        custom_config = ConfigConvertSetting( config_path=value,
                                             browser_version=get_chromium_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return [
                    document.body.clientWidth,
                    document.documentElement.clientWidth,
                    document.body.offsetWidth,
                    document.body.scrollWidth,
                    window.outerWidth,
                    window.innerWidth,
                  ];
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('rect.width')

        print("设置 可视区域页面宽度:", value, setting_value)
        for item in value:
            assert item == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_height(self, value):
        """
        测试 可视区域页面高度
        """
        custom_config = ConfigConvertSetting( config_path=value,
                                             browser_version=get_chromium_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return [
                    document.body.clientHeight,
                    document.documentElement.clientHeight,
                    document.body.offsetHeight,
                    document.body.scrollHeight,
                    window.outerHeight,
                    window.innerHeight,
                  ]
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('rect.height')

        print("设置 可视区域页面高度:", value, setting_value)
        for (index, item) in enumerate(value):
            # 如果是 document.body.clientHeight,  document.body.offsetHeight, document.body.scrollHeight, 则跳过
            if index == 0 or index == 2 or index == 3:
                continue
            assert item == int(setting_value)

        self.driver.close()
        self.driver.quit()
