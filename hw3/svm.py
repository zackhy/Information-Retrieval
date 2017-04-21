import csv
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

with open('train.tsv', 'rb') as trainf, open('test.tsv', 'rb') as testf:
    traintsv = csv.reader(trainf, delimiter='\t')
    testtsv = csv.reader(testf, delimiter='\t')
    next(traintsv)
    next(testtsv)
    result = {}

    train_data = []
    target = []
    for line in traintsv:
        target.append(int(line[0]))
        train_data.append(line[1].decode('utf-8'))

    test_data = []
    test_id = []
    for line in testtsv:
        test_data.append(line[1])
        test_id.append(line[0])

basic_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 1))),
                      ('tfidf', TfidfTransformer(norm='l2', use_idf=False)),
                      ('clf', SGDClassifier(loss='hinge', penalty='l1', alpha=1e-5, n_iter=20))])

parameters = {
    # 'vect__max_df': (0.5, 0.75, 1.0),
    # 'vect__max_features': (None, 5000, 10000, 50000),
    'vect__ngram_range': ((1, 1), (1, 2), (1, 3)),
    # 'tfidf__use_idf': (True, False),
    'tfidf__sublinear_tf': (True, False),
    # 'tfidf__norm': ('l1', 'l2'),
    # 'clf__alpha': (0.0001, 0.0005, 0.0007, 0.00001, 0.00003, 0.00005, 0.00007, 0.000001),
    # 'clf__penalty': ('l1', 'l2'),
    'clf__n_iter': (20, 40, 14),
}

text_clf = basic_clf.fit(train_data, target)
result_2 = text_clf.predict(test_data)
filename = 'result/svm_9.csv'
f = open(filename, 'wb')
writer = csv.writer(f)
writer.writerow(['Id', 'Category'])
for id, label in zip(test_id, result_2):
    writer.writerow([id, label])


# if __name__ == "__main__":
#     grid_search = GridSearchCV(basic_clf, parameters, n_jobs=-1, verbose=1)
#     grid_search.fit(train_data, target)
#     best_parameters = grid_search.best_estimator_.get_params()
#     for param_name in sorted(parameters.keys()):
#         print("\t%s: %r" % (param_name, best_parameters[param_name]))
#
#     print basic_clf.get_params

"""
clf__alpha: 1e-05
clf__n_iter: 20
clf__penalty: 'l1'
tfidf__norm: 'l2'
tfidf__use_idf: False
vect__ngram_range: (1, 1)
"""

"""
clf__alpha: 1e-05
clf__n_iter: 40
clf__penalty: 'l1'
tfidf__norm: 'l2'
tfidf__use_idf: False
vect__ngram_range: (1, 1)
"""

"""
clf__alpha: 1e-05
clf__n_iter: 40
tfidf__norm: 'l2'
tfidf__sublinear_tf: True
tfidf__use_idf: False
"""
