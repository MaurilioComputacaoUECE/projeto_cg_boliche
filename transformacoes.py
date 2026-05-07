"""
Transformações geométricas 2D usando matrizes homogêneas 3x3.
Atende aos requisitos: Translação, Rotação, Escala.
"""

import math
from matriz import Mat3

def translacao(dx, dy):
    """
    Retorna matriz de translação.
    Move um ponto por (dx, dy).
    """
    return Mat3([
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ])

def escala(sx, sy):
    """
    Retorna matriz de escala.
    Redimensiona um ponto por (sx, sy).
    """
    return Mat3([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

def rotacao(angulo_graus):
    """
    Retorna matriz de rotação (ângulo em graus).
    Gira um ponto ao redor da origem.
    """
    rad = math.radians(angulo_graus)
    cos = math.cos(rad)
    sen = math.sin(rad)
    return Mat3([
        [cos, -sen, 0],
        [sen,  cos, 0],
        [0,    0,   1]
    ])

def cisalhamento_x(k):
    """Cisalhamento no eixo X (transforma quadrado em paralelogramo)"""
    return Mat3([
        [1, k, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

def cisalhamento_y(k):
    """Cisalhamento no eixo Y"""
    return Mat3([
        [1, 0, 0],
        [k, 1, 0],
        [0, 0, 1]
    ])

def reflexao_x():
    """Reflete no eixo X (espelha verticalmente)"""
    return Mat3([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])

def reflexao_y():
    """Reflete no eixo Y (espelha horizontalmente)"""
    return Mat3([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

def reflexao_origem():
    """Reflete na origem (180 graus)"""
    return Mat3([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])