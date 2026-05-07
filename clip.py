"""
Classe CohenSutherland - Implementa o algoritmo de clipping (recorte) de linhas em 2D.
Atende ao requisito: Recorte de Cohen-Sutherland (Clipping)

O algoritmo divide o plano em 9 regiões usando códigos de 4 bits (outcodes):
- Bit 1 (LEFT):   ponto está à esquerda da janela
- Bit 2 (RIGHT):  ponto está à direita da janela
- Bit 3 (BOTTOM): ponto está abaixo da janela
- Bit 4 (TOP):    ponto está acima da janela

O código 0000 (INSIDE) significa que o ponto está dentro da janela.
"""

class CohenSutherland:
    """Clipping de linhas 2D usando algoritmo de Cohen-Sutherland"""
    
    # Códigos de região (outcodes) - constantes da classe
    INSIDE = 0  # 0000 - dentro da janela
    LEFT = 1    # 0001 - esquerda
    RIGHT = 2   # 0010 - direita
    BOTTOM = 4  # 0100 - abaixo
    TOP = 8     # 1000 - acima
    
    def __init__(self, x_min, y_min, x_max, y_max):
        """
        Inicializa o clipper com os limites da janela de recorte.
        
        Parâmetros:
            x_min, y_min: canto superior esquerdo da janela
            x_max, y_max: canto inferior direito da janela
        """
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
    
    def _calcular_codigo(self, x, y):
        """
        Calcula o código de região para um ponto (x, y).
        Retorna um número de 4 bits onde cada bit representa uma posição relativa à janela.
        
        Exemplo: ponto à esquerda e acima → LEFT | TOP = 1 | 8 = 9 (1001 em binário)
        """
        codigo = self.INSIDE
        
        if x < self.x_min:
            codigo |= self.LEFT      # liga o bit da esquerda
        elif x > self.x_max:
            codigo |= self.RIGHT     # liga o bit da direita
        
        if y < self.y_min:
            codigo |= self.BOTTOM    # liga o bit de baixo
        elif y > self.y_max:
            codigo |= self.TOP       # liga o bit de cima
        
        return codigo
    
    def _intersectar(self, x1, y1, x2, y2, codigo):
        """
        Calcula a interseção da linha com a borda da janela indicada pelo código.
        
        Parâmetros:
            x1, y1, x2, y2: extremos da linha
            codigo: código da borda a ser calculada (LEFT, RIGHT, BOTTOM ou TOP)
        
        Retorna: (x, y) ponto de interseção
        """
        # Calcula o parâmetro t para interpolação linear
        if x2 != x1:
            t = (self.x_min - x1) / (x2 - x1)
        else:
            t = 0
        
        # Calcula interseção com a borda apropriada
        if codigo & self.LEFT:      # Interseção com borda esquerda
            y = y1 + t * (y2 - y1)
            return (self.x_min, y)
        
        if codigo & self.RIGHT:     # Interseção com borda direita
            if x2 != x1:
                t = (self.x_max - x1) / (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (self.x_max, y)
        
        if codigo & self.BOTTOM:    # Interseção com borda inferior
            if y2 != y1:
                t = (self.y_min - y1) / (y2 - y1)
            x = x1 + t * (x2 - x1)
            return (x, self.y_min)
        
        if codigo & self.TOP:       # Interseção com borda superior
            if y2 != y1:
                t = (self.y_max - y1) / (y2 - y1)
            x = x1 + t * (x2 - x1)
            return (x, self.y_max)
        
        return (x1, y1)  # não deveria chegar aqui
    
    def clip(self, x1, y1, x2, y2):
        """
        Aplica clipping na linha (x1,y1)-(x2,y2).
        
        Retorna:
            (x1, y1, x2, y2) - linha recortada (se visível)
            None - linha totalmente invisível
        
        Algoritmo:
            1. Calcula códigos dos dois pontos
            2. Se ambos dentro (códigos zero) → ACEITA
            3. Se ambos fora do mesmo lado (códigos & != 0) → REJEITA
            4. Caso contrário, calcula interseção com uma borda e repete
        """
        x1_atual, y1_atual = x1, y1
        x2_atual, y2_atual = x2, y2
        
        while True:
            codigo1 = self._calcular_codigo(x1_atual, y1_atual)
            codigo2 = self._calcular_codigo(x2_atual, y2_atual)
            
            # CASO 1: ambos dentro → linha totalmente visível
            if codigo1 == 0 and codigo2 == 0:
                return (int(x1_atual), int(y1_atual), int(x2_atual), int(y2_atual))
            
            # CASO 2: ambos fora do mesmo lado → linha totalmente invisível
            if codigo1 & codigo2 != 0:
                return None
            
            # CASO 3: um ou ambos fora → calcular interseção
            # Escolhe um ponto fora para recortar
            codigo = codigo1 if codigo1 != 0 else codigo2
            
            # Calcula interseção com a borda
            x_int, y_int = self._intersectar(x1_atual, y1_atual, 
                                            x2_atual, y2_atual, codigo)
            
            # Substitui o ponto fora pelo ponto de interseção
            if codigo == codigo1:
                x1_atual, y1_atual = x_int, y_int
            else:
                x2_atual, y2_atual = x_int, y_int
    
    def clip_poligono_borda(self, vertices, borda):
        """
        Clipe um polígono contra uma borda específica (Sutherland-Hodgman).
        
        Parâmetros:
            vertices: lista de pontos (x,y) do polígono
            borda: tupla (x_min, y_min, x_max, y_max)
        
        Retorna: lista de vértices do polígono recortado
        
        Nota: Este método não está completo (faltam as funções ponto_dentro e intersectar).
        Para uso completo, seriam necessários:
            - self.ponto_dentro(p, borda): verifica se ponto está dentro
            - self.intersectar(p1, p2, borda): calcula interseção com a borda
        """
        novos_vertices = []
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i+1) % len(vertices)]
            
            dentro1 = self.ponto_dentro(p1, borda)
            dentro2 = self.ponto_dentro(p2, borda)
            
            if dentro1 and dentro2:          # Caso 1: ambos dentro → adiciona p2
                novos_vertices.append(p2)
            elif dentro1 and not dentro2:    # Caso 2: saindo → adiciona interseção
                novos_vertices.append(self.intersectar(p1, p2, borda))
            elif not dentro1 and dentro2:    # Caso 3: entrando → adiciona interseção e p2
                novos_vertices.append(self.intersectar(p1, p2, borda))
                novos_vertices.append(p2)
            # Caso 4: ambos fora → nada
        return novos_vertices