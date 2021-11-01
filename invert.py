import helper_func as diegotom
import nltk
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


porter = PorterStemmer()
STOP_WORDS = stopwords.words('english')


with open("cacm.all_one", "r") as f:
    text = f.read()
    text_split = text.split(".I ")
    sub = text_split[1:]
    print(sub)

diegotom.pre_processing(text_split)
# def pre_processing(document):
