import random
import time
import csv
import re

# only keep instances after from_date
cat_train_from = 20120101
cat_train_to = 20121231
cat_test_from = 20130101
cat_test_to = 20130512

dog_train_from = 20120701
dog_train_to = 20130630
dog_test_from = 20130701
dog_test_to = 20131112

pig_train_from = 20130101
pig_train_to = 20131231
pig_test_from = 20140101
pig_test_to = 20140512

# only keep neg_rate of negative instances
neg_rate =  1 #0.2
# num of folds to split train
n_fold = 3

# raw data
p_outcome = './outcomes.csv'
p_outcome_filt = './outcomes_filt.csv'
p_outcome_duration = './outcomes_duration.csv'
p_outcome_chat = './outcomes_chat.csv'
p_outcome_nochat = './outcomes_nochat.csv'

p_project = '../raw_data/projects.csv'
p_essay = '../raw_data/essays.csv'
p_resource = '../raw_data/resources.csv'
p_submit = '../raw_data/sampleSubmission.csv'

# output
out_dir = './'
p_train_cat = '%s/train_cat.svm' % out_dir
p_test_cat = '%s/test_cat.svm' % out_dir
p_label_cat = '%s/test_cat.label' % out_dir
p_train_dog = '%s/train_dog.svm' % out_dir
p_test_dog = '%s/test_dog.svm' % out_dir
p_label_dog = '%s/test_dog.label' % out_dir
p_train_pig = '%s/train_pig.svm' % out_dir
p_test_pig = '%s/test_pig.svm' % out_dir
p_label_pig = '%s/test_pig.label' % out_dir


train_cat, test_cat = {}, {}
train_dog, test_dog = {}, {}
train_pig, test_pig = {}, {}

def load_train_id():
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            date = int(row[-1].replace('-', ''))

            if date >= cat_train_from and date <= cat_train_to:
                train_cat[eid] = [[0,0,0], []]
            if date >= cat_test_from and date <= cat_test_to:
                test_cat[eid] = [0, []]
            if date >= dog_train_from and date <= dog_train_to:
                train_dog[eid] = [[0,0,0], []]
            if date >= dog_test_from and date <= dog_test_to:
                test_dog[eid] = [0, []]
            if date >= pig_train_from and date <= pig_train_to:
                train_pig[eid] = [[0,0,0], []]
            if date >= pig_test_from and date <= pig_test_to:
                test_pig[eid] = [0, []]
def add_train_label():
    fin = open(p_outcome_duration)
    fin.readline()
    for line in fin:
        arr = line.strip().split(',')
        eid = arr[0]
        if arr[1] == 't':
            #label = 1
            label = 0.88 + max(0, 120 - float(arr[2])) / 1000.
        else:
            label = 0 
        if eid in train_cat:
            train_cat[eid][0][0] = label
        if eid in train_dog:
            train_dog[eid][0][0] = label
        if eid in train_pig:
            train_pig[eid][0][0] = label
    fin.close()
    fin = open(p_outcome_chat)
    fin.readline()
    for line in fin:
        arr = line.strip().split(',')
        eid = arr[0]
        if arr[1] == 't':
            label = 1
        else:
            label = 0 
        if eid in train_cat:
            train_cat[eid][0][1] = label
        if eid in train_dog:
            train_dog[eid][0][1] = label
        if eid in train_pig:
            train_pig[eid][0][1] = label
    fin.close()
    fin = open(p_outcome_nochat)
    fin.readline()
    for line in fin:
        arr = line.strip().split(',')
        eid = arr[0]
        if arr[1] == 't':
            label = 1
        else:
            label = 0 
        if eid in train_cat:
            train_cat[eid][0][2] = label
        if eid in train_dog:
            train_dog[eid][0][2] = label
        if eid in train_pig:
            train_pig[eid][0][2] = label
    fin.close()

    fin = open(p_outcome_filt)
    fin.readline()
    for line in fin:
        arr = line.strip().split(',')
        eid = arr[0]
        label = 1 if arr[1]=='t' else 0
        if eid in test_cat:
            test_cat[eid][0] = label
        if eid in test_dog:
            test_dog[eid][0] = label
    fin.close()

def add_default():
    for eid in train_cat:
        train_cat[eid][1] += [(0, 1)]
    for eid in test_cat:
        test_cat[eid][1] += [(0, 1)]
    for eid in train_dog:
        train_dog[eid][1] += [(0, 1)]
    for eid in test_dog:
        test_dog[eid][1] += [(0, 1)]
    for eid in train_pig:
        train_pig[eid][1] += [(0, 1)]
    for eid in test_pig:
        test_pig[eid][1] += [(0, 1)]
def add_feats(eid, feat):
            F_len = feat
            if eid in train_cat:
                train_cat[eid][1] += F_len
            if eid in test_cat:
                test_cat[eid][1] += F_len
            if eid in train_dog:
                train_dog[eid][1] += F_len
            if eid in test_dog:
                test_dog[eid][1] += F_len
            if eid in train_pig:
                train_pig[eid][1] += F_len
            if eid in test_pig:
                test_pig[eid][1] += F_len
def add_essay_len(idx):
    var = [10., 100., 100., 500.]
    with open(p_essay, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[2:]
            n_feat = len(Feat)
            F_len = [(idx+i, int(len(v)/var[i])) for i, v in enumerate(Feat)] 
            add_feats(eid, F_len)
    return idx + n_feat
def add_project_float(idx):
    #0: project id
    #1: teacher id               (string)
    #2-3: school ids            (string)
    #4-5: school location       (float)
    #6-11: school info          (string)
    #12-17: school info         (bool)
    #18: teacher gender Mrs./Mr.(bool)
    #19-20: teacher info        (bool)
    #21-24: course info         (string)
    #25: resource type          (string)
    #26-27: school/grade level  (string) 
    #28: cost      (int)
    #29-30: price      (int)
    #31: students      (int)
    #32-33: eligible            (bool)
    #34: date
    #var = [30., 500., 500., 100.]
    var = [500., 500.]
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[29:31]
            n_feat = len(Feat)
            F_len = [(idx+i, float(v)/var[i]) for i, v in enumerate(Feat) if v] 
            add_feats(eid, F_len)
    return idx + n_feat
def add_project_cost_float(idx):
    #0: project id
    #1: teacher id               (string)
    #2-3: school ids            (string)
    #4-5: school location       (float)
    #6-11: school info          (string)
    #12-17: school info         (bool)
    #18: teacher gender Mrs./Mr.(bool)
    #19-20: teacher info        (bool)
    #21-24: course info         (string)
    #25: resource type          (string)
    #26-27: school/grade level  (string) 
    #28: cost      (int)
    #29-30: price      (int)
    #31: students      (int)
    #32-33: eligible            (bool)
    #34: date
    #var = [30., 500., 500., 100.]
    #var = [500., 500.]
    var = [100.]
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[31:32]
            n_feat = len(Feat)
            F_len = [(idx+i, float(v)/var[i]) for i, v in enumerate(Feat) if v] 
            add_feats(eid, F_len)
    return idx + n_feat
def add_project_school_bool(idx):
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[12:18]
            n_feat = len(Feat)
            F_len = [(idx+i, 1) if v=='t' else (idx+i, 0) for i, v in enumerate(Feat) if v] 
            add_feats(eid, F_len)
    return idx + n_feat
def add_project_teacher_gender(idx):
    #18: teacher gender Mrs./Mr.(bool)
    #19-20: teacher info        (bool)
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            gender = row[18].lower()
            if gender == 'ms.':
                F_len = [(idx, 1)]
            elif gender == 'mrs.':
                F_len = [(idx+1, 1)]
            else:
                F_len = [(idx+2, 1)]
            add_feats(eid, F_len)
    return idx + 3
def add_project_teacher_bool(idx):
    #18: teacher gender Mrs./Mr.(bool)
    #19-20: teacher info        (bool)
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[19:21]
            n_feat = len(Feat)
            F_len = [(idx+i, 1) if v=='t' else (idx+i, 0) for i, v in enumerate(Feat) if v] 
            add_feats(eid, F_len)
    return idx + n_feat
def add_project_eligible_bool(idx):
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[32:34]
            n_feat = len(Feat)
            F_len = [(idx+i, 1) if v.lower() in ('t') else (idx+i, 0) for i, v in enumerate(Feat) if v] 
            add_feats(eid, F_len)
    return idx + n_feat
def add_school_level_str(idx):
    #26-27: school/grade level  (string) 
    stat_dict = {}
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            if eid not in train_dog and eid not in test_dog: continue
            Feat = row[26:27]
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    stat_dict[key] = stat_dict.get(key, 0) + 1
    key_dict = {}
    for key in stat_dict:
        if stat_dict[key] >= 15:
            key_dict[key] = idx
            idx += 1
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[26:27]
            F_len = []
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    if key in key_dict:
                        F_len.append( (key_dict[key], 1) )
            add_feats(eid, F_len)
    return idx
def add_grade_level_str(idx):
    #26-27: school/grade level  (string) 
    stat_dict = {}
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            if eid not in train_dog and eid not in test_dog: continue
            Feat = row[27:28]
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    stat_dict[key] = stat_dict.get(key, 0) + 1
    key_dict = {}
    for key in stat_dict:
        if stat_dict[key] >= 15:
            key_dict[key] = idx
            idx += 1
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[27:28]
            F_len = []
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    if key in key_dict:
                        F_len.append( (key_dict[key], 1) )
            add_feats(eid, F_len)
    return idx
def add_project_weekday_str(idx):
    #34: date
    stat_dict = {}
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            if eid not in train_dog and eid not in test_dog: continue
            #date = row[-1].split('-')[1]
            time_arr = [int(v) for v in row[-1].split('-')] + [0]*6
            date = time.localtime(time.mktime(time_arr)).tm_wday
            Feat = [str(date)] 
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    stat_dict[key] = stat_dict.get(key, 0) + 1
    key_dict = {}
    for key in stat_dict:
        if stat_dict[key] >= 15:
            key_dict[key] = idx
            idx += 1
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            #date = row[-1].split('-')[1]
            time_arr = [int(v) for v in row[-1].split('-')] + [0]*6
            date = time.localtime(time.mktime(time_arr)).tm_wday
            Feat = [str(date)] 
            F_len = []
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    if key in key_dict:
                        F_len.append( (key_dict[key], 1) )
            add_feats(eid, F_len)
    return idx
def add_project_resource_str(idx):
    #25: resource type          (string)
    stat_dict = {}
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            if eid not in train_dog and eid not in test_dog: continue
            Feat = row[25:26]
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    stat_dict[key] = stat_dict.get(key, 0) + 1
    key_dict = {}
    for key in stat_dict:
        if stat_dict[key] >= 15:
            key_dict[key] = idx
            idx += 1
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[25:26]
            F_len = []
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    if key in key_dict:
                        F_len.append( (key_dict[key], 1) )
            add_feats(eid, F_len)
    return idx
def add_project_course_info_str(idx):
    #21-24: course info         (string)
    stat_dict = {}
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            if eid not in train_dog and eid not in test_dog: continue
            Feat = row[22:23]
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    stat_dict[key] = stat_dict.get(key, 0) + 1
    key_dict = {}
    for key in stat_dict:
        if stat_dict[key] >= 15:
            key_dict[key] = idx
            idx += 1
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[22:23]
            F_len = []
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    if key in key_dict:
                        F_len.append( (key_dict[key], 1) )
            add_feats(eid, F_len)
    return idx
def add_teacher_id_str(idx):
    #2-3: school ids            (string)
    stat_dict = {}
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            if eid not in train_dog and eid not in test_dog: continue
            Feat = row[1:2]
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    stat_dict[key] = stat_dict.get(key, 0) + 1
    key_dict = {}
    for key in stat_dict:
        if stat_dict[key] >= 15:
            key_dict[key] = idx
            idx += 1
    with open(p_project, 'rb') as f:
        cin = csv.reader(f)
        cin.next()
        for row in cin:
            eid = row[0]
            Feat = row[1:2]
            F_len = []
            for i, v in enumerate(Feat):
                if v: 
                    key = '%s_%s' % (i, v)
                    if key in key_dict:
                        F_len.append( (key_dict[key], 1) )
            add_feats(eid, F_len)
    return idx


def save_train(test_x, p_test_x):
    ftest = []
    for i in range(3):
        ftest.append(open(p_test_x+str(i), 'w'))
    for eid, pair in test_x.items():
        labels, feat = pair
        for i, label in enumerate(labels):
            ftest[i].write('%s %s\n' % (label, ' '.join(['%s:%s' % (k, v) for k, v in feat])))
    for i in range(3):
        ftest[i].close()
def save_test(test_x, p_test_x, p_label_x):
    ftest = open(p_test_x, 'w')
    flabel = open(p_label_x, 'w')
    flabel.write('Eventid,Label\n')
    for eid, pair in test_x.items():
        label, feat = pair
        ftest.write('%s %s\n' % (label, ' '.join(['%s:%s' % (k, v) for k, v in feat])))
        flabel.write('%s,%s\n' % (eid, label))
    ftest.close()
    flabel.close()


if __name__ == '__main__':
    import sys


    load_train_id()
    add_train_label()

    add_default()
    idx = 1 

    idx = add_essay_len(idx)
    print 'after add_essay_len, max idx:', idx
    idx = add_project_float(idx)
    print 'after add_project_float, max idx:', idx
    idx = add_project_cost_float(idx)
    print 'after add_project_cost_float, max idx:', idx
    idx = add_project_school_bool(idx)
    print 'after add_project_school_bool, max idx:', idx
    idx = add_project_teacher_gender(idx)
    print 'after add_project_teacher_gender, max idx:', idx
    idx = add_project_teacher_bool(idx)
    print 'after add_project_teacher_bool, max idx:', idx
    idx = add_project_eligible_bool(idx)
    print 'after add_project_eligible_bool, max idx:', idx
    idx = add_school_level_str(idx)
    print 'after add_school_level_str, max idx:', idx
    idx = add_grade_level_str(idx)
    print 'after add_grade_level_str, max idx:', idx
    idx = add_project_weekday_str(idx)
    print 'after add_project_weekday_str, max idx:', idx
    idx = add_project_resource_str(idx)
    print 'after add_project_resource_str, max idx:', idx
    idx = add_project_course_info_str(idx)
    print 'after add_project_course_info_str, max idx:', idx
    idx = add_teacher_id_str(idx)
    print 'after add_teacher_id_str, max idx:', idx

    save_train(train_cat, p_train_cat)
    save_test(test_cat, p_test_cat, p_label_cat)
    save_train(train_dog, p_train_dog)
    save_test(test_dog, p_test_dog, p_label_dog)
    save_train(train_dog, p_train_pig)
    save_test(test_pig, p_test_pig, p_label_pig)

