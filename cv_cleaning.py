import nltk
import string
import re

stopword = nltk.corpus.stopwords.words('english')


def clean_cv(text):
    text = remove_punct(text)
    text_token = tokenize(text)
    text_no_stop = remove_stopwords(text_token)
    return text_no_stop


# remove punctuation
def remove_punct(text):
    text_nopunct = "".join([char for char in text if char not in string.punctuation])
    return text_nopunct


# tokenize text
def tokenize(text):
    tokens = re.split('\W+', text)
    return tokens


# remove stopwords
def remove_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in stopword]
    return text

# stemming

# ps = nltk.PorterStemmer()

# def stemming(tokenized_text):
#    text = [ps.stem(word) for word in tokenized_text]
#    return text

# text_stemmed = stemming(text_nonstop)

