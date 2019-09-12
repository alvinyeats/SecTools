import os
import logging
import time
import subprocess

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Account(object):
    """
    账号模块，用于提供检索用的账号关键字
    """

    def __init__(self):
        self.domain_path = os.path.join('resources', 'domain_accounts.txt')
        self.local_path = os.path.join('resources', 'local_accounts.txt')
        self.domain_accounts = []
        self.local_accounts = []

    def update_domain(self):
        start = time.time()

        # 获取域账号列表
        result = subprocess.Popen('net users /domain', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result_lines = result.stdout.readlines()
        with open(self.domain_path, 'w') as f:
            for line in result_lines:
                line = line.decode('gbk').strip()
                # windows自带的输出提示里也有空格（1个），这些是我们不需要的，域账号之间的空格超过两个，
                # 故用双空格来判断是否是我们想要的输出行
                if '  ' in line:
                    line_domains = [d for d in line.split() if d]
                    for domain in line_domains:
                        f.write(domain)

        end = time.time()
        logger.info(f'update domain accounts success, time spend: {end - start}s')

    def data_init(self):
        # 读取域账号文件
        with open(self.domain_path, 'r') as fr:
            for line in fr:
                line = line.strip()
                if line:
                    self.domain_accounts.append(line)

        # 读取本地账号文件
        with open(self.local_path, 'r') as fr:
            for line in fr:
                line = line.strip()
                if line:
                    self.local_accounts.append(line)

        logger.info(f'data init success, domains: {len(self.domain_accounts)}, locals: {len(self.local_accounts)}')

    def get_domain(self):
        return self.domain_accounts

    def get_local(self):
        """获取常见本地账号，如root, admin等"""
        return self.local_accounts

    def get_accounts(self):
        return self.domain_accounts + self.local_accounts




