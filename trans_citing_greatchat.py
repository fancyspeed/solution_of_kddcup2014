p_outcome = '../raw_data/outcomes.csv'

p_e2 = './outcomes_nochat.csv'
p_e3 = './outcomes_chat.csv'

idx = 5

fe2 = open(p_e2, 'w')
fe3 = open(p_e3, 'w')
n_origin = 0
n_change = 0
with open(p_outcome) as fe:
    l = fe.readline()
    print l.strip().split(',')[idx]
    fe2.write(l)
    fe3.write(l)

    for line in fe:
        row = line.strip().split(',')
        label_y = row[1]
        n_origin += 1 if label_y=='t' else 0

        label_p = 't' if ''.join(row[2:6]).count('t') == 4 and ''.join(row[6:9]).count('t') >= 1 else 'f'
        if label_y != label_p: print line 

        label_y3 = 't' if row[idx] == 't' else 'f' 
        fe3.write('%s,%s\n' % (row[0], label_y3))
        
        row[idx]='t'
        label_y2 = 't' if ''.join(row[2:6]).count('t') == 4 and ''.join(row[6:9]).count('t') >= 1 else 'f'
        fe2.write('%s,%s\n' % (row[0], label_y2))
        n_change += 1 if label_y2!=label_y else 0


fe2.close()
fe3.close()

print 'origin', n_origin
print 'changed', n_change
