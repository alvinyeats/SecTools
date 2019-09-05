from abc import abstractmethod

from docx import Document
from xlrd import open_workbook


class Strategy(object):

    @abstractmethod
    def check(self, f_path):
        pass

    @abstractmethod
    def get_supports(self):
        pass


class TextStrategy(Strategy):
    """
    文本文件检测策略
    """
    def __init__(self, keywords):
        self.keywords = keywords
        self.supports = ['.txt', '.config', '.conf']

    def get_supports(self):
        return self.supports

    def check(self, f_path):
        with open(f_path, 'r') as f:
            for k in self.keywords:
                if k in f.read():
                    return True
        return False


class WordStrategy(Strategy):
    """
    word文件检测策略
    """
    def __init__(self, keywords):
        self.keywords = keywords
        self.supports = ['.doc', '.docx']

    def get_supports(self):
        return self.supports

    def check(self, f_path):
        doc = Document(f_path)
        for para in doc.paragraphs:
            for k in self.keywords:
                if k in para.text:
                    return True
        return False


class ExcelStrategy(Strategy):
    """
    excel文件检测策略
    """
    def __init__(self, keywords):
        self.keywords = keywords
        self.supports = ['.xls', '.xlsx']

    def get_supports(self):
        return self.supports

    def check(self, f_path):
        book = open_workbook(f_path)
        for sheet in book.sheets():
            for r_id in range(sheet.nrows):
                row = sheet.row(r_id)
                for cell in row:
                    for k in self.keywords:
                        if k in cell.value:
                            return True
        return False

