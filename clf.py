from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.feature_extraction.text import TfidfVectorizer as TV
from sklearn.cross_validation import LeaveOneOut as LOO
from sklearn.cross_validation import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier as DT
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import ExtraTreesClassifier as ETC
from sklearn.ensemble import AdaBoostClassifier as Ada
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix as CM
from sklearn import tree
from sklearn.preprocessing import normalize
import numpy as np
import pylab as pl

mapping = {'Recreation': 1, 'Transportation': 2, 'Business': 3, 'Public-Safety': 4, 'Social-Services': 5, 'Environment': 6, 'Health': 7, 'City-Government': 8, 'Education': 9, 'Housing-Development': 10}
lines = [i.strip().split(',') for i in open('ny_dump','r').readlines()]
field = []
label = []
for l in lines:
    if len(l)>6:
        field.append(' '.join(l[5:]))
        label.append(mapping[l[3]])

'''
-break down all the fields into single words (?)
-vectorize the bag of words for each dataset
-train and testing
'''

label = np.array(label)
#vc = CV(token_pattern='[a-z]{2,}', binary=True)
vc = TV(token_pattern='[a-z]{2,}',binary=True)
vector = vc.fit_transform(field).toarray()
idx = LOO(len(vector))
preds = []
ctr = 0
for train, test in idx:
    train_data = vector[train]
    train_label = label[train]
    test_data = vector[test]
    #test_label = label[test]
    clf = DT(criterion='entropy', random_state=0)
    #clf = RFC(n_estimators=5, criterion='entropy')
    clf.fit(train_data, train_label)
    pred = clf.predict(test_data)
    preds.append(pred)
    #if pred != test_label:
    #    ctr += 1
    #    print 'inst', i+1, '%d:%d'%(test_label,pred)

acc = accuracy_score(label, preds)
print 'acc', acc


cm = CM(label,preds)
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
