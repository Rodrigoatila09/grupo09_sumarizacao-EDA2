# Sumarizador de notícias da Copa do Mundo 2026

Sumarização extrativa multi-documento baseada em grafos, aplicada a notícias
da Copa do Mundo agregadas de vários portais (GE, UOL, ESPN). Projeto
acadêmico de Estruturas de Dados 2.

### Participantes

| Nome | Matrícula |
| --- | --- |
| Ângelo Cordova | 241025917 |
| Yan Santos | 241025480 |
| Rodrigo Átila | 241025855 |
| Pedro Inácio | 241026001 |
| Felipe Gomes | 241025766 |

## Restrições atendidas

- Os algoritmos de **grafo** (similaridade, matriz de adjacência, PageRank
  ponderado) são implementados **do zero**, sem networkx/igraph.
- NLTK é usado **apenas** no pré-processamento (tokenização de frases,
  stopwords PT, stemming RSLP). Não há uso de TF-IDF.
- O grafo é representado por **matriz de adjacência** (`src/graph.py`).
- Utilizamos mais estruturas de dados além do grafo:
  - **Max-heap** implementado do zero como a classe `MaxHeap`
    (`src/summarizer.py`): array interno + `inserir` com sift-up +
    `extrair_maximo` com sift-down, ambos O(log n).
  - **Tabela hash** (`dict` nativo do Python, usado apenas como container de
    chave/valor) em `src/summarizer.py`, mapeando frase → artigo de origem.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('rslp')"
```

## Como rodar

```bash
python main.py jogo01 6
```

O primeiro argumento é o nome da pasta em `data/` (um jogo); o segundo é o
número de frases desejadas no resumo final (default: 6). A entrada do
pipeline é sempre arquivos `.txt` já salvos em `data/<jogo>/`, um por
portal.

## Pipeline

```
data/<jogo>/*.txt
    -> preprocess.py   (lê artigos, segmenta frases, stopwords + stemming)
    -> graph.py         (similaridade TextRank + matriz de adjacência ponderada)
    -> pagerank.py      (PageRank ponderado via power method, do zero)
    -> summarizer.py    (MaxHeap do zero + tabela hash + anti-redundância)
    -> newsletter.py    (saída em Markdown com referência à fonte)
    -> analysis.py       (scores do PageRank, arestas mais fortes, seleção do resumo, taxa de compressão)
```

`graph.py` reúne tanto o cálculo de similaridade (fórmula original do
TextRank) quanto a classe `Grafo` baseada em matriz de
adjacência, já que uma é construída diretamente a partir da outra.

## Relatório de análise (`analysis.py`)

Em vez de métricas estatísticas (ROUGE, redução de redundância etc.),
`analysis.py` imprime um relatório legível com:

1. todos os vértices/frases com seu score de PageRank, em ordem decrescente;
2. as arestas de maior peso de similaridade do grafo;
3. quais frases entraram no resumo final, com a fonte de cada uma;
4. a taxa de compressão (`frases_resumo / frases_total`) como único número
   calculado.
