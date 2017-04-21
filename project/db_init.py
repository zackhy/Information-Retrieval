import sqlite3
import json

conn = sqlite3.connect('reviews.db')

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Review")
cur.execute("DROP TABLE IF EXISTS User")
cur.execute("DROP TABLE IF EXISTS Cosine")

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'User (user_id TEXT PRIMARY KEY, user_name TEXT)'

cur.execute(statement)

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Review (review_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
             'user_id TEXT,' \
             'product_id TEXT,' \
             'helpfulness TEXT,' \
             'review_text TEXT,' \
             'rating INTEGER,' \
             'created_at INTEGER,' \
             'FOREIGN KEY (user_id) REFERENCES User(user_id))'
cur.execute(statement)

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Cosine (review_id_1 INTEGER,' \
             'review_id_2 INTEGER,' \
             'cosine_similarity REAL,' \
             'FOREIGN KEY (review_id_1) REFERENCES Review(review_id),' \
             'FOREIGN KEY (review_id_2) REFERENCES Review(review_id))'
cur.execute(statement)

conn.commit()

with open('Beauty_5.json', 'r', encoding='utf-8') as f:
    user_dict = {}
    for line in f:
        review = json.loads(line)

        try:
            user_record = (review['reviewerID'], review['reviewerName'])
        except:
            user_record = (review['reviewerID'], 'NA')

        review_record = (None,
                         review['reviewerID'],
                         review['asin'],
                         json.dumps(review['helpful']),
                         review['reviewText'],
                         review['overall'],
                         review['unixReviewTime'])

        q = 'INSERT INTO User VALUES (?, ?)'
        try:
            cur.execute(q, user_record)
        except:
            pass

        q = 'INSERT INTO Review VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.execute(q, review_record)

conn.commit()

conn.close()