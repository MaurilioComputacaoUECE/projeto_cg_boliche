import math
"""
Classe Pino - Representa um pino de boliche.
Atende aos requisitos: Polígonos, Scanline Fill, Transformações (Rotação, Translação),
                      Gradiente (indireto via cores), Colisões (física)
"""

import math
from transformacoes import translacao, rotacao, escala
from matriz import Vec2
from cor import BRANCO, VERMELHO, CINZA

class Pino:
    """
    Pino de boliche com física de colisão, animação de queda e pontuação.
    """
    
    def __init__(self, x, y, largura=20, altura=35):
        """
        Inicializa o pino na posição (x, y) com as dimensões especificadas.
        
        Parâmetros:
            x, y: posição do centro do pino
            largura, altura: dimensões do pino em pixels
        """
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.angulo = 0           # ângulo de rotação (queda)
        self.caindo = False       # indica se o pino está caindo
        self.velocidade_queda = 15  # velocidade angular da queda
        self.vx = 0               # velocidade horizontal (empurrão)
        self.vy = 0               # velocidade vertical
        self.massa = 2            # massa para cálculo de colisão
        self.pontuado = False     # se já contabilizou pontos

        # Largura do topo (pescoço) - bem estreito
        largura_topo = largura / 5
        
        # Vértices do corpo (base larga que afina até o topo)
        self.vertices_local = [
            # Topo (pescoço estreito)
            Vec2(-largura_topo/2, -altura),   # esquerdo topo
            Vec2(largura_topo/2, -altura),    # direito topo
            
            # Corpo (afinando gradualmente)
            Vec2(largura/2.5, -altura/2),     # meio direito
            Vec2(largura/2, 0),               # base direita
            
            # Base
            Vec2(largura/2, 0),               # base direita
            Vec2(-largura/2, 0),              # base esquerda
            
            # Corpo (afinando gradualmente)
            Vec2(-largura/2.5, -altura/2),    # meio esquerdo
        ]
        
        # Cabeça do pino (círculo)
        self.raio_cabeca = int(largura / 3)
        self.cabeca_y = -altura - self.raio_cabeca/2
    
    def derrubar(self, pontuar=False):
        """
        Derruba o pino, iniciando a animação de queda.
        Se pontuar=True e ainda não pontuou, marca como pontuado.
        """
        if not self.caindo:
            self.caindo = True
            if pontuar and not self.pontuado:
                self.pontuado = True
                return True
        return False
    
    def atualizar(self, dt, limites=(0, 0, 800, 600), outros_pinos=None):
        """
        Atualiza a física do pino (posição, velocidade, queda).
        Requisitos: Translação (movimento do pino ao ser atingido),
                    Rotação (queda)
        """
        # Atualiza posição com velocidade (translação)
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Aplica atrito
        self.vx *= 0.95
        self.vy *= 0.95
        
        # Limites da tela
        x_min, y_min, x_max, y_max = limites
        self.x = max(x_min + self.largura/2, min(self.x, x_max - self.largura/2))
        self.y = max(y_min + self.altura/2, min(self.y, y_max - self.altura/2))
        
        # Verifica colisão com outros pinos (efeito dominó)
        if outros_pinos:
            self.verificar_colisao_pino_pino(outros_pinos)
        
        # Animação de queda (rotação)
        if self.caindo:
            self.angulo += self.velocidade_queda * dt
            if self.angulo >= 90:
                self.angulo = 90
                self.vx = 0
                self.vy = 0
    
    def colidiu(self, bola, dt):
        """
        Verifica colisão entre o pino e a bola.
        Aplica impulso para bola e pino baseado na conservação de momento.
        Requisito: Animação 2D (colisão com física)
        """
        # Hitbox do pino (retângulo)
        pino_esquerda = self.x - self.largura/2
        pino_direita = self.x + self.largura/2
        pino_topo = self.y - self.altura/2
        pino_base = self.y + self.altura/2
        
        # Hitbox da bola (círculo)
        bola_esquerda = bola.x - bola.raio
        bola_direita = bola.x + bola.raio
        bola_topo = bola.y - bola.raio
        bola_base = bola.y + bola.raio
        
        # Colisão entre retângulo e círculo
        colidiu = not (bola_direita < pino_esquerda or 
                       bola_esquerda > pino_direita or
                       bola_base < pino_topo or
                       bola_topo > pino_base)
        
        if colidiu and not self.caindo:
            print(f"COLISÃO! Pino em ({self.x:.0f},{self.y:.0f})")
            
            # Vetor normal da colisão
            dx = self.x - bola.x
            dy = self.y - bola.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist == 0:
                return False
            
            nx = dx / dist
            ny = dy / dist
            
            # Velocidade relativa
            vrelx = bola.vx - self.vx
            vrely = bola.vy - self.vy
            vrel = vrelx * nx + vrely * ny
            
            # Coeficiente de restituição (0.3 = perda de energia)
            e = 0.3
            m_bola = bola.massa
            m_pino = self.massa
            
            # Impulso (conservação de momento)
            j = -(1 + e) * vrel / (1/m_bola + 1/m_pino)
            
            # Aplica impulso na bola
            bola.vx += j * nx / m_bola
            bola.vy += j * ny / m_bola
            
            # Aplica impulso no pino
            self.vx = -j * nx / m_pino
            self.vy = -j * ny / m_pino
            
            # Derruba o pino e marca para pontuação
            self.derrubar(pontuar=True)
            self.angulo = 15
            
            return True
        return False

    def verificar_colisao_pino_pino(self, outros_pinos):
        """
        Verifica colisão deste pino com outros pinos (efeito dominó).
        Quando um pino cai e bate em outro, o outro também cai.
        """
        if not self.caindo:
            return False
        
        for outro in outros_pinos:
            if outro is self or outro.caindo:
                continue
            
            # Verifica se os retângulos colidem
            if (abs(self.x - outro.x) < (self.largura + outro.largura) / 2 and
                abs(self.y - outro.y) < (self.altura + outro.altura) / 2):
                
                print(f"  EFEITO DOMINÓ!")
                outro.derrubar(pontuar=True)
                outro.angulo = 15
                outro.vx = self.vx * 0.5
                outro.vy = self.vy * 0.5
                return True
        return False
    
    def desenhar(self, g):
        """
        Desenha o pino usando matrizes de transformação.
        Requisitos: Transformações (Translação + Rotação), 
                    Scanline Fill (preenchimento do polígono)
        """
        if self.angulo >= 90:
            return  # Pino já caiu completamente
        
        # Matriz de transformação: Translação * Rotação
        M = translacao(self.x, self.y) * rotacao(self.angulo) * escala(1, 1)
        
        # Corpo principal (polígono preenchido com scanline)
        vertices = [M * v for v in self.vertices_local]
        pontos = [(int(v.x), int(v.y)) for v in vertices]
        g.scanline_fill(pontos, BRANCO)
        g.poligono(pontos, CINZA)
        
        # Cabeça (círculo) - também transformada pela matriz
        cabeca_local = Vec2(0, self.cabeca_y)
        cabeca = M * cabeca_local
        
        g.circulo_preenchido(int(cabeca.x), int(cabeca.y), self.raio_cabeca, BRANCO)
        g.circulo(int(cabeca.x), int(cabeca.y), self.raio_cabeca, CINZA)
        
        # Listra vermelha decorativa
        listra_local = [
            Vec2(-self.largura/6, -self.altura + 3),
            Vec2(self.largura/6, -self.altura + 3),
            Vec2(self.largura/7, -self.altura + 8),
            Vec2(-self.largura/7, -self.altura + 8),
        ]
        listra = [M * v for v in listra_local]
        pontos_listra = [(int(v.x), int(v.y)) for v in listra]
        g.scanline_fill(pontos_listra, VERMELHO)