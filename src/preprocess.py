import os
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import sent_tokenize

_STOPWORDS_PT = set(stopwords.words("portuguese"))
_STEMMER = RSLPStemmer()

def _tokenizar_e_normalizar(frase: str) -> list:
    """
    Converte uma frase em uma lista de tokens "processados":
    minúsculos, sem pontuação, sem stopwords e já com stemming aplicado.
    """
    frase_lower = frase.lower()
    tabela_pontuacao = str.maketrans(string.punctuation, " " * len(string.punctuation))
    frase_sem_pontuacao = frase_lower.translate(tabela_pontuacao)
    palavras = frase_sem_pontuacao.split()
    tokens_processados = []
    for palavra in palavras:
        if palavra in _STOPWORDS_PT:
            continue
        if len(palavra) < 2:
            continue
        tokens_processados.append(_STEMMER.stem(palavra))
    return tokens_processados


def _segmentar_em_frases(texto: str) -> list:
    """
    Quebra um texto em frases usando o tokenizador de sentenças do NLTK
    (treinado para o português via o pacote 'punkt').
    """
    texto_limpo = re.sub(r"\s+", " ", texto).strip()
    if not texto_limpo:
        return []
    frases = sent_tokenize(texto_limpo, language="portuguese")
    # Descarta frases muito curtas
    return [f.strip() for f in frases if len(f.strip()) > 0]