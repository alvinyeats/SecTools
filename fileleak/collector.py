import os


class Collector(object):

    def __init__(self):
        self.root = ''
        self.files = {}

    def set_root(self, dir_name):
        self.root = dir_name

    def _add(self, key, value):
        if key not in self.files:
            self.files[key] = [value]
        else:
            self.files[key].append(value)

    def search_by_extension(self, f_extension):
        """
        search files by file extension, for example:
        str args: '.txt'
        tuple args: ('.txt', '.docx')
        :param f_extension:
        :return:
        """
        for root, dirs, files in os.walk(self.root):
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
        return self.files

    def print_files(self):
        print(self.files)


if __name__ == "__main__":
    c = Collector()
    c.set_root(r'C:\Users\Desktop')
    c.search_by_name('a.txt')
    c.search_by_extension(('.txt', '.docx'))
    c.print_files()
