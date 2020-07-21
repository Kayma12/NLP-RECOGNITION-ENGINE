import os
import pickle
import pandas as pd

# get ml stream classification df
# os.path.join(os.path.dirname(),

with open('Machine_learning_df', 'rb') as fh:  # you need to use 'rb' to read
    df_stream = pickle.load(fh)

df_stream.head(2)

df_stream.describe()

# may  need to vectorize each text
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.feature_extraction.text import CountVectorizer

X= df_stream.drop(['Stream'], axis=1)
y= df_stream['Stream'].values

df_stream['cv_text'].head()

X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.25, random_state=1000)

y

vectorizer = CountVectorizer()
vectorizer.fit(X_train)
X_train = vectorizer.transform(X_train)
X_test = vectorizer.transform(X_test)

# ### A simple logistoic Regression Model

encoder = LabelEncoder()
encoder.fit(y)
y = encoder.transform(y)


y = to_categorical(y)

y

df_stream.info()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Dense(8, input_dim=4, activation='relu'))
model.add(Dense(3, activation='softmax'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x=X_train, y=y_train, epochs=100, batch_size=5, validation_data=(X_test,y_test))



from sklearn.linear_model import LogisticRegression

X_test


y_test

# +
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer

nb = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', MultinomialNB()),
              ])
nb.fit(X_train, y_train)

# %%time
from sklearn.metrics import classification_report
y_pred = nb.predict(X_test)

print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred,target_names=my_tags))
# -






