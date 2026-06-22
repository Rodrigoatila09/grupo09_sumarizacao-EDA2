def gerar_newsletter_markdown(
    ids_resumo: list,
    frases: list,
    tabela_origem: dict,
    titulo: str = "Resumo da Partida",
) -> str:
    linhas = [f"# {titulo}", ""]
    frases_por_id = {frase["id_global"]: frase for frase in frases}

    for posicao, id_frase in enumerate(ids_resumo, start=1):
        texto_original = frases_por_id[id_frase]["texto_original"]
        portal_origem = tabela_origem[id_frase]

        linhas.append(f"{posicao}. {texto_original}")
        linhas.append(f"   — fonte: {portal_origem}")
        linhas.append("")

    return "\n".join(linhas)


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

    markdown = gerar_newsletter_markdown(
        ids_resumo, frases, tabela_origem, titulo="Brasil 2 x 1 Argentina"
    )
    print(markdown)
