# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:05:45 2015

@author: aleksej
"""
import os
import codecs
import sqlite3
import os
from sklearn.externals import joblib
import sklearn
otvet = []
text = []
for papka in os.listdir('/Users/aleksej/Desktop/python/lenta/database2')[1:]:
    for name in os.listdir('/Users/aleksej/Desktop/python/lenta/database2/%s'%papka):
        otvet.append(papka)
        text.append(codecs.open('/Users/aleksej/Desktop/python/lenta/database2/%s/%s'%(papka,name),'r').read().decode('koi8_r'))
a = open('text.txt','w')
a.write(text)

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_counts = count_vect.fit_transform(text) 


from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_tfidf = tfidf_transformer.fit_transform(X_counts)





from sklearn.ensemble import AdaBoostClassifier
clf1 = AdaBoostClassifier(n_estimators=100)
scores1 = cross_val_score(clf1, X_tfidf,otvet)
print scores1.mean()
#34%

from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
clf2 = BaggingClassifier(KNeighborsClassifier(),max_samples=0.5, max_features=0.5)
scores2 = cross_val_score(clf2, X_tfidf,otvet)
print scores2.mean()
#30%

from sklearn.ensemble import ExtraTreesClassifier
clf3 = ExtraTreesClassifier(n_estimators=10, max_depth=None,min_samples_split=1, random_state=0)
scores3 = cross_val_score(clf3, X_tfidf,otvet)
print scores3.mean()
#43%

from sklearn.multiclass import OneVsRestClassifier
clf4 = OneVsRestClassifier(clf3)
scores4 = cross_val_score(clf4, X_tfidf,otvet)
print scores4.mean()
#46%

from sklearn.naive_bayes import GaussianNB
clf5 = GaussianNB()
scores5 = cross_val_score(clf5, X_tfidf.toarray(),otvet)
print scores5.mean()
#33%

from sklearn.naive_bayes import MultinomialNB
clf6 = MultinomialNB()
scores6 = cross_val_score(clf6, X_tfidf.toarray(),otvet)
print scores6.mean()
#27%

clf7 = BaggingClassifier(ExtraTreesClassifier(n_estimators=10, max_depth=None,min_samples_split=1, random_state=0),max_samples=0.5, max_features=0.5)
scores7 = cross_val_score(clf7, X_tfidf.toarray(),otvet)
print scores7.mean()
#44%

clf8 = OneVsRestClassifier(clf7)
scores8 = cross_val_score(clf8, X_tfidf.toarray(),otvet)
print scores8.mean()
#47%
clf8 = clf8.fit(X_tfidf,otvet)
joblib.dump(clf8, 'classifier.pkl') 


