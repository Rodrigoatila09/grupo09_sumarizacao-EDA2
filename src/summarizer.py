
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


