from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.feature_extraction.text import TfidfVectorizer as TV
from sklearn.cross_validation import LeaveOneOut as LOO
from sklearn.cross_validation import StratifiedKFold
import numpy as np
import random
import pprint

mapping = {'Recreation': 1, 'Transportation': 2, 'Business': 3, 'Public-Safety': 4, 'Social-Services': 5, 'Environment': 6, 'Health': 7, 'City-Government': 8, 'Education': 9, 'Housing-Development': 10}
lines = [i.strip().split(',') for i in open('ny_dump','r').readlines()]
random.shuffle(lines)
print '==================================='
print 'Category mapping:', mapping
print '==================================='

field = []
label = []
cate = []
sum_all = {}
sum_use = {}
ctr = 0
for l in lines:
    #sum_all[l[3]] = sum_all.get(l[3],0) + 1
    if ctr==10:
        break;
    if len(l)>6:
        field.append(' '.join(l[5:]))
        label.append(mapping[l[3]])
        cate.append(l[3])
        ctr += 1
        #sum_use[l[3]] = sum_use.get(l[3],0) + 1
#print sum_all
#print sum_use

print 'we have schema in the DB:'
print '(Class Number : Field Names)'
for c,f in zip(cate,field):
    print c,':',' | '.join(f.split())
print '==================================='

ddl = raw_input('give me your field names sepearted by white place: ')
print '==================================='

label = np.array(label)
vc = CV(token_pattern='[a-z]{2,}', binary=True)
#vc = TV(token_pattern='[a-z]{2,}', binary=True)
field.append(ddl)
vector = vc.fit_transform(field).toarray()

idx = 0
tag = label[0]
tmp = vector[-1]
#dist = np.linalg.norm(tmp-vector[0])/sum(vector[0])
dist = sum(abs(tmp-vector[0]))/sum(vector[0])
i = 1
for i in xrange(len(vector)-1):
    #d = np.linalg.norm(tmp-vector[i])/sum(vector[i])
    d = sum(abs(tmp-vector[i]))/sum(vector[i])
    if d<dist:
        dist = d
        idx = i
        tag = label[i]

print 'matched with category', tag, 'w/ headers:', field[idx]
#print vector
#print len(vc.get_feature_names())
#print vc.get_feature_names()

print '==================================='
#target = vector[idx]
#tags = np.array(vc.get_feature_names())
#add = tags[(target-tmp)==1]
#rmv = tags[(tmp-target)==1]
target = field[idx].split()
tmp = ddl.split()
rmv = []
add = []
for t in tmp:
    if t not in target:
        rmv.append(t)
for t in target:
    if t not in tmp:
        add.append(t)
print 'need to remove:', ' | '.join(rmv)
print 'need to add:', ' | '.join(add)






