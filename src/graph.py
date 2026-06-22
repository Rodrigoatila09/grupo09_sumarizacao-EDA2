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

class Grafo:

    def __init__(self, n_vertices: int):
        self.n_vertices = n_vertices
        self.matriz_adjacencia = [[0.0] * n_vertices for _ in range(n_vertices)]

    def adicionar_aresta(self, i: int, j: int, peso: float) -> None:
        if i == j:
            return
        self.matriz_adjacencia[i][j] = peso
        self.matriz_adjacencia[j][i] = peso

    def peso_aresta(self, i: int, j: int) -> float:
        return self.matriz_adjacencia[i][j]

    def vizinhos(self, i: int) -> list:
        return [
            j
            for j in range(self.n_vertices)
            if j != i and self.matriz_adjacencia[i][j] > 0
        ]

    def grau_ponderado(self, i: int) -> float:
        return sum(self.matriz_adjacencia[i])

    def listar_arestas(self) -> list:
        arestas = []
        for i in range(self.n_vertices):
            for j in range(i + 1, self.n_vertices):
                peso = self.matriz_adjacencia[i][j]
                if peso > 0:
                    arestas.append((i, j, peso))
        return arestas

    @classmethod
    def construir_a_partir_da_similaridade(
        cls, matriz_similaridade: list, limiar: float = 0.0
    ) -> "Grafo":
        n = len(matriz_similaridade)
        grafo = cls(n)

        for i in range(n):
            for j in range(i + 1, n):
                peso = matriz_similaridade[i][j]
                if peso >= limiar and peso > 0:
                    grafo.adicionar_aresta(i, j, peso)

        return grafo


if __name__ == "__main__":
    import os
    from preprocess import carregar_frases_da_pasta

    pasta_exemplo = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "jogo01",
    )
    frases = carregar_frases_da_pasta(pasta_exemplo)
    matriz_sim = construir_matriz_similaridade(frases)

    print(f"Matriz de similaridade: {len(matriz_sim)}x{len(matriz_sim)}\n")


    pares = []
    for i in range(len(frases)):
        for j in range(i + 1, len(frases)):
            if frases[i]["id_artigo"] != frases[j]["id_artigo"]:
                pares.append((matriz_sim[i][j], i, j))
    pares.sort(reverse=True)

    print("Top 5 pares de frases mais similares (entre portais diferentes):\n")
    for sim, i, j in pares[:5]:
        print(f"sim={sim:.3f}")
        print(f"  [{frases[i]['id_artigo']}] {frases[i]['texto_original']}")
        print(f"  [{frases[j]['id_artigo']}] {frases[j]['texto_original']}")
        print()

    grafo = Grafo.construir_a_partir_da_similaridade(matriz_sim, limiar=0.05)

    print(f"Vértices (frases): {grafo.n_vertices}")
    print(f"Arestas (após limiar): {len(grafo.listar_arestas())}\n")

    print("Grau ponderado das 5 primeiras frases:")
    for i in range(5):
        print(
            f"  [{i:02d}] grau={grafo.grau_ponderado(i):.3f}  "
            f"vizinhos={grafo.vizinhos(i)}"
        )
