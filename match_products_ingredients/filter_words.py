from nltk.corpus import stopwords


def load_words_from_file(fileName):
    with open(fileName) as f:
        return set(item.strip() for item in f.readlines())


stop_words = set()
stop_words |= set(stopwords.words('english'))
stop_words |= load_words_from_file('del_words.txt')
stop_words |= load_words_from_file('propositions.txt')


def filter_words(words):
    return words - stop_words
