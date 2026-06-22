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


def imprimir_frases_do_resumo(
    ids_resumo: list, frases: list, tabela_origem: dict
) -> None:
    frases_por_id = {frase["id_global"]: frase for frase in frases}

    print("--- Frases selecionadas para o resumo ---\n")
    for posicao, id_frase in enumerate(ids_resumo, start=1):
        frase = frases_por_id[id_frase]
        origem = tabela_origem[id_frase]
        print(f"{posicao}. [{id_frase:02d}] ({origem}) {frase['texto_original']}")
    print()


def imprimir_relatorio_completo(
    scores_pagerank: dict,
    grafo,
    frases: list,
    ids_resumo: list,
    tabela_origem: dict,
    top_n_arestas: int = 10,
) -> None:
    imprimir_scores_pagerank(scores_pagerank, frases)
    imprimir_arestas_mais_fortes(grafo, frases, top_n=top_n_arestas)
    imprimir_frases_do_resumo(ids_resumo, frases, tabela_origem)

    compressao = taxa_compressao(len(ids_resumo), len(frases))
    print(
        f"Taxa de compressão: {compressao:.3f}  "
        f"({len(ids_resumo)}/{len(frases)} frases)"
    )


if __name__ == "__main__":
    import os

    from graph import Grafo, construir_matriz_similaridade
    from pagerank import calcular_pagerank
    from preprocess import carregar_frases_da_pasta
    from summarizer import construir_tabela_hash_origem, selecionar_resumo

    pasta_exemplo = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "jogo01",
    )
    frases = carregar_frases_da_pasta(pasta_exemplo)
    matriz_sim = construir_matriz_similaridade(frases)
    grafo = Grafo.construir_a_partir_da_similaridade(matriz_sim, limiar=0.05)
    scores, _ = calcular_pagerank(grafo)

    tabela_origem = construir_tabela_hash_origem(frases)
    ids_resumo = selecionar_resumo(
        scores, matriz_sim, n_frases_resumo=6, limiar_redundancia=0.5
    )

    imprimir_relatorio_completo(scores, grafo, frases, ids_resumo, tabela_origem)
