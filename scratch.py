# /usr/bin/python3
import socket
from urllib import request
from urllib.error import URLError
import pandas as pd
import threading
import queue
import os.path
import time

_MAX_STATE = 8
_states = []
_last_update_time = time.time()  # 上次更新状态文件的时间
_statefile_update_interval = 1000  # 状态文件更新间隔，单位秒

socket.setdefaulttimeout(10)

for i in range(_MAX_STATE):
    state_filename = 'state/state%s.txt' % i
    if not os.path.exists(state_filename):
        state = pd.Series(index=range(i * 10000, i * 10000 + 10000))
        state[:] = 'none'
        state.name = 'state'
        state.index.name = 'num'
        state.to_csv(state_filename, header=True)
    else:
        state = pd.read_csv(state_filename, index_col=0, header=0, names=['num', 'state'])
        state = state['state']
    _states.append(state)



# 多线程类
class Download(threading.Thread):
    def __init__(self, t_queue):
        threading.Thread.__init__(self)
        self.que = t_queue

    def run(self):
        while True:
            if not self.que.empty():
                down(self.que.get())
            else:
                break


# 设置指定队伍的状态并且立即更新状态文件
def set_states(team_nums: list, state_code: str):
    global _states
    for i in range(_MAX_STATE):
        filename = 'state/state%s.txt' % i
        state = _states[i]
        transform = state[team_nums]
        indexes = transform[transform.notnull()].index
        state[indexes] = state_code
        state.to_csv(filename, header=True)


# 下载一个队伍的证书并更新状态并且完成状态文件更新的工作
def down(team_num: int, update_in_place=False):
    global _last_update_time
    global _states
    now = time.time()
    # 如果就地更新状态参数为真或到达写入间隔
    if update_in_place or now - _last_update_time > _statefile_update_interval:
        _last_update_time = now
        print('Writing csv...')
        # 更新所有state文件
        for i in range(_MAX_STATE):
            filename = 'state/state%s.txt' % i
            _states[i].to_csv(filename, header=True)
    url = 'http://www.comap-math.com/mcm/2016Certs/%s.pdf' % team_num
    cur_state = _states[team_num // 10000]
    if cur_state[team_num] == 'ok':  # or state[team_num] == 'notfound':
        print('......skip %s' % team_num)
        return
    try:
        request.urlretrieve(url, 'pdf/%s.pdf' % team_num)
        cur_state[team_num] = 'ok'
    except ConnectionResetError as e:
        cur_state[team_num] = 'reset'
    except URLError as e:
        if hasattr(e, 'code'):
            if e.code == 404:
                cur_state[team_num] = 'notfound'
            else:
                cur_state[team_num] = str(e)
        else:
            cur_state[team_num] = str(e)
    except socket.timeout:
        cur_state[team_num] = 'timeout'
    except Exception as e:
        cur_state[team_num] = str(e)
    finally:
        print('%s:%s' % (team_num, cur_state[team_num]))


# 处理未知状态(非ok且非notfound)的队伍
def _deal_unknown():
    print("----------Deal with unknown items---------")
    state_dump = state[state != 'ok']
    state_dump = state_dump[state_dump != 'notfound']
    unknown_teams = state_dump.index
    for team_num in unknown_teams:
        down(team_num)


# 使用多线程下载low~high队伍号的队伍证书，默认线程数20
def multi_down(teams:list, thread_nums: int = 20, timeout=5, to_deal_unknown=False):
    global que
    socket.setdefaulttimeout(timeout)
    que = queue.Queue()
    for i in teams:
        que.put(i)
    threads = [Download(que) for i in range(thread_nums)]
    for d in threads:
        d.start()
    while True:
        if que.empty():
            if to_deal_unknown:
                _deal_unknown()
            break



