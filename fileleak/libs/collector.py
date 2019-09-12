import os
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Collector(object):

    def __init__(self):
        self.root = ''
        self.counter = 0
        self.files = {}
        self.excludes = []
        self.max_size_k = 1000

    def set_root(self, dir_name):
        self.root = dir_name

    def set_exclude(self, dir_list):
        """set exclude dir name list"""
        self.excludes = dir_list

    def delete_search_results(self):
        self.files = {}

    def _add(self, ext, path):
        if ext not in self.files:
            self.files[ext] = [path]
        else:
            self.files[ext].append(path)
        self.counter += 1

    def search_by_extension(self, f_extension):
        """
        search files by file extension, for example:
        str args: '.txt'
        tuple args: ('.txt', '.docx')
        :param f_extension:
        :return:
        """
        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if (d.lower() not in self.excludes) and not d.startswith('.')]
            for file in files:
                if file.endswith(f_extension):
                    _, c_extension = os.path.splitext(file)
                    self._add(c_extension, os.path.join(root, file))

    def search_by_name(self, f_name):
        """
        search files by file type, for example:
        str args: '.txt'
        tuple args: ('.txt', '.docx')
        :param f_name:
        :return:
        """
        for root, dirs, files in os.walk(self.root):
            if f_name in files:
                self._add(f_name, os.path.join(root, f_name))

    def get_files(self):
        logger.info(f'matched files count: {self.counter}')
        return self.files



