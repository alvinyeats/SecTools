import concurrent.futures
from libs.searcher import Searcher

EXCLUDES = [w.lower() for w in ['$Recycle.Bin', 'Program Files', 'Program Files (x86)', 'ProgramData', 'Windows',
            'AppData', 'Go', 'WXWork', 'MicrosoftEdgeBackups', 'WeChat Files', 'Downloads', '']]
OUTPUT = 'results'


def process_file_name():
    search = Searcher()
    root_path = r'C:'
    target_name = 'a.txt'
    return search.search_name(root_path, target_name)


def process_file_extension(ip_list, username, password):
    search = Searcher()
    search.init_keywords()
    search.set_query('ext', ('.txt', '.xlsx', 'xlsx'))
    search.set_excludes(EXCLUDES)
    search.set_output(OUTPUT)
    search.set_auth(username, password)

    with concurrent.futures.ProcessPoolExecutor(max_workers=min(5, len(ip_list))) as executor:
        executor.map(search.process_single_ip, ip_list)


if __name__ == "__main__":
    un = r'google\admin'
    pw = '123456'
    ips = ['1.1.1.1', '2.2.2.2', '3.3.3.3']
    process_file_extension(ips, un, pw)
