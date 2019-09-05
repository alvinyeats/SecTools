
from account import Account
from collector import Collector
from strategy import TextStrategy, WordStrategy, ExcelStrategy


def find_leak():
    account = Account()
    account.update()
    keywords = account.get_accounts()

    collector = Collector()
    collector.set_root(r'C:\Users\wyr13087\Desktop')
    target_extensions = ('.txt', '.docx')
    collector.search_by_extension(target_extensions)
    files = collector.get_files()

    print(files)
    ts = TextStrategy(keywords)
    ws = WordStrategy(keywords)
    es = ExcelStrategy(keywords)
    result = []
    for ext, paths in files.items():
        if ext in ts.get_supports():
            for path in paths:
                if ts.check(path):
                    result.append(path)
        if ext in ws.get_supports():
            for path in paths:
                if ws.check(path):
                    result.append(path)
        if ext in es.get_supports():
            for path in paths:
                if es.check(path):
                    result.append(path)
    print(result)


if __name__ == "__main__":
    find_leak()
