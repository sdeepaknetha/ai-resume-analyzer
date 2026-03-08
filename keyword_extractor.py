from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text):

    vectorizer = TfidfVectorizer(stop_words="english", max_features=10)

    X = vectorizer.fit_transform([text])

    keywords = vectorizer.get_feature_names_out()

    return keywords
