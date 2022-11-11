import pytest
from helper.util import get_driver, sleep, get_chromium_version, stop_browser_app
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.screen import Screen
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk import ConfigConvertSetting


class TestChromeDriver(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_chrome_driver(self, value):
        """
        测试是否包含 driver 属性
        """
        custom_config = ConfigConvertSetting(config_path=value,
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
                          for (let attr of [
                            "cdc_adoQpoasnfa76pfcZLmcfl_Array",
                            "cdc_adoQpoasnfa76pfcZLmcfl_Promise",
                            "cdc_adoQpoasnfa76pfcZLmcfl_Symbol",
                        ]) {
                            if (attr in window) {
                                return true;
                            }
                        }
                    
                        for (let attr of [
                            "$cdc_asdjflasutopfhvcZLmcfl_",
                            "$chrome_asyncScriptInfo",
                        ]) {
                            if (attr in document) {
                                return true;
                            }
                        }
                    
                        return false;
                       }
                       return func();
                   '''
        value = self.driver.execute_script(script)

        print("是否包含 chrome driver 属性:", value)
        assert value is False

        self.driver.close()
        self.driver.quit()
