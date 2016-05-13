import pandas as pd
import os
import re

pattern = re.compile(r'[\s\S]*Be It Known That The Team Of(?P<name>[\s\S]*)With Faculty Advisor(?P<advisor>[\s\S]*?)Of'
                     r'(?P<school>[\s\S]*)Was Designated As(?P<award>[\s\S]*)Administered by[\s\S]*')


def line_counts():
    lines_map_counts = {}
    lines_map_filenames = {}
    files = os.popen('ls text').readlines()
    for filename in files:
        with open("text/%s" % filename.rstrip(), 'r') as f:
            contents_list = f.readlines()
            lines = len(contents_list)
            lines_map_counts.setdefault(lines, 0)
            lines_map_filenames.setdefault(lines, [])
            lines_map_filenames[lines].append(filename)
            lines_map_counts[lines] += 1
    print(lines_map_counts)
    for k, v in lines_map_filenames.items():
        print('%s:%s' % (k, v[0].strip()))


def extract_data():
    data = []
    index = []
    files = os.popen('ls text').readlines()
    for filename in files:
        with open("text/%s" % filename.strip(), 'r') as f:
            contents = ''.join(f.readlines())
            m = re.match(pattern, contents)
            if not m:
                os.system('pdftotext pdf/%s.pdf text/%s' % (filename.rstrip('.txt\n'), filename))
                print(filename)
                print(contents)
                continue
            match_dict = m.groupdict()
            for k in match_dict:
                match_dict[k] = match_dict[k].strip()
            index.append(filename.rstrip('.txt\n'))
            data.append(match_dict)
    frame = pd.DataFrame(data, index=index, dtype=str)
    frame.index.name = 'team'
    return frame

frame = extract_data()
frame.to_csv('data.csv', header=True)
