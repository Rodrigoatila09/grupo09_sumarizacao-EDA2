def taxa_compressao(n_frases_resumo: int, n_frases_total: int) -> float:
    if n_frases_total == 0:
        return 0.0
    return n_frases_resumo / n_frases_total


def imprimir_scores_pagerank(scores_pagerank: dict, frases: list) -> None:
    frases_por_id = {frase["id_global"]: frase for frase in frases}
    ranking = sorted(scores_pagerank.items(), key=lambda par: par[1], reverse=True)

    print("--- Scores de PageRank (ordem decrescente) ---\n")
    for id_frase, score in ranking:
        frase = frases_por_id[id_frase]
        print(
            f"[{id_frase:02d}] score={score:.4f}  ({frase['id_artigo']})  "
            f"{frase['texto_original']}"
        )
    print()


def imprimir_arestas_mais_fortes(grafo, frases: list, top_n: int = 10) -> None:
    frases_por_id = {frase["id_global"]: frase for frase in frases}
    arestas = grafo.listar_arestas()
    arestas.sort(key=lambda aresta: aresta[2], reverse=True)

    print(f"--- Top {top_n} arestas de maior similaridade ---\n")
    for i, j, peso in arestas[:top_n]:
        frase_i = frases_por_id[i]
        frase_j = frases_por_id[j]
        print(f"peso={peso:.3f}")
        print(f"  [{frase_i['id_artigo']}] {frase_i['texto_original']}")
        print(f"  [{frase_j['id_artigo']}] {frase_j['texto_original']}")
        print()
