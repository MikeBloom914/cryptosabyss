#!usr/bin/env python3

import csv
import pandas as pd
import os

kens = []
string = '.py'
with open('chartinfo.csv', 'r') as f:
    rows = csv.reader(f)
    next(rows, None)
    for row in rows:
        kens.append(row[2])
filelist = [x + string for x in kens]

print(filelist)
print(len(filelist))

os.system('touch run.sh')
with open('run.sh', 'w') as g:
    writer = csv.writer(g)
    for i in filelist:
        writer.writerow(['python3 {i}'.format(i=i)])
