import os
import shutil
import concurrent.futures

from .account import Account
from .collector import Collector
from .strategy import StrategyFactory
from .remote import Remote


class Searcher(object):

    def __init__(self):
        self.account = Account()
        self.remote = Remote()
        self.collector = Collector()
        self.s_fac = StrategyFactory()

        self.query_mode = None  # ext or name
        self.query_args = None   # ('.text', '.docx') or 'sdk.jar', 'passwd.txt' and so on
        self.excludes = None
        self.output = ''
        self.max_workers = 5

    def init_keywords(self):
        self.account.data_init()
        keywords = self.account.get_accounts()
        self.s_fac.set_keywords(keywords)

    def set_auth(self, username, password):
        self.remote.set_auth(username, password)

    def set_query(self, mode, args):
        self.query_mode = mode
        self.query_args = args

    def set_excludes(self, words):
        self.excludes = words

    def set_output(self, dir_name):
        self.output = dir_name

    def copy_file(self, data):
        src = data.split(': ')[1]
        paths = src.split('\\')
        dst = os.path.join(os.path.join(self.output, fr'{paths[2]}'), paths[-1])
        shutil.copyfile(src, dst)

    def reset_before_search(self):
        self.collector.delete_search_results()

    def search_name(self, root, filename, excludes=None):
        self.collector.set_root(root)
        if excludes:
            self.collector.set_exclude(excludes)
        self.collector.search_by_name(filename)
        return self.collector.get_files()

    def search_extension(self, root, extensions, excludes=None):
        self.collector.set_root(root)
        if excludes:
            self.collector.set_exclude(excludes)
        self.collector.search_by_extension(extensions)
        return self.collector.get_files()

    def filter_extension(self, files):
        result = []
        for ext, fps in files.items():
            self.s_fac.set_strategy(ext)

            # 多线程
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(self.max_workers, len(fps))) as executor:
                future_to_file = {executor.submit(self.s_fac.is_danger, fp): fp for fp in fps}
                for future in concurrent.futures.as_completed(future_to_file):
                    try:
                        data = future.result(timeout=60)
                    except concurrent.futures.TimeoutError:
                        data = False
                    if data:
                        result.append(data)

        return result

    def connect(self, ip):
        self.remote.login(ip)

    def get_roots(self, ip):
        return self.remote.get_roots(ip)

    def disconnect(self, ip):
        self.remote.logout(ip)

    def process_single_ip(self, ip):
        self.disconnect(ip)
        self.connect(ip)
        roots = self.get_roots(ip)

        danger_files_dir = os.path.join(self.output, ip)
        if not os.path.exists(danger_files_dir):
            os.mkdir(danger_files_dir)

        if self.query_mode == 'ext':
            danger_paths = []
            for root in roots:
                self.reset_before_search()
                files = self.search_extension(root, self.query_args, excludes=self.excludes)
                danger_paths += self.filter_extension(files)

                with open(os.path.join(self.output, f'{ip}.txt'), 'w') as f:
                    for path in danger_paths:
                        f.write(path + '\n')
                        self.copy_file(path)

        if self.query_mode == 'name':
            target_paths = []
            for root in roots:
                self.search_name(root, self.query_args)
            return target_paths




