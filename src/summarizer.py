
class MaxHeap:

    def __init__(self):
        self._dados = []  

    def __len__(self) -> int:
        return len(self._dados)

    def esta_vazio(self) -> bool:
        return len(self._dados) == 0

    def _indice_pai(self, i: int) -> int:
        return (i - 1) // 2

    def _indice_filho_esquerdo(self, i: int) -> int:
        return 2 * i + 1

    def _indice_filho_direito(self, i: int) -> int:
        return 2 * i + 2

    def _trocar(self, i: int, j: int) -> None:
        self._dados[i], self._dados[j] = self._dados[j], self._dados[i]

    def _sift_up(self, i: int) -> None:
    
        while i > 0:
            pai = self._indice_pai(i)
            if self._dados[i][0] > self._dados[pai][0]:
                self._trocar(i, pai)
                i = pai
            else:
                break

    def _sift_down(self, i: int) -> None:
      
        n = len(self._dados)
        while True:
            esquerda = self._indice_filho_esquerdo(i)
            direita = self._indice_filho_direito(i)
            maior = i

            if esquerda < n and self._dados[esquerda][0] > self._dados[maior][0]:
                maior = esquerda
            if direita < n and self._dados[direita][0] > self._dados[maior][0]:
                maior = direita

            if maior == i:
                break

            self._trocar(i, maior)
            i = maior

    def inserir(self, prioridade: float, valor) -> None:
     
        self._dados.append((prioridade, valor))
        self._sift_up(len(self._dados) - 1)

    def extrair_maximo(self):
      
        if self.esta_vazio():
            raise IndexError("extrair_maximo() chamado em heap vazio")

        maximo = self._dados[0]
        ultimo = self._dados.pop()

        if self._dados:
            self._dados[0] = ultimo
            self._sift_down(0)

        return maximo

def construir_tabela_hash_origem(frases: list) -> dict:
  
    return {frase["id_global"]: frase["id_artigo"] for frase in frases}


def selecionar_resumo(
    scores_pagerank: dict,
    matriz_similaridade: list,
    n_frases_resumo: int,
    limiar_redundancia: float = 0.5,
) -> list:

    heap_candidatas = MaxHeap()
    for id_frase, score in scores_pagerank.items():
        heap_candidatas.inserir(score, id_frase)

    ids_selecionados = []

    while not heap_candidatas.esta_vazio() and len(ids_selecionados) < n_frases_resumo:
        _score, id_candidata = heap_candidatas.extrair_maximo()

        eh_redundante = any(
            matriz_similaridade[id_candidata][id_escolhida] >= limiar_redundancia
            for id_escolhida in ids_selecionados
        )

        if not eh_redundante:
            ids_selecionados.append(id_candidata)
      
    return ids_selecionados


if __name__ == "__main__":
  
    import os
    from preprocess import carregar_frases_da_pasta
    from graph import construir_matriz_similaridade, Grafo
    from pagerank import calcular_pagerank

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

    print(f"Frases selecionadas para o resumo ({len(ids_resumo)}):\n")
    for id_frase in ids_resumo:
        frase = frases[id_frase]
        origem = tabela_origem[id_frase]
        print(f"- {frase['texto_original']}  [fonte: {origem}]")

