"""
Classe Bola - Gerencia a física, movimento e rotação da bola de boliche
Atende aos requisitos: Translação, Rotação, Escala (via viewport), SetPixel, Círculo
"""

import math
from transformacoes import translacao, rotacao, escala
from matriz import Vec2
from cor import PRETO, CINZA, BRANCO

class Bola:
    def __init__(self, x, y, raio=25):
        """
        Inicializa a bola na posição (x, y) com um raio específico.
        
        Parâmetros:
            x, y: posição inicial em pixels
            raio: raio da bola em pixels
        
        Atributos de física:
            vx, vy: velocidade nos eixos X e Y (px/s)
            angulo: ângulo de rotação atual (graus)
            velocidade_angular: taxa de rotação (graus/s)
            massa: massa da bola (para cálculo de colisão)
        
        Atributos visuais:
            cor: cor da bola (PRETO)
            buracos: coordenadas locais dos 3 buracos (usando Vec2)
        """
        self.x = x
        self.y = y
        self.raio = raio
        self.vx = 0
        self.vy = 0
        self.angulo = 0
        self.velocidade_angular = 0
        self.no_chao = True
        self.cor = PRETO
        self.massa = 5
        
        # Posição dos 3 buracos (coordenadas LOCAIS, relativas ao centro)
        self.buracos = [
            Vec2(-self.raio/3, -self.raio/3),   # buraco superior esquerdo
            Vec2(self.raio/3, -self.raio/3),    # buraco superior direito
            Vec2(0, self.raio/4),               # buraco inferior central
        ]
    
    def lancar(self, forca, angulo_rad):
        """
        Lança a bola com uma força e ângulo específicos.
        
        Requisito atendido: Translação (a bola começa a se mover)
        
        Parâmetros:
            forca: intensidade do lançamento (0-100)
            angulo_rad: direção do lançamento em radianos
        
        A velocidade angular é proporcional à força, fazendo a bola girar mais rápido
        quanto mais forte for o lançamento.
        """
        self.vx = forca * 60 * math.cos(angulo_rad)
        self.vy = forca * 60 * math.sin(angulo_rad)
        self.velocidade_angular = forca * 60
        print(f"LANÇADO: vx={self.vx:.1f}, vy={self.vy:.1f}")
    
    def atualizar(self, dt, atrito=0.98, limites=(0, 0, 800, 600)):
        """
        Atualiza a posição e rotação da bola a cada frame.
        
        Requisitos atendidos:
            - Translação: atualiza x e y baseado na velocidade
            - Rotação: atualiza o ângulo baseado na velocidade angular
            - Animação 2D: movimento contínuo da bola
        
        Parâmetros:
            dt: delta time (tempo desde o último frame)
            atrito: fator de desaceleração (0.98 = perde 2% da velocidade por segundo)
            limites: tupla (x_min, y_min, x_max, y_max) para clipping da bola
        
        Aplica colisões com as bordas da tela (quique com perda de energia)
        """
        # Aplica atrito (desaceleração gradual)
        self.vx *= atrito
        self.vy *= atrito
        
        # Atualiza posição (Translação)
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Atualiza rotação (Rotação contínua)
        self.angulo += self.velocidade_angular * dt
        self.velocidade_angular *= atrito
        
        x_min, y_min, x_max, y_max = limites
        
        # Colisão com borda esquerda/direita (quique com perda de energia)
        if self.x - self.raio < x_min:
            self.x = x_min + self.raio
            self.vx = -self.vx * 0.5
        if self.x + self.raio > x_max:
            self.x = x_max - self.raio
            self.vx = -self.vx * 0.5
        
        # Colisão com borda superior/inferior
        if self.y - self.raio < y_min:
            self.y = y_min + self.raio
            self.vy = -self.vy * 0.5
        if self.y + self.raio > y_max:
            self.y = y_max - self.raio
            self.vy = -self.vy * 0.5
        
        # Para a bola completamente quando estiver muito lenta
        if abs(self.vx) < 1 and abs(self.vy) < 1:
            self.vx = 0
            self.vy = 0
            self.velocidade_angular = 0
    
    def desenhar(self, g):
        """
        Desenha a bola e seus buracos usando matrizes de transformação.
        
        Requisitos atendidos:
            - Set Pixel: indireto via g.circulo_preenchido()
            - Círculo: desenha a bola e os buracos
            - Transformações Geométricas: uso da matriz M = Translação * Rotação
            - Mapeamento de Textura: indireto (os buracos são preenchidos)
        
        A matriz M transforma as coordenadas locais dos buracos para coordenadas
        globais, aplicando rotação ao redor do centro da bola.
        """
        # MATRIZ DE TRANSFORMAÇÃO: Translação * Rotação (sem escala nos buracos)
        # A ordem correta: primeiro rotaciona (em torno da origem), depois translada
        M = translacao(self.x, self.y) * rotacao(self.angulo)
        
        # Bola preta (círculo no centro)
        g.circulo_preenchido(int(self.x), int(self.y), self.raio, self.cor)
        
        # Buracos (aplicando a matriz para que girem com a bola)
        raio_buraco = max(2, int(self.raio / 5))
        for buraco in self.buracos:
            p = M * buraco  # Aplica rotação e translação ao buraco
            g.circulo_preenchido(int(p.x), int(p.y), raio_buraco, CINZA)
            # Destaque interno (brilho) para dar efeito 3D
            g.circulo_preenchido(int(p.x) - 1, int(p.y) - 1, raio_buraco//2, BRANCO)