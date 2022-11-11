import threading
from helper.port import Port


class AppiumPort(Port):
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, *args, **kwargs):
        with AppiumPort._instance_lock:
            if not hasattr(AppiumPort, "_instance"):
                AppiumPort._instance = AppiumPort(*args, **kwargs)
        return AppiumPort._instance
