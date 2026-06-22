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


def carregar_frases_da_pasta(caminho_pasta: str) -> list:
    """
    Lê todos os arquivos .txt de `caminho_pasta` e devolve uma lista de dicts no formato:

        {
            "id_global": int,            # índice único da frase no corpus inteiro
            "texto_original": str,       # frase como apareceu no artigo
            "tokens_processados": list,  # tokens normalizados (p/ similaridade)
            "id_artigo": str,            # nome do arquivo de origem (ex: "ge.txt")
        }
    """
    frases_resultado = []
    id_global = 0

    nomes_arquivos = sorted(
        nome for nome in os.listdir(caminho_pasta) if nome.endswith(".txt")
    )

    for nome_arquivo in nomes_arquivos:
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
        with open(caminho_completo, "r", encoding="utf-8") as arquivo:
            texto_artigo = arquivo.read()

        for frase_original in _segmentar_em_frases(texto_artigo):
            tokens = _tokenizar_e_normalizar(frase_original)

            # Frases cujo conteúdo (após remover stopwords) não ajudam na similaridade e são descartadas.
            if not tokens:
                continue

            frases_resultado.append(
                {
                    "id_global": id_global,
                    "texto_original": frase_original,
                    "tokens_processados": tokens,
                    "id_artigo": nome_arquivo,
                }
            )
            id_global += 1

    return frases_resultado