"""
Classe Mat3 - Matriz 3x3 para transformações geométricas 2D.
Atende aos requisitos: Transformações Geométricas (Rotação, Translação, Escala)
"""

from vetor import Vec2

class Mat3:
    """
    Matriz 3x3 para transformações homogêneas em 2D.
    
    Estrutura:
        [ a  b  tx ]
        [ c  d  ty ]
        [ 0  0  1  ]
    
    Onde (a,b,c,d) definem rotação/escala e (tx,ty) definem translação.
    """
    
    def __init__(self, dados=None):
        """
        Inicializa a matriz.
        Se nenhum dado for fornecido, cria a matriz identidade.
        
        Parâmetros:
            dados: lista 3x3 opcional com os valores da matriz
        """
        if dados:
            self.m = dados
        else:
            # Matriz identidade (não transforma o ponto)
            self.m = [[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]]
    
    def __mul__(self, v):
        """
        Multiplica a matriz por um vetor ou por outra matriz.
        
        Caso 1: Matriz * Vetor (transforma um ponto)
        Caso 2: Matriz * Matriz (concatena transformações)
        
        REQUISITO: Transformações Geométricas (multiplicação de matrizes)
        """
        if isinstance(v, Vec2):
            # Matriz * Vetor: aplica a transformação ao ponto (x,y)
            x = self.m[0][0] * v.x + self.m[0][1] * v.y + self.m[0][2]
            y = self.m[1][0] * v.x + self.m[1][1] * v.y + self.m[1][2]
            return Vec2(x, y)
        
        elif isinstance(v, Mat3):
            # Matriz * Matriz: concatena duas transformações
            # A ordem importa: M1 * M2 (aplica M2 primeiro, depois M1)
            resultado = [[0, 0, 0] for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    soma = 0
                    for k in range(3):
                        soma += self.m[i][k] * v.m[k][j]
                    resultado[i][j] = soma
            return Mat3(resultado)
    
    def __repr__(self):
        """Representação textual da matriz para debugging"""
        return f"Mat3({self.m[0]},{self.m[1]},{self.m[2]})"