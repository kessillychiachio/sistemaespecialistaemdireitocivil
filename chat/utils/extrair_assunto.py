import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("rslp")

def extrair_assuntos(frase):
    if not frase:
        return []

    frase = frase.lower()
    tokens = word_tokenize(frase, language="portuguese")

    stopwords_pt = set(stopwords.words("portuguese"))
    tokens_filtrados = [t for t in tokens if t.isalpha() and t not in stopwords_pt]

    stemmer = RSLPStemmer()
    radicais = list(set(stemmer.stem(t) for t in tokens_filtrados))

    return radicais
