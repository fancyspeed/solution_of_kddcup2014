#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Steven

import os
import sys

import csv
import math
import random

#import numpy as np
#import pandas as pd

from datetime import *

rerank_coef = 1.0

pro_dict = {}
projects = csv.reader(file('../raw_data/projects.csv', 'rb'))
projects.next()
for row in projects:
    pid = row[0]
    pts = row[-1]
    pro_dict[pid] = pts
print 'len(pro_dict) =', len(pro_dict)




cnt = 0
cnt1 = 0
cnt2 = 0
cnt3 = 0
cnt4 = 0
cnt5 = 0



rank_dict ={}
submit = csv.reader(file('libfm.csv'))
submit.next()
for row in submit:
    rank_dict[row[0]] = float(row[1])


sort_list = sorted(rank_dict.items(), key = lambda x:-x[1])
for pid, score in sort_list:
    cnt += 1
    dt = pro_dict[pid]
    #submit3.writerow([pid, score])
    reranking = score
    if dt.find('2014-01') >= 0:
        cnt1 += 1
    if dt.find('2014-02') >= 0:
        cnt2 += 1
    if dt.find('2014-03') >= 0:
        cnt3 += 1
    if dt.find('2014-04') >= 0:
        cnt4 += 1
    if dt.find('2014-05') >= 0:
        cnt5 += 1

    if cnt % 4000 == 0:
        print 'after reranking 2014-01-01 -> 2014-05-13', cnt
        print 'month 1 =', cnt1, 'proportion =', cnt1/float(cnt)
        print 'month 2 =', cnt2, 'proportion =', cnt2/float(cnt)
        print 'month 3 =', cnt3, 'proportion =', cnt3/float(cnt)
        print 'month 4 =', cnt4, 'proportion =', cnt4/float(cnt)
        print 'month 5 =', cnt5, 'proportion =', cnt5/float(cnt)


