from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

from typing import Set


def load_words_from_file(file_name: str) -> Set[str]:
    with open(file_name) as f:
        return set(item.strip() for item in f.readlines())


stop_words = set()
stop_words |= set(stopwords.words('english'))
stop_words |= load_words_from_file('del_words.txt')
stop_words |= load_words_from_file('propositions.txt')

lemmatizer = WordNetLemmatizer()


def filter_words(words: Set[str]) -> Set[str]:
    return words - stop_words


def lemmatize(words: Set[str]) -> Set[str]:
    return set(lemmatizer.lemmatize(word) for word in words)


def nltk_preprocess(sentence: str) -> Set[str]:
    sentence = sentence.lower()
    words = set()
    for word, tag in pos_tag(word_tokenize(sentence)):
        wntag = tag[0].lower()
        wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
        if not wntag:
            lemma = word
        else:
            lemma = lemmatizer.lemmatize(word, wntag)
        if len(lemma) > 2:
            words.add(lemma)
    words = filter_words(words)
    return words
