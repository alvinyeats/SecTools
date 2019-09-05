
class Detector(object):

    def __init__(self, strategy):
        self.strategy = strategy

    def is_leak(self, f_path):
        return self.strategy.check(f_path)

