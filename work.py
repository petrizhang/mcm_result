import random
import os
from list_state import stat
from scratch import multi_down
from scratch import set_states
from scratch import down


# 列举文件夹内的文件,去掉指定后缀,返回文件名的集合
def list_as_sets(directory: str, appendix: str) -> set:
    files = os.popen('ls %s' % directory).readlines()
    files = [i.rstrip('.%s\n' % appendix) for i in files]
    return set([int(i) for i in files])


def find_broken_teams():
    # 首先列举pdf文件夹内的文件
    pdfs = list_as_sets('pdf', 'pdf')
    # 然后列举已经转换成成功的text文件
    txts = list_as_sets('text', 'txt')
    # 两集合的差集表示pdf文件破损的队伍号
    broken_teams = pdfs - txts
    # 为文件破损的队伍更新状态
    set_states(broken_teams, 'broken')
    return broken_teams


def repair_broken(broken_teams: list):
    # 然后爬错误文件的数据
    broken_teams = list(find_broken_teams())
    random.shuffle(broken_teams)
    for team in broken_teams:
        down(team)

    # 使用新数据重新生成txt
    print("----There is %s broken pdf files.----" % len(broken_teams))
    print('Excuting pdftotext...')
    for team in broken_teams:
        print(('Excuting pdftotext pdf/%s.pdf text/%s.txt' % (team, team)))
        os.system('pdftotext pdf/%s.pdf text/%s.txt' % (team, team))


if __name__ == '__main__':
    pdfs = list_as_sets('pdf', 'pdf')
    set_states(pdfs, 'ok')
    total = stat()
    while total < 12466:
        teams = (list(range(42000, 55000)))
        random.shuffle(teams)
        multi_down(teams, to_deal_unknown=True)
        total = stat()
    broken_teams = find_broken_teams()
    while broken_teams:
        repair_broken(broken_teams)
        broken_teams = find_broken_teams()
