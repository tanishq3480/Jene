from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

vectorizer = CountVectorizer(analyzer='char', ngram_range=(3,3))
model = MultinomialNB()

def train_classifier(sequences, labels):
    X = vectorizer.fit_transform(sequences)
    model.fit(X, labels)

def predict(sequence):
    X = vectorizer.transform([sequence])
    return model.predict(X)[0]