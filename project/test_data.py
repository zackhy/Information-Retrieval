"""
This program collects test data and stores them in database
Author: Haoyou Liu
"""

import sqlite3
import os

conn = sqlite3.connect('reviews.db')
cur = conn.cursor()

statement = 'DROP TABLE IF EXISTS Test'
cur.execute(statement)

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Test (review TEXT, label INTEGER)'
cur.execute(statement)

records = []
for filename in os.listdir('./test/fake'):
    for filename2 in os.listdir('./test/fake/' + filename):
        with open('test/fake/' + filename + '/' + filename2, 'rU') as f:
            for line in f:
                records.append((line, 0))

q = 'INSERT INTO Test VALUES (?, ?)'
cur.executemany(q, records)

records = []
for filename in os.listdir('./test/true'):
    for filename2 in os.listdir('./test/true/' + filename):
        for filename3 in os.listdir('./test/true/' + filename + '/' + filename2):
            with open('./test/true/' + filename + '/' + filename2 + '/' + filename3) as f:
                for line in f:
                    records.append((line, 1))

q = 'INSERT INTO Test VALUES (?, ?)'
cur.executemany(q, records)

conn.commit()
conn.close()
