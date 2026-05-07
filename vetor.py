"""
Classe Vec2 - Vetor 2D para operações geométricas.
Atende aos requisitos: Transformações Geométricas (operações com vetores).
"""

class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Soma de vetores"""
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, escalar):
        """Multiplicação por escalar"""
        return Vec2(self.x * escalar, self.y * escalar)
    
    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"