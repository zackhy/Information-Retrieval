"""
This program build the text classifier for detecting the fake reviews
Author: Haoyou Liu
"""

import csv
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

conn = sqlite3.connect('reviews.db')
cur = conn.cursor()

q = 'SELECT review_text, label FROM review JOIN labels on review.review_id=labels.review_id'
cur.execute(q)

rows = cur.fetchall()
reviews = []
target = []
for row in rows:
    reviews.append(row[0])
    target.append(row[1])

q = 'SELECT review, label FROM Test'
cur.execute(q)
rows = cur.fetchall()
test = []
test_target = []
for row in rows:
    test.append(row[0])
    test_target.append(row[1])

cv = CountVectorizer().fit(reviews)
vect = cv.transform(reviews)
# X_train, X_test, y_train, y_test = train_test_split(vect, target, test_size=0.33, random_state=42)
X_test = cv.transform(test)

clf = SGDClassifier(loss='hinge', penalty='l1', alpha=1e-5, n_iter=20)
clf.fit(vect, target)
result = clf.score(X_test, test_target)
print result