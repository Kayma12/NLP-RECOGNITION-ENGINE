import nltk
import string
import re
from cleaning_and_reading import read_in_files
from nltk.tokenize import sent_tokenize

stopword = nltk.corpus.stopwords.words('english')


# cv = "dummy_cvs/Susan Campbell CV1.docx"
# text = read_in_files.read_in_doc_docx_file(cv)


def clean_cv(text):
    text = text.lower()
    text = remove_punct(text)
    text = join_java_and_script(text)

    text_token = tokenize(text)
    sent_tok = senetnce_tokenize(text)
    text_no_stop = remove_stopwords(text_token)
    return text_no_stop


def clean_tokenize_text(text):
    pass


# remove punctuation
def remove_punct(text):
    punc_keep = ['-', '+', '#']  # (C)  c ')', '(',
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

def remove_alevel_gcse_section(cv):
    """
    Removes the section with gcse or alevel, and it checks in case it is on another line
    """
    education = [x.lower() for x in ["A Level", "alevel", "A-Level", "GCSE's", "GCSEs", "gcse"]]
    lines = [x.lower() for x in cv.splitlines()]
    cv_text = " "
    for i in range(len(lines)):
        if any(e in lines[i] for e in education):
            for num_line in range(i, i + 3):
                lines[num_line] = " "
        cv_text += lines[i] + " "

    return cv_text


def join_java_and_script(cv):
    find_java_followed_script = re.findall(r'{0}(?:\s{1}+)'.format('java', 'script'), cv)
    if len(find_java_followed_script) > 0:
        for match in find_java_followed_script:
            cv = cv.replace(match, str(match).replace(" ", ""))

    return cv


