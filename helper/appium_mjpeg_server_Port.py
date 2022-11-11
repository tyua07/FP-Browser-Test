import threading
from helper.port import Port


class AppiumMjpegServerPort(Port):
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, *args, **kwargs):
        with AppiumMjpegServerPort._instance_lock:
            if not hasattr(AppiumMjpegServerPort, "_instance"):
                AppiumMjpegServerPort._instance = AppiumMjpegServerPort(*args, **kwargs)
        return AppiumMjpegServerPort._instance
