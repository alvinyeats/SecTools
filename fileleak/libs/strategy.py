import shutil
import re
from abc import abstractmethod
import logging.config

from docx import Document
from xlrd import open_workbook

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger(__name__)


class Strategy(object):

    @abstractmethod
    def find(self, f_path, keywords):
        pass

    @abstractmethod
    def get_supports(self):
        pass


class TextStrategy(Strategy):
    """
    文本文件检测策略
    """
    def __init__(self):
        self.supports = ['.txt', '.config', '.conf']
        self.max_size_k = 500

    def get_supports(self):
        return self.supports

    def find(self, f_path, keywords):
        try:
            with open(f_path, 'r') as f:
                for line in f:
                    for k in keywords:
                        if re.search(k, line, re.IGNORECASE):
                            logger.warning(f'Bad: ({k}) {f_path}')
                            return k
        except Exception as e:
            logger.debug(f'Forbidden: {f_path}, {e}')
        else:
            logger.info(f'Good: {f_path}')
        return False


class WordStrategy(Strategy):
    """
    word文件检测策略
    """
    def __init__(self):
        self.supports = ['.doc', '.docx']
        self.max_size_k = 1000

    def get_supports(self):
        return self.supports

    def find(self, f_path, keywords):
        try:
            doc = Document(f_path)
            for para in doc.paragraphs:
                for k in keywords:
                    if k in para.text.lower():
                        logger.warning(f'Bad: ({k}) {f_path}')
                        return k
        except Exception as e:
            logger.debug(f'Forbidden: {f_path}, {e}')
        else:
            logger.info(f'Good: {f_path}')
        return False


class ExcelStrategy(Strategy):
    """
    excel文件检测策略
    """
    def __init__(self):
        self.supports = ['.xls', '.xlsx']
        self.max_size_k = 1000

    def get_supports(self):
        return self.supports

    def find(self, f_path, keywords):
        try:
            book = open_workbook(f_path)
            for sheet in book.sheets():
                for r_id in range(sheet.nrows):
                    row = sheet.row(r_id)
                    for cell in row:
                        for k in keywords:
                            if k in str(cell.value).lower():
                                logger.warning(f'Bad: ({k}) {f_path}')
                                return k
        except Exception as e:
            logger.debug(f'Forbidden: {f_path}, {e}')
        else:
            logger.info(f'Good: {f_path}')
        return False


class StrategyFactory(object):

    def __init__(self):
        self.keywords = []
        self.strategy = None

    def set_keywords(self, keywords):
        self.keywords = keywords

    def set_strategy(self, extension):
        if extension in ['.txt', '.config', '.conf']:
            self.strategy = TextStrategy()
        elif extension in ['.doc', '.docx']:
            self.strategy = WordStrategy()
        elif extension in ['.xls', '.xlsx']:
            self.strategy = ExcelStrategy()

    def is_danger(self, path):
        find_result = self.strategy.find(path, self.keywords)
        if find_result:
            return f'({find_result}): {path}'
        else:
            return False


