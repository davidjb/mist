import os
from nltk.tokenize import RegexpTokenizer

here = os.path.abspath(os.path.dirname(__file__))


WORD_TOKENIZER = RegexpTokenizer(r'\w+')
STOP_WORDS = open(os.path.join(here, 'stopwords.txt')).read().split()
PROFANITY = open(os.path.join(here, 'profanity.txt')).read().split()

