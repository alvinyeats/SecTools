import subprocess
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Remote(object):

    def __init__(self):
        self.username = ''
        self.password = ''

    def set_auth(self, username, password):
        self.username = username
        self.password = password

    def login(self, ip):
        result = subprocess.Popen(fr'net use \\{ip} /user:{self.username} {self.password}',
                                  shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logger.info(result.stdout.read().decode('gbk').strip().replace('\r\n', ''))

    def get_roots(self, ip):
        c = f'\\\\{ip}\\C$\\Users\\'
        # d = f'\\\\{self.ip}\\D$\\'
        # e = f'\\\\{self.ip}\\E$\\'
        return [c]

    def logout(self, ip):
        result = subprocess.Popen(fr'net use \\{ip} /delete',
                                  shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logger.info(result.stdout.read().decode('gbk').strip())


