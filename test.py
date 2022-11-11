from helper.util import get_driver, sleep
import pytest
import warnings

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # 测试 device-motion todo 需要手动去测试，因为需要晃动设备
    # pytest.main(["-s", "-v", "testcase/test_devicemotion.py"])

    # 测试 ja3
    # pytest.main(["-s", "-v", "--report=ssl.html", '--template=2', "testcase/test_ssl.py"])

    # 测试 document iframe 里的 referer
    # pytest.main(["-s", "-v", "--report=document.html", '--template=2', "testcase/test_document_iframe.py"])

    # 测试 rect
    # pytest.main(["-s", "-v", "--report=rect.html", '--template=2', "testcase/test_rect.py"])

    pytest.main(["-s", "-v", "--report=webrtc.html", '--template=2', "testcase/test_webrtc.py"])

