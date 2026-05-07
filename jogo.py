"""
Módulo do jogo Boliche 
Gerencia a lógica principal do jogo, física, colisões e estado dos rounds.
Atende aos requisitos: Animação 2D, Translação, Rotação, Input (mouse/teclado)
"""

import math
from bola import Bola
from pino import Pino
from desenho import Desenho
from cor import *


class Jogo:
    """
    Classe principal do jogo. Controla:
    - Estado do jogo (rounds, pontuação)
    - Física da bola e pinos
    - Colisões
    - Input do mouse para lançamento
    """
    
    def __init__(self, g, input):
        """
        Inicializa o jogo com o motor gráfico e sistema de input.
        
        Parâmetros:
            g: instância da classe Pixel (motor gráfico)
            input: instância da classe Input (teclado/mouse)
        """
        self.g = g
        self.input = input
        self.largura = 800
        self.altura = 600
        self.dt = 1/60  # delta time para física (60 FPS)
        
        self.desenho = Desenho(g, self.largura, self.altura)
        
        # Estado do jogo
        self.bola = None
        self.pinos_principal = []
        self.pontos_total = 0      # pontos acumulados de todos os rounds
        self.pontos_round = 0      # pontos do round atual
        self.round = 1
        self.max_rounds = 5
        self.jogo_finalizado = False
        
        # Estado do lançamento
        self.lancando = False      # bola está em movimento
        self.arrastando = False    # mouse está arrastando para lançar
        self.forca = 0             # força do lançamento (0-100)
        self.angulo = 0            # direção do lançamento (radianos)
        self.pos_inicial = (0, 0)  # posição inicial do arrasto
        
        self.iniciar_jogo()
    
    def iniciar_jogo(self):
        """
        Inicia ou reinicia o jogo.
        Cria a bola e os pinos nas posições iniciais.
        """
        # Bola na posição inicial (centro inferior)
        self.bola = Bola(self.largura//2, self.altura - 60, raio=25)
        
        centro = self.largura//2
        
        # Posições dos pinos em formato de triângulo (4 fileiras)
        posicoes_principal = [
            # Fileira 1 (mais atrás) - 1 pino
            (centro, 165),    
            # Fileira 2 - 2 pinos
            (centro - 25, 150), (centro + 25, 150),
            # Fileira 3 - 3 pinos
            (centro - 50, 120), (centro, 120), (centro + 50, 120),
            # Fileira 4 (mais perto) - 4 pinos
            (centro - 70, 105), (centro - 25, 105), (centro + 25, 105), (centro + 70, 105),
        ]
        
        self.pinos_principal = []
        for x, y in posicoes_principal:
            self.pinos_principal.append(Pino(x, y, largura=20, altura=35))
        
        self.pontos_total = 0
        self.pontos_round = 0
        self.lancando = False
        self.arrastando = False
        self.forca = 0
        self.angulo = 0
    
    def proximo_round(self):
        """
        Prepara o próximo round.
        Reseta a bola e os pinos, mantém a pontuação acumulada.
        Retorna False se o jogo acabou.
        """
        self.round += 1
        if self.round > self.max_rounds:
            self.jogo_finalizado = True
            print(f"FIM DE JOGO! Pontuação final: {self.pontos_total}")
            return False
        
        print(f"\n=== ROUND {self.round} ===")
        
        # Reseta a bola
        self.bola = Bola(self.largura//2, self.altura - 60, raio=25)
        
        # Recria os pinos
        centro = self.largura//2
        posicoes_principal = [
            (centro, 165), (centro - 25, 150), (centro + 25, 150),
            (centro - 50, 120), (centro, 120), (centro + 50, 120),
            (centro - 70, 105), (centro - 25, 105), (centro + 25, 105), (centro + 70, 105),
        ]
        
        self.pinos_principal = []
        for x, y in posicoes_principal:
            self.pinos_principal.append(Pino(x, y, largura=20, altura=35))
        
        self.pontos_round = 0
        self.lancando = False
        self.arrastando = False
        self.forca = 0
        
        return True
    
    def processar_input(self):
        """
        Processa entrada do mouse para o lançamento da bola.
        - Clique na bola: inicia arrasto
        - Arrasto: define força e ângulo
        - Soltar: lança a bola
        Requisito: Input (mouse)
        """
        if self.jogo_finalizado:
            return
        
        # Aguardando lançamento
        if not self.lancando and not self.arrastando:
            if self.input.mouse_clicou_esquerdo():
                mx, my = self.input.mouse_pos()
                dx = self.bola.x - mx
                dy = self.bola.y - my
                # Verifica se clicou na bola
                if abs(dx) < self.bola.raio and abs(dy) < self.bola.raio:
                    self.arrastando = True
                    self.pos_inicial = (mx, my)
        
        # Arrastando o mouse (calcula força e ângulo)
        if self.arrastando and self.input.mouse_pressionado_esquerdo():
            x_atual, y_atual = self.input.mouse_pos()
            dx = self.pos_inicial[0] - x_atual
            dy = self.pos_inicial[1] - y_atual
            
            distancia = math.sqrt(dx*dx + dy*dy)
            self.forca = min(distancia, 100)           # Força de 0 a 100
            self.angulo = math.atan2(dy, dx)           # Direção do lançamento
        
        # Soltou o mouse -> lança a bola
        if self.arrastando and not self.input.mouse_pressionado_esquerdo():
            self.arrastando = False
            if self.forca > 3:                         # Força mínima para lançar
                self.lancando = True
                self.bola.lancar(self.forca, self.angulo)
                print(f"Round {self.round} - Lançado! Força={self.forca:.1f}")
            self.forca = 0
    
    def atualizar(self):
        """
        Atualiza a física do jogo a cada frame.
        - Movimento da bola (Translação e Rotação)
        - Colisões com pinos
        - Verifica se bola saiu da pista (vala ou fundo preto)
        Requisitos: Translação, Rotação, Animação 2D
        """
        if self.jogo_finalizado:
            return
        
        if self.lancando:
            limites = (0, 0, self.largura, self.altura)
            self.bola.atualizar(self.dt, atrito=0.98, limites=limites)
            
            # Verifica colisão bola-pino
            for pino in self.pinos_principal:
                pino.colidiu(self.bola, self.dt)
            
            # Atualiza animação dos pinos (queda)
            for pino in self.pinos_principal:
                pino.atualizar(self.dt, limites, self.pinos_principal)

            # Calcula pontos do round (10 pontos por pino derrubado)
            self.pontos_round = sum(10 for p in self.pinos_principal if p.pontuado)

            # ========== LIMITES DA PISTA ==========
            # Verifica se a bola saiu da pista (caiu na vala ou fundo preto)
            pista_esq = self.desenho.limite_pista_esq
            pista_dir = self.desenho.limite_pista_dir
            fundo_preto_y = 80
            
            if (self.bola.x < pista_esq or self.bola.x > pista_dir or 
                self.bola.y < fundo_preto_y):
                print("BOLA SAIU DA PISTA!")
                self.pontos_total += self.pontos_round
                self.lancando = False
                self.proximo_round()
                return
            
            # Verifica se a bola parou naturalmente
            parou = abs(self.bola.vx) < 1 and abs(self.bola.vy) < 1
            saiu = (self.bola.x > self.largura + 100 or self.bola.x < -100 or
                    self.bola.y > self.altura + 100 or self.bola.y < -100)
            
            if parou or saiu:
                self.pontos_total += self.pontos_round
                self.lancando = False
                self.proximo_round()
    
    def desenhar(self):
        """
        Desenha todo o conteúdo do jogo.
        Delega para a classe Desenho o desenho do cenário, bola e pinos.
        """
        if self.jogo_finalizado:
            self.desenho.desenhar_game_over(self.pontos_total, self.round, self.max_rounds)
        else:
            self.desenho.desenhar_cenario(
                self.bola, self.pinos_principal, self.pontos_total, 
                self.lancando, self.arrastando, self.forca, self.angulo,
                self.round, self.max_rounds
            )
    
    def finalizado(self):
        """Retorna True se o jogo terminou"""
        return self.jogo_finalizado
    
    def get_pontos(self):
        """Retorna a pontuação total atual"""
        return self.pontos_total