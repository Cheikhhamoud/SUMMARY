import nltk
nltk.download('stopwords')
nltk.download('punkt')

import re
import heapq
import numpy as np
import pandas as pd
import sys


def read_text(file_data):
    """
    Read text from file

    INPUT:
    file_name - Text file containing original text.

    OUTPUT:
    text - str. Text with reference number, i.e. [1], [10] replaced with space, if any...
    clean_text - str. Lowercase characters with digits & one or more spaces replaced with single space.
    """

    text = file_data
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    clean_text = text.lower()

    # replace characters other than [a-zA-Z0-9], digits & one or more spaces with single space
    regex_patterns = [r'\W', r'\d', r'\s+']
    for regex in regex_patterns:
        clean_text = re.sub(regex, ' ', clean_text)

    return text, clean_text


def rank_sentence(text, clean_text, sent_word_length):
    """
    Rank each sentence and return sentence score

    INPUT:
    text - str. Text with reference numbers, i.e. [1], [10] removed, if any...
    clean_text - str. Clean lowercase characters with digits and additional spaces removed.
    sent_word_length - int. Maximum number of words in a sentence.

    OUTPUT:
    sentence_score - dict. Sentence score
    """
    sentences = nltk.sent_tokenize(text)
    stop_words = nltk.corpus.stopwords.words('english')

    word_count = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word_count.keys():
                word_count[word] = 1
            else:
                word_count[word] += 1

    sentence_score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_count.keys():
                if len(sentence.split(' ')) < int(sent_word_length):
                    if sentence not in sentence_score.keys():
                        sentence_score[sentence] = word_count[word]
                    else:
                        sentence_score[sentence] += word_count[word]

    return sentence_score


def generate_summary(file_data, sent_word_length, top_n):
    """
    Generate summary

    INPUT:
    file_name - Text file containing original text.
    sent_word_length - int. Maximum number of words in a sentence.
    top_n - int. Top n sentences to display.

    OUTPUT:
    summarized_text - str. Summarized text with each sentence on each line.
    """
    text, clean_text = read_text(file_data)

    sentence_score = rank_sentence(text, clean_text, sent_word_length)

    best_sentences = heapq.nlargest(int(top_n), sentence_score, key=sentence_score.get)

    summarized_text = []

    sentences = nltk.sent_tokenize(text)

    for sentence in sentences:
        if sentence in best_sentences:
            summarized_text.append(sentence)

    summarized_text = "\n".join(summarized_text)

    return summarized_text

if __name__ == '__main__':
    #test article: files/text_articles/test_algo.txt
    with open('/home/mohamedali/PycharmProjects/text_summarization/pdf_processing/pdf_processing_output/abstract of abstracts.txt', 'r') as f:
        file_data = f.read()
    summary = generate_summary(file_data, 30, 3)
    for i in summary:
        print(i,end="")
