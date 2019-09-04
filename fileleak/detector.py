import docx


class TextStrategy(object):
    """
    文本文件检测策略
    """
    def __init__(self, keywords):
        self.keywords = keywords

    def is_leak(self, f_path):
        with open(f_path, 'r') as f:
            for k in self.keywords:
                if k in f.read():
                    return True
        return False


class WordStrategy(object):
    """
    word文件检测策略
    """
    def __init__(self, keywords):
        self.keywords = keywords

    def is_leak(self, f_path):
        pass


class ExcelStrategy(object):
    """
    excel文件检测策略
    """
    def __init__(self, keywords):
        self.keywords = keywords

    def is_leak(self, f_path, keywords):
        with open(f_path, 'r') as fr:
            for line in fr:
                for k in keywords:
                    if k in line:
                        return True
        return False


class Detector(object):

    def __init__(self, strategy):
        self.strategy = strategy

    def is_leak(self, f_path):
        return self.strategy.is_leak(f_path, )

