import pandas as pd
import numpy as np
import os.path


def stat():
    all_ok, all_notfound, all_others, all_total = (0, 0, 0, 0)
    i = 1
    while True:
        f = "state/state%s.txt" % i
        if not os.path.exists(f):
            break
        state = pd.read_csv(f, index_col=0, header=0, names=['num', 'state'])
        state = state['state'].values
        ok = np.sum(state == 'ok')
        notfound = np.sum(state == 'notfound')
        others = np.sum(np.all([[state != 'ok'], [state != 'notfound']], axis=0))
        total = ok + notfound + others
        cur_accuracy = float(ok + notfound) / float(total)
        all_ok += ok
        all_notfound += notfound
        all_others += others
        all_total += total
        print('------------From %s to %s------------' % (i * 10000, i * 10000 + 10000))
        print('%5d items have been retrieved.' % ok)
        print('%5d items have been determined not exist.' % notfound)
        print("%5d items' state are not sure." % others)
        print("%3.1f%% is sure." % (cur_accuracy * 100))
        print('%5d toltal items.' % total)
        i += 1

    print('------------      Total        ------------')
    print('%5d items have been retrieved.' % all_ok)
    print('%5d items have been determined not exist.' % all_notfound)
    print("%5d items' state are not sure." % all_others)
    print('%5d toltal items.' % all_total)

    return all_ok

if __name__ == "__main__":
    stat()
