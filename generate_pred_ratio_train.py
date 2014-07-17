import sys
if len(sys.argv) != 5:
    print '<usage> pred label project out'
    exit(1)

eid_dict = {}
with open(sys.argv[2]) as fin:
    fin.readline()
    for line in fin:
        row = line.strip().split(',')
        eid = row[0]
        eid_dict[eid] = 1

eid_date = {}
mind, maxd = 1000000, 0 
with open(sys.argv[3]) as fin:
    fin.readline()
    for line in fin:
        row = line.strip().split(',')
        eid, date = row[0], row[-1]
        if eid not in eid_dict: continue
        month, day = int(date[5:7]), int(date[-2:])
        date = month*31 + day
        eid_date[eid] = date
        mind = min(mind, date)
        maxd = max(maxd, date)

fo = open(sys.argv[4], 'w')
fps = []
for i in range(3):
    fps.append(open(sys.argv[1]+str(i)))
with open(sys.argv[2]) as fin:
    fin.readline()
    for line in fin:
        row = line.strip().split(',')
        eid, label = row[0], row[1]
        pred0 = fps[0].readline().strip()
        pred1 = fps[1].readline().strip()
        pred2 = fps[2].readline().strip()
        date_score = (eid_date[eid] - mind) / (maxd - mind + 1.)
        fo.write('%s %s:%s %s:%s %s:%s %s:%s\n' % (label, 0, date_score, 1, pred0, 2, pred1, 3, pred2))
for i in range(3):
    fps[i].close()
fo.close()
