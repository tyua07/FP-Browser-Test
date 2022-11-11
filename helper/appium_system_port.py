import threading
from helper.port import Port


class AppiumSystemPort(Port):
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, *args, **kwargs):
        with AppiumSystemPort._instance_lock:
            if not hasattr(AppiumSystemPort, "_instance"):
                AppiumSystemPort._instance = AppiumSystemPort(*args, **kwargs)
        return AppiumSystemPort._instance
