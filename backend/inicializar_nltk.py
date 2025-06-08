import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
import unicodedata

def baixar_recursos():
    try:
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("rslp")
        print("Recursos NLTK baixados com sucesso.")
    except Exception as e:
        print(f"Erro ao baixar recursos NLTK: {e}")

def limpar(texto):
    texto = unicodedata.normalize("NFKC", texto).lower()
    texto = texto.replace("\u200b", "").replace("\xa0", " ").strip()
    return texto

stopwords_pt = set(stopwords.words("portuguese"))
stopwords_pt.update(['oi', 'olá', 'ola', 'bom', 'dia', 'tarde', 'noite', 'tudo', 'bem', 'como', 'vai', 'você', 'estou', 'obrigado', 'obrigada', 'valeu', 'agradecido', 'agradecida'])

stemmer = RSLPStemmer()

def extrair_assuntos(frase):
    if not frase:
        return []

    frase = limpar(frase)
    tokens = word_tokenize(frase, language="portuguese")

    tokens_filtrados = [t for t in tokens if t.isalpha() and t not in stopwords_pt]

    radicais = list(set(stemmer.stem(t) for t in tokens_filtrados))

    return radicais

if __name__ == "__main__":
    baixar_recursos()