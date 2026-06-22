D_AMORTECIMENTO = 0.85
MAX_ITERACOES = 100
TOLERANCIA_CONVERGENCIA = 1e-4

def calcular_pagerank(grafo, d: float = D_AMORTECIMENTO,
                       max_iter: int = MAX_ITERACOES,
                       tolerancia: float = TOLERANCIA_CONVERGENCIA):
    
    n = grafo.n_vertices

    scores = {i: 1.0 for i in range(n)}

    grau_ponderado = {j: grafo.grau_ponderado(j) for j in range(n)}

    historico_convergencia = []

    for iteracao in range(max_iter):
        novos_scores = {}
        maior_delta = 0.0

        for i in range(n):
            soma_contribuicoes = 0.0

            for j in grafo.vizinhos(i):
                w_ij = grafo.peso_aresta(i, j)
                grau_j = grau_ponderado[j]
                if grau_j == 0:
                    continue
                soma_contribuicoes += (w_ij / grau_j) * scores[j]

            novo_score = (1 - d) + d * soma_contribuicoes
            novos_scores[i] = novo_score

            delta = abs(novo_score - scores[i])
            if delta > maior_delta:
                maior_delta = delta

        scores = novos_scores
        historico_convergencia.append(maior_delta)

        if maior_delta < tolerancia:
            break

    return scores, historico_convergencia


if __name__ == "__main__":
    import os
    from preprocess import carregar_frases_da_pasta
    from graph import construir_matriz_similaridade, Grafo

    pasta_exemplo = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "jogo01",
    )
    frases = carregar_frases_da_pasta(pasta_exemplo)
    matriz_sim = construir_matriz_similaridade(frases)
    grafo = Grafo.construir_a_partir_da_similaridade(matriz_sim, limiar=0.05)

    scores, historico = calcular_pagerank(grafo)

    print(f"Convergiu em {len(historico)} iterações.")
    print(f"Último delta: {historico[-1]:.6f}\n")

    ranking = sorted(scores.items(), key=lambda par: par[1], reverse=True)

    print("Top 5 frases por score de PageRank:\n")
    for id_frase, score in ranking[:5]:
        frase = frases[id_frase]
        print(f"score={score:.4f}  [{frase['id_artigo']}] {frase['texto_original']}")
