class Context(object):
    def __init__(self, driver):
        self.driver = driver

        self.contexts = self.driver.contexts

        self.original_context = self.driver.context
        self.original_window = self.driver.current_window_handle

    # 设置为原生
    def native(self):
        for ctx in self.contexts:
            if ctx == 'NATIVE_APP':
                self.driver.switch_to.context(ctx)
                break

    # 还原上下文
    def reduction(self):
        self.driver.switch_to.context(self.original_context)

        # 切换到最新的一个 window 对象
        if self.original_window:
            self.driver.switch_to.window(self.original_window)
