# Boliche

> Projeto desenvolvido para a disciplina de **Computação Gráfica** da **Universidade Estadual do Ceará (UECE)**

## Sobre o Projeto

Jogo de boliche 2D onde toda a renderização foi feita manualmente usando `set_pixel`, implementando algoritmos clássicos de Computação Gráfica (Bresenham, scanline, flood fill, Cohen-Sutherland, etc).

## Estrutura do Projeto
Boliche/
├── main.py # Loop principal
├── pixel.py # Motor gráfico (set_pixel, linha, círculo, scanline, flood fill etc...)
├── cor.py # Cores predefinidas
├── input.py # Mouse e teclado
├── vetor.py # Classe Vec2
├── matriz.py # Classe Mat3
├── transformacoes.py # Matrizes de transformação (translação, rotação, escala)
├── clip.py # Cohen-Sutherland (clipping)
├── bola.py # Física e desenho da bola
├── pino.py # Física e desenho dos pinos
├── desenho.py # Cenário (pista, valas, tijolos, viewport)
├── menu.py # Interface do menu
├── menu_handler.py # Navegação do menu
├── jogo.py # Lógica principal (rounds, pontuação, colisões)
├── requirements.txt # Dependências
├── README.md # Este arquivo
└── imagem_textura/ # Pasta com a textura do quadro decorativo
    └── Layout.jpg


## 🎮 Física do Jogo

- **Movimento da bola**: translação + rotação (matrizes 3x3)
- **Colisões**: conservação de momento, coeficiente de restituição (0.3)
- **Efeito dominó**: pinos derrubam outros pinos
- **Gravidade e atrito**: aplicados ao movimento da bola

## 🎮 Como Jogar

- **Menu**: setas do teclado ou clique do mouse para navegar, ENTER para selecionar
- **Lançar bola**: clique na bola branca, arraste para trás (força) e para o lado (direção), solte
- **ESC**: volta ao menu durante o jogo

## ✅ Requisitos Atendidos

| Requisito | Implementação |
|-----------|---------------|
| Set Pixel | `pixel.py` - `set_pixel()` |
| Linha, Círculo, Elipse | `linha()`, `circulo()`, `elipse()` (Bresenham) |
| Flood Fill / Scanline | `flood_fill()`, `scanline_fill()` |
| Translação, Rotação, Escala | Matrizes 3x3 em `transformacoes.py` |
| Animação 2D | Movimento da bola, rotação, queda dos pinos |
| Janela e Viewport | `desenhar_janela_viewport()` em `pixel.py` - região do mundo centrada na bola mapeada para o canto inferior direito da tela |
| Clipping | Cohen-Sutherland nas laterais da pista |
| Textura | `texturizar_poligono()` com imagem externa |
| Input | Mouse para lançar bola, teclado para menu |
| Menu Interativo | Navegação por setas e mouse |
| Gradiente de cores | Interpolação por vértice nos polígonos (pista, valas) |

### 📝 Observações sobre a implementação

- **Linha, Círculo e Elipse**: Todos os desenhos geométricos utilizam o algoritmo de **Bresenham**, que calcula os pixels sem operações de ponto flutuante, garantindo eficiência e precisão.
- **Flood Fill**: Implementado com pilha manual para preencher regiões fechadas, utilizado na tela do menu e nos botões.
- **Scanline**: Responsável pelo preenchimento de polígonos (pinos, pista, valas), percorrendo linha por linha e preenchendo entre as interseções.
- **Transformações**: A rotação da bola e a queda dos pinos são aplicadas via **matrizes 3x3** (translação + rotação), demonstrando o uso de coordenadas homogêneas.
- **Escala**: A barra de força durante o lançamento da bola cresce proporcionalmente à força aplicada, demonstrando o conceito de **escala** em tempo real.
- **Clipping**: O algoritmo de **Cohen-Sutherland** é utilizado para recortar elementos que ultrapassam os limites da tela, como as laterais da pista e os tijolos da parede.
- **Textura**: Uma imagem externa é carregada e mapeada em um polígono (quadro decorativo) através de **scanline texture mapping**, lendo pixel a pixel com `get_at()` e desenhando com `set_pixel()`.
- **Viewport**: Durante o jogo, uma área ampliada mostra a bola em zoom no canto inferior direito, simulando uma câmera de acompanhamento.
- **Gradiente**: Utilizado na pista e nas valas, o gradiente é calculado interpolando as cores dos vértices de cada polígono. Na pista, há uma transição suave de tons de madeira da esquerda para a direita; nas valas, o gradiente simula profundidade (escuro → meio → escuro).

## 🎥 Demonstração

[Link do vídeo](https://www.youtube.com/watch?v=xAOb4GgGzPA)

## 🚀 Como Executar

```bash
# 1. Instale o Pygame
pip install pygame

# 2. Execute o jogo
python main.py
```

## Autor
- **Maurílio Salvaterra Cordeiro Neto**