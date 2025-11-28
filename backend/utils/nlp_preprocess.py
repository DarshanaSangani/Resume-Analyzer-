import re
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download once
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def clean_resume_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    lemmatized = [token.lemma_ for token in nlp(' '.join(tokens))]
    return ' '.join(lemmatized)
