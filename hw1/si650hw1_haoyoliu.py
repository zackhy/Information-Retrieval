from __future__ import division
import nltk
from itertools import groupby
from math import log
import matplotlib.pyplot as plt
import re
from collections import Counter

def word_freq(file, stopwords):
    word_freq_dict = {}
    sw = 0
    cap_len = 0
    word_len = 0
    count = 0
    pos_freq = {}
    pos_dict = {}

    for line in file:
        words = nltk.word_tokenize(line)

        for word in words:
            count += 1

            match = re.findall(r'[A-Z]', word)
            cap_len += len(match)

            word_len += len(word)

            if word.lower() in stopwords:
                sw += 1
                continue

            if word in word_freq_dict:
                word_freq_dict[word] += 1
            else:
                word_freq_dict[word] = 1

    aver_word_len = word_len/count

    pos_list = nltk.pos_tag(word_freq_dict.keys())

    for item in pos_list:
        if item[1] in pos_freq:
            pos_freq[item[1]] += 1
        else:
            pos_freq[item[1]] = 1

        pos_dict[item] = word_freq_dict[item[0]]

    pos_dict = sorted(pos_dict.items(), key= lambda x: x[1], reverse= True)

    return word_freq_dict, sw, cap_len, aver_word_len, pos_freq, pos_dict

def xy_axis(dict):
    raw_list = sorted(dict.values())
    prop_list = [len(list(group)) for key, group in groupby(raw_list)]
    freq_list = sorted(set(raw_list))

    y_list = [log(i, 2) for i in prop_list]
    x_list = [log(j, 2) for j in freq_list]

    plt.scatter(x_list, y_list)
    plt.show()

if __name__ == '__main__':
    stopwords = []
    with open('stoplist.txt', 'r') as f:
        for stopword in f:
            stopwords.append(stopword.replace('\n', '').replace('\r', ''))

    with open('blog.txt', 'r') as f1:
        blog_dict, sw, cap, word_len, pos_freq, pos_dict = word_freq(f1, stopwords)
        # xy_axis(blog_dict)
        print 'vocabulary size for blog'
        print len(blog_dict)
        print '\n'

        print 'Frequency of stopwords for blog'
        print sw
        print '\n'

        print 'Number of capital letters for blog'
        print cap
        print '\n'

        print 'Average number of characters per word'
        print word_len
        print '\n'

        nouns = ['NN', 'NNS', 'NNP', 'NNPS']
        JJ = ['JJ', 'JJR', 'JJS']
        verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        adv = ['RB', 'RBR', 'RBS', 'WRB']
        pron = ['PRP', 'PRP$', 'WP', 'WP$']

        print 'number of nouns'
        num = 0
        for i in nouns:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        print 'number of adjectives'
        num = 0
        for i in JJ:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        print 'number of verbs'
        num = 0
        for i in verbs:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        print 'number of adverbs'
        num = 0
        for i in adv:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        print 'number of pronouns'
        num = 0
        for i in pron:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        count = 1
        for item in pos_dict:
            if count > 10:
                break
            if item[0][1] in nouns:
                print 'Nouns ' + str(count) + ' ' + str(item[0][0])
                count += 1

        count = 1
        for item in pos_dict:
            if count > 10:
                break
            if item[0][1] in verbs:
                print 'Verb ' + str(count) + ' ' + str(item[0][0])
                count +=1

        count = 1
        for item in pos_dict:
            if count > 10:
                break
            if item[0][1] in JJ:
                print 'adjectives ' + str(count) + ' ' + str(item[0][0])
                count += 1

    with open('congress_speech.txt', 'r') as f2:
        congress_dict, sw, cap, word_len, pos_freq, pos_dict = word_freq(f2, stopwords)
        # xy_axis(congress_dict)
        print 'vocabulary size for congress speech'
        print len(congress_dict)
        print '\n'

        print 'Frequency of stopwords for congress speech'
        print sw
        print '\n'

        print 'Number of capital letters for congress speech'
        print cap
        print '\n'

        print 'Average number of characters per word'
        print word_len
        print '\n'

        print 'number of nouns'
        num = 0
        for i in nouns:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        print 'number of adjectives'
        num = 0
        for i in JJ:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        print 'number of verbs'
        num = 0
        for i in verbs:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        print 'number of adverbs'
        num = 0
        for i in adv:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        print 'number of pronouns'
        num = 0
        for i in pron:
            if i in pos_freq.keys():
                num += pos_freq[i]
        print num

        count = 1
        for item in pos_dict:
            if count > 10:
                break
            if item[0][1] in nouns:
                print 'Nouns ' + str(count) + ' ' + str(item[0][0])
                count += 1

        count = 1
        for item in pos_dict:
            if count > 10:
                break
            if item[0][1] in verbs:
                print 'Verb ' + str(count) + ' ' + str(item[0][0])
                count +=1

        count = 1
        for item in pos_dict:
            if count > 10:
                break
            if item[0][1] in JJ:
                print 'adjectives ' + str(count) + ' ' + str(item[0][0])
                count += 1


    # TF-IDF
    words_list = blog_dict.keys()
    words_list.extend(congress_dict.keys())
    doc_freq = Counter(words_list)

    tf_idf_blog = {}
    N = 2
    for word in blog_dict.keys():
        match = re.match(r'\W', word)
        if match:
            continue
        tf = log(blog_dict[word] + 1)
        idf = 1 + log(N/doc_freq[word])
        tf_idf_blog[word] = tf*idf

    tf_idf_blog = sorted(tf_idf_blog.items(), key= lambda x: x[1], reverse= True)
    print tf_idf_blog[:10]

    tf_idf_congress = {}
    for word in congress_dict.keys():
        match = re.match(r'\W', word)
        if match:
            continue
        tf = log(congress_dict[word] + 1)
        idf = 1 + log(N/doc_freq[word])
        tf_idf_congress[word] = tf*idf

    tf_idf_congress = sorted(tf_idf_congress.items(), key=lambda x: x[1], reverse=True)
    print tf_idf_congress[:10]


