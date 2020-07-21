import os
import pickle
import pandas as pd

# get ml stream classification df
# os.path.join(os.path.dirname(),

with open('Machine_learning_df', 'rb') as fh:  # you need to use 'rb' to read
    df_stream = pickle.load(fh)

df_stream.head(2)

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

X_train

y_train

# Change to binary
encoder = LabelEncoder()
encoder.fit(y)
y = encoder.transform(y)

y = to_categorical(y)

X_train.shape

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

X_train.shape

y_train.shape

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


