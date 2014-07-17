import csv

p_outcome = '../raw_data/outcomes.csv'
p_project = '../raw_data/projects.csv'
p_essay = '../raw_data/essays.csv'
p_donation = '../raw_data/donations.csv'
p_submit = '../raw_data/sampleSubmission.csv'

p_e2 = './outcomes_duration.csv'

plast_dict = {} 
with open(p_donation, 'rb') as f:
        import time
        cin = csv.reader(f)
        header = cin.next()
        head_dict = {v:i for i, v in enumerate(header)}
        for row in cin:
            pid = row[head_dict['projectid']]
            ts = row[head_dict['donation_timestamp']]
            if not ts: continue
            a = ts.split(' ')[0].split('-')
            lt = time.mktime([int(v) for v in a] + [0]*6)
            plast_dict[pid] = max(lt, plast_dict.get(pid, 0))

ppost_dict = {}
with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        header = cin.next()
        head_dict = {v:i for i, v in enumerate(header)}
        for row in cin:
            eid = row[0]
            ts = row[head_dict['date_posted']]
            if not ts: continue

            a = ts.split('-')
            lt = time.mktime([int(v) for v in a] + [0]*6)
            ppost_dict[eid] = lt

fe2 = open(p_e2, 'w')
mind, maxd = 9999, 0
with open(p_outcome) as fe:
    l = fe.readline()
    fe2.write(l)

    for line in fe:
        row = line.strip().split(',')
        label_y = row[1]
        label_p = 't' if ''.join(row[2:6]).count('t') == 4 and ''.join(row[6:9]).count('t') >= 1 else 'f'
        pid = row[0]
        diff = 9999 
        if label_y=='t' and pid in plast_dict and pid in ppost_dict:
            diff = (plast_dict[pid] - ppost_dict[pid])/86400
            mind = min(mind, diff)
            maxd = max(maxd, diff)
        fe2.write('%s,%s,%s\n' % (row[0], label_y, diff))
fe2.close()
print mind, maxd
