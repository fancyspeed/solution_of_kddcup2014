import sys
import csv

cat_start = 20130101
cat_end = 20130512
dog_start = 20130701
dog_end = 20131112

eid_date = {}
origin_cat = 0
origin_dog = 0
with open('../raw_data/projects.csv') as fin:
    fin.readline()
    for line in fin:
        row = line.strip().split(',')
        eid, date = row[0], int(row[-1].replace('-', ''))
        if date >= cat_start and date <= cat_end:
            eid_date[eid] = date
            origin_cat+=1
        if date >= dog_start and date <= dog_end:
            eid_date[eid] = date
            origin_dog+=1
print 'cat origin', origin_cat
print 'dog origin', origin_dog

eid_label = {}
with open('../raw_data/outcomes.csv') as fin:
    fin.readline()
    for line in fin:
        row = line.strip().split(',')
        eid = row[0]
        label = 1 if row[1]=='t' else 0
        eid_label[eid] = label

change_cat = 0
change_dog = 0
with open('../raw_data/donations.csv') as fin:
    ff = csv.reader(fin)
    ff.next()
    for row in ff:
        eid = row[1]
        if eid not in eid_date: continue
        date0 = eid_date[eid]
        date = int(row[7].split(' ')[0].replace('-', ''))
        if date0 >= cat_start and date0 <= cat_end and date > cat_end and eid_label[eid] == 1:
            change_cat += 1
            eid_label[eid] = 0
        elif date0 >= dog_start and date0 <= dog_end and date > dog_end and eid_label[eid] == 1:
            change_dog += 1
            eid_label[eid] = 0
print 'cat changed', change_cat
print 'dog changed', change_dog

with open('./outcomes_filt.csv', 'w') as fo:
    fo.write('projectid,is_exciting\n')
    for eid in eid_date:
        fo.write('%s,%s\n' % (eid, 't' if eid_label[eid] else 'f'))

    

