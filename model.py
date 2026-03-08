import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression

# load dataset
data = pd.read_csv("dataset.csv")

X = data["text"]
y = data["role"]

# convert text to numbers
vectorizer = TfidfVectorizer()

X_vector = vectorizer.fit_transform(X)

# train model
model = LogisticRegression()

model.fit(X_vector, y)


def predict_role(resume_text):

    resume_vector = vectorizer.transform([resume_text])

    prediction = model.predict(resume_vector)

    return prediction[0]
