import nltk
import string
import re
import read_in_files
from nltk.tokenize import sent_tokenize

stopword = nltk.corpus.stopwords.words('english')

cv = "dummy_cvs/Susan Campbell CV1.docx"
text = read_in_files.read_in_doc_docx_file(cv)


def clean_cv(text):
    text = text.lower()
    text = remove_punct(text)
    text_token = tokenize(text)
    # sent_tok = senetnce_tokenize(text)
    text_no_stop = remove_stopwords(text_token)
    return text_no_stop


# remove punctuation
def remove_punct(text):
    punc_keep = [')', '(', '-', '+']  # (C)  c
    new_punc = []
    for punc in string.punctuation:
        if punc in punc_keep:
            continue
        else:
            new_punc.append(punc)

    text_nopunct = "".join([char for char in text if char not in new_punc])
    return text_nopunct


# print(string.punctuation) #!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~


# print(remove_punct(text))


# tokenize text
def tokenize(text):
    tokens = re.split("\s+", text)  # "(['()\w]+|\.)"  \W+
    return tokens


# print(tokenize(remove_punct(text)))

def senetnce_tokenize(text):
    sent_tokens = sent_tokenize(text)
    return sent_tokens


# print(senetnce_tokenize(text))


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
