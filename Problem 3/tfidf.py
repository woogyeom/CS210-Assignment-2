from collections import Counter, defaultdict
import re
import math

# Preprocessing
def read_stopwords():
    stopwords = []
    stopwords_file = open('stopwords.txt', 'r')
    lines = stopwords_file.readlines()
    stopwords_file.close
    for line in lines:
        stopwords.append(line.strip())
    return stopwords

def read_tfidf_file():
    input_files = []
    tfidf_file = open('tfidf_docs.txt', 'r')
    lines = tfidf_file.readlines()
    tfidf_file.close
    for line in lines:
        input_files.append(line.strip())
    return input_files

def lines_to_words(lines):
    words = []
    for line in lines:
        words.extend(line.split())
    return words

def clean_file(words):
    new_words = []
    for word in words:
        word = re.sub(r'https?://\S+', '', word)
        word = re.sub(r'[^\w\s]', '', word)
        if word:
            word = word.lower()
            new_words.append(word)
    return new_words

def remove_stopwords(words):
    new_words = []
    for word in words:
        if word not in stopwords:
            new_words.append(word)
    return new_words

def stemming_lemmatization(words):
    new_words = []
    for word in words:
        word = re.sub(r'ing$', '', word)
        word = re.sub(r'ly$', '', word)
        word = re.sub(r'ment$', '', word)
        new_words.append(word)
    return new_words

def print_preproc_file(filename, words):
    file = open(f'preproc_{filename}', 'w')
    file.write(" ".join(words))
    file.close
    
stopwords = read_stopwords()
input_files = read_tfidf_file()
for filename in input_files:
    file = open(filename)
    lines = file.read().splitlines()
    file.close
    words = lines_to_words(lines)
    words = clean_file(words)
    words = remove_stopwords(words)
    words = stemming_lemmatization(words)
    print_preproc_file(filename, words)

# Computing TF-IDF Scores
preproc_files = [f'preproc_{file}' for file in input_files]

def find_word(target):
    found = 0
    for file in preproc_files:
        file = open(file)
        line = file.readline()
        file.close
        words = line.split()
        for word in words:
            if word == target:
                found += 1
                break
    return found

def print_tfidf_file(filename, top_five):
    filename = filename.replace('preproc', 'tfidf')
    file = open(filename, 'w')
    file.write(str(top_five))
    file.close

for filename in preproc_files:
    tf_idf_dict = defaultdict(list)
    file = open(filename)
    lines = file.read().splitlines()
    file.close
    words = lines_to_words(lines)    
    words_counter = Counter(words)
    distinct_words = list(set(words_counter.elements()))
    total_count = sum(count for count in words_counter.values())
    for word in distinct_words:
        if word not in tf_idf_dict.items():
            tf = words_counter[word] / total_count
            num_word_found = find_word(word)
            idf = (math.log(len(input_files) / num_word_found)) + 1
            tf_idf_dict[word] = round((tf * idf), 2)
    top_five = sorted(tf_idf_dict.items(), key=lambda x: (-x[1], x[0]))[:5]
    print_tfidf_file(filename, top_five)