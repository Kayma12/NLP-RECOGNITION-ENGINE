import os
import pickle
import pandas as pd

# Using Machine Learning to predict streams

# get ml stream classification df
# os.path.join(os.path.dirname(),

with open('Machine_learning_df', 'rb') as fh:  # you need to use 'rb' to read
    df_stream = pickle.load(fh)

df_stream.head(8)

df_stream.describe()

df_stream[df_stream['Stream']==NAN]


# may  need to vectorize each text
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.feature_extraction.text import CountVectorizer

# +
X= df_stream['cv_text'].values

y= df_stream['Stream'].values
# -

df_stream['cv_text'].head()

X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=101)

# ### A simple MultinomialNB Model

df_stream.info()

# +
## from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer

nb = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', MultinomialNB()),
              ])
nb.fit(X_train, y_train)

# #%%time
from sklearn.metrics import classification_report, accuracy_score
y_pred = nb.predict(X_test)

print('accuracy %s' % accuracy_score(y_pred, y_test))
# -

df_stream['Stream'].unique()

X_train.shape


# ### Defining a Baseline Model

vectorizer = CountVectorizer()
vectorizer.fit(X_train)
X_train = vectorizer.transform(X_train)
X_test = vectorizer.transform(X_test)
X_train

from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression()
classifier.fit(X_train, y_train) # fit the data to a logisticc regression
score = classifier.score(X_test,y_test)
print("Accuracy: ", score)

# ## Drop any empty streams

empty_stream = df_stream[df_stream['Stream'] == ""]

empty_stream.index

df_stream.drop(empty_stream.index, inplace=True)

# ### Keras Model 1 >> Real python

# +
X= df_stream['cv_text'].values

y= df_stream['Stream']
# -

# Change to binary
encoder = LabelEncoder()
encoder.fit(y)
y = encoder.transform(y)

y = to_categorical(y)

X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=101)

vectorizer = CountVectorizer()
vectorizer.fit(X_train)
X_train = vectorizer.transform(X_train)
X_test = vectorizer.transform(X_test)
X_train

# +
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

input_dim = X_train.shape[1]  # Number of features

model = Sequential()
model.add(layers.Dense(10, input_dim=input_dim, activation='relu'))
model.add(layers.Dense(8, activation='softmax'))
# -

model.compile(loss='categorical_crossentropy', 
              optimizer='adam', 
              metrics=['accuracy'])
model.summary()

history = model.fit(X_train, y_train,
                    epochs=100,
                    verbose=False,
                    validation_data=(X_test, y_test),
                    batch_size=10)

loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))

# +
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def plot_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    x = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, acc, 'b', label='Training acc')
    plt.plot(x, val_acc, 'r', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x, loss, 'b', label='Training loss')
    plt.plot(x, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()


# -

plot_history(history)

# ### LSTM embedded layer

from tensorflow.keras.layers import Dense, Flatten, LSTM, Dropout, Activation, Embedding, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

vocab_size = 5000 # make the top list of words (common words)
embedding_dim = 32
max_length = 200
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>' # OOV = Out of Vocabulary
training_portion = .7

# +
X= df_stream['cv_text']
y= df_stream['Stream']

X= X.tolist()
y= y.tolist()
# -

# Change to binary
encoder = LabelEncoder()
encoder.fit(y)
y = encoder.transform(y)
y = to_categorical(y)

# +
train_size = int(len(X) * training_portion)

train_X = X[0: train_size]
train_y = y[0: train_size]

validation_X = X[train_size:]
validation_y = y[train_size:]

# +
tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(train_X)
word_index = tokenizer.word_index

train_sequences = tokenizer.texts_to_sequences(train_X)
train_padded = pad_sequences(train_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

validation_sequences = (tokenizer.texts_to_sequences(validation_X))
validation_padded = (pad_sequences(validation_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type))


# +
# label_tokenizer = Tokenizer()
# label_tokenizer.fit_on_texts(y)

# training_label_seq = (label_tokenizer.texts_to_sequences(train_y))
# validation_label_seq =(label_tokenizer.texts_to_sequences(validation_y))

# +
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim))
model.add(Dropout(0.5))
model.add(Bidirectional(LSTM(embedding_dim)))
model.add(Dense(8, activation='softmax'))

model.summary()

# +

opt = Adam(lr=0.001, decay=1e-6)
model.compile(
    loss='categorical_crossentropy',
    optimizer=opt,
    metrics=['accuracy'],
)
# -

validation_y

# +
num_epochs = 50
model.fit(train_padded, train_y, epochs=num_epochs, validation_data=(validation_padded, validation_y), verbose=2)


# -

losses = pd.DataFrame(model.history.history)

plt.figure(figsize=(12,8))
plt.plot(model.history.history['accuracy'])
plt.plot(model.history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# "Loss"
plt.figure(figsize=(12,8))
plt.plot(model.history.history['loss'], 'g' )
plt.plot(model.history.history['val_loss'], 'y')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

df_stream.head(2)

# +
#PREDICTION
# Making incorrect prediciton

txt = [X[0]]
seq = tokenizer.texts_to_sequences(txt)
padded = pad_sequences(seq, maxlen=max_length)
pred = model.predict(padded)
labels = ['Tester', 'Business Analysis', 'Business Intelligence',
       'Development', 'PMO', 'Risk Regulation & Compliance',
       'Project Support Officer', 'Analyst']

print(pred)
print(np.argmax(pred))
print(labels[np.argmax(pred)-1])
# -

X[0]
df_stream['Stream'].unique()
