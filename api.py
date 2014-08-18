from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.feature_extraction.text import TfidfVectorizer as TV
from sklearn.cross_validation import LeaveOneOut as LOO
from sklearn.cross_validation import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier as DT
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import ExtraTreesClassifier as ETC
from sklearn.ensemble import AdaBoostClassifier as Ada
from sklearn.naive_bayes import GaussianNB as GNB
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix as CM
from sklearn import tree
from sklearn.preprocessing import normalize
import random
import numpy as np
import pylab as pl

mapping = {'Recreation': 1, 'Transportation': 2, 'Business': 3, 'Public-Safety': 4, 'Social-Services': 5, 'Environment': 6, 'Health': 7, 'City-Government': 8, 'Education': 9, 'Housing-Development': 10}
raw_lines = [i.strip().split(',') for i in open('ny_dump','r').readlines()]
lines = []
data_ = []
data = []
label = []
#sum_all = {}
sum_use = {}
for l in raw_lines:
    if len(l)>6:
        lines.append(l)
    else:
        pass

for l in lines:
    '''
    1-agency
    2-name
    3-description
    4-category
    5-url id
    6:-field names
    '''
    #sum_all[l[3]] = sum_all.get(l[3],0) + 1
    #data_.append(l[2]+' '+' '.join(l[5:]))
    data_.append(' '.join(l[5:]))
    data.append(l[2])
    label.append(mapping[l[3]])
    sum_use[l[3]] = sum_use.get(l[3],0) + 1
#print sum_use

'''
-break down all the datas into single word (?)
-vectorize the bag of words for each dataset
-train and testing
'''
label = np.array(label)
vc_ = CV(analyzer='char_wb', ngram_range=(3,5), min_df=1, token_pattern='[a-z]{2,}')
#vc = TV(analyzer='char_wb', ngram_range=(2,3), min_df=1, token_pattern='[a-z]{2,}')
vc = CV(token_pattern='[a-z]{2,}')
#vc = TV(token_pattern='[a-z]{2,}', binary=True)

vector_ = vc_.fit_transform(data_).toarray()
vector = vc.fit_transform(data).toarray()
#print len(vc.get_feature_names())
#print vc.get_feature_names()

idx = LOO(len(vector))
#fold = 10
#idx = StratifiedKFold(label, n_folds=fold)

#clf = DT(criterion='entropy', random_state=0)
#clf = RFC(n_estimators=50, criterion='entropy')
clf = GNB()
#clf = SVC(C=0.1,kernel='linear')
ctr = 0
#for train, test in idx:
while True:
    train = range(len(vector))
    test = random.randint(0,len(vector)-1)
    train.remove(test)
    train_data = vector[train]
    train_label = label[train]
    test_data = vector[test]
    test_label = label[test]
    clf.fit(train_data, train_label)
    pred = clf.predict(test_data)
    #preds.append(pred)
    if pred != test_label:
        continue
    #    ctr += 1
    #    print 'inst', i+1, '%d:%d'%(test_label,pred)

    i=0
    while i<len(lines):
        if i==test:
            lines[i].append(100)
            i+=1
            continue
        if label[i]!=pred:
            lines[i].append(100)
            '''
        #using distance btw two prob vector
        else:
            clf_ = RFC(n_estimators=50, criterion='entropy')
            #clf_ = GNB()
            idx_ = range(len(vector_))
            idx_.remove(test)
            idx_.remove(i)
            train_data_ = vector_[idx_]
            train_label_ = label[idx_]
            clf_.fit(train_data_, train_label_)
            pr_ex = clf_.predict_proba(vector_[test])
            pr_cur = clf_.predict_proba(vector_[i])
            d = np.linalg.norm((pr_ex-pr_cur), ord=2)
            lines[i].append(d)
            '''
        else:
            L_i = np.linalg.norm((vector_[i]), ord=2)
            L_test = np.linalg.norm((vector_[test]), ord=2)
            d = np.linalg.norm((vector_[i]/L_i - vector_[test]/L_test), ord=2)
            lines[i].append(d)
        i+=1
    break

#res = [i.rsplit(',',1) for i in lines]
source = lines[test]
print '>>>>>>>>>>SOURCE>>>>>>>>>>>>>>>>>>>>>>>>>>'
print 'Publishing Agency:', source[0]
print 'Name:', source[1]
print 'Description:', source[2]
print 'Category:', source[3]
print 'Columns:'
print ' | '.join(source[5:-1])
lines = sorted(lines, key=lambda x:x[-1])
res = lines[:5]
print '<<<<<<<<<<TARGET<<<<<<<<<<<<<<<<<<<<<<<<<<'
for i in res:
    print 'distance:', i[-1]
    print 'Publishing Agency:', i[0]
    print 'Name:', i[1]
    print 'Despriction:', i[2]
    print 'Category:', i[3]
    print 'Columns:'
    print ' | '.join(i[5:-1])
    print '------------------------------------------------'

'''
    acc = accuracy_score(test_label, preds)
    a_sum.append(acc)
    print acc
    if acc>tmp:
        tmp = acc
        l = test_label[:]
        p = preds[:]
print 'ave acc:', np.mean(a_sum)
print 'std:', np.std(a_sum)

cm = CM(l,p)
#print cm
cm = normalize(cm.astype(np.float), axis=1, norm='l1')
#print cm
#cm /= cm.astype(np.float).sum(axis=1)
fig = pl.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(cm)
fig.colorbar(cax)

for x in xrange(len(cm)):
    for y in xrange(len(cm)):
         ax.annotate(str("%.3f"%cm[x][y]), xy=(y,x),
                     horizontalalignment='center',
                     verticalalignment='center')


cls = ['recrtn','trans','busi','safety','servcs','environ','health','gov','edu','housing']
pl.xticks(range(len(cm)),cls)
pl.yticks(range(len(cm)),cls)
pl.title('Confusion matrix')
#pl.colorbar()
pl.ylabel('True label')
pl.xlabel('Predicted label')
pl.show()
'''
