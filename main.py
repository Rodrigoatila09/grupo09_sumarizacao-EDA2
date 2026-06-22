import os
import sys

from src.preprocess import carregar_frases_da_pasta
from src.graph import construir_matriz_similaridade, Grafo
from src.pagerank import calcular_pagerank
from src.summarizer import construir_tabela_hash_origem, selecionar_resumo
from src.newsletter import gerar_newsletter_markdown
from src.analysis import imprimir_relatorio_completo


LIMIAR_ARESTA_GRAFO = 0.05
LIMIAR_REDUNDANCIA_RESUMO = 0.5
N_FRASES_RESUMO_DEFAULT = 6


def executar_pipeline(nome_jogo: str, n_frases_resumo: int) -> None:
    pasta_jogo = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data", nome_jogo
    )

    if not os.path.isdir(pasta_jogo):
        print(f"[ERRO] Pasta não encontrada: {pasta_jogo}")
        sys.exit(1)

    frases = carregar_frases_da_pasta(pasta_jogo)
    if not frases:
        print(f"[ERRO] Nenhuma frase válida encontrada em {pasta_jogo}")
        sys.exit(1)

    matriz_similaridade = construir_matriz_similaridade(frases)

    grafo = Grafo.construir_a_partir_da_similaridade(
        matriz_similaridade, limiar=LIMIAR_ARESTA_GRAFO
    )

    scores_pagerank, _historico_convergencia = calcular_pagerank(grafo)

    tabela_hash_origem = construir_tabela_hash_origem(frases)
    ids_resumo = selecionar_resumo(
        scores_pagerank,
        matriz_similaridade,
        n_frases_resumo=n_frases_resumo,
        limiar_redundancia=LIMIAR_REDUNDANCIA_RESUMO,
    )

    titulo = f"Resumo — {nome_jogo}"
    texto_newsletter = gerar_newsletter_markdown(
        ids_resumo, frases, tabela_hash_origem, titulo=titulo
    )

    print(texto_newsletter)

    imprimir_relatorio_completo(
        scores_pagerank, grafo, frases, ids_resumo, tabela_hash_origem
    )


if __name__ == "__main__":
    nome_jogo_arg = sys.argv[1] if len(sys.argv) > 1 else "jogo01"
    n_frases_arg = int(sys.argv[2]) if len(sys.argv) > 2 else N_FRASES_RESUMO_DEFAULT

    executar_pipeline(nome_jogo_arg, n_frases_arg)