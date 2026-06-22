import math

def _contar_tokens_comuns(tokens_i: list, tokens_j: list) -> int:
    set_i = set(tokens_i)
    set_j = set(tokens_j)
    return len(set_i & set_j)


def similaridade_textrank(tokens_i: list, tokens_j: list) -> float:
    len_i = len(tokens_i)
    len_j = len(tokens_j)

    if len_i <= 1 or len_j <= 1:
        return 0.0

    tokens_comuns = _contar_tokens_comuns(tokens_i, tokens_j)
    if tokens_comuns == 0:
        return 0.0

    denominador = math.log(len_i) + math.log(len_j)
    if denominador == 0:
        return 0.0

    return tokens_comuns / denominador


def construir_matriz_similaridade(frases: list) -> list:
    n = len(frases)
    matriz = [[0.0] * n for _ in range(n)]

    for i in range(n):
        tokens_i = frases[i]["tokens_processados"]
        for j in range(i + 1, n):
            tokens_j = frases[j]["tokens_processados"]
            sim = similaridade_textrank(tokens_i, tokens_j)
            matriz[i][j] = sim
            matriz[j][i] = sim

    return matriz

