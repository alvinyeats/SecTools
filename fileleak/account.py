import time
import subprocess


class Account(object):
    """
    账号模块，用于提供检索用的账号关键字
    """

    def __init__(self):
        self.domain_accounts = []
        self.local_accounts = []

    def update(self):
        start = time.time()

        # 获取域账号列表
        result = subprocess.Popen('net users /domain', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result_lines = result.stdout.readlines()
        for line in result_lines:
            line = line.decode('gbk').strip()
            # windows自带的输出提示里也有空格（1个），这些是我们不需要的，域账号之间的空格超过两个，
            # 故用双空格来判断是否是我们想要的输出行
            if '  ' in line:
                line_domains = [d for d in line.split() if d]
                self.domain_accounts += line_domains

        # 获取本地用户
        with open('local_accounts.txt', 'r') as fr:
            for line in fr:
                line = line.strip()
                if line:
                    self.local_accounts.append(line)

        end = time.time()
        print(f'update spend: {end - start}s')
        print(f'domain accounts: {len(self.domain_accounts)}')
        print(f'local accounts: {len(self.local_accounts)}')

    def get_domain(self):
        return self.domain_accounts

    def get_local(self):
        """获取常见本地账号，如root, admin等"""
        return self.local_accounts

    def get_accounts(self):
        return self.domain_accounts + self.local_accounts

    def print_account(self):
        print("domain accounts: ")
        print(self.domain_accounts)
        print("local accounts:")
        print(self.local_accounts)


if __name__ == '__main__':
    ac = Account()
    ac.update()
    ac.print_account()
