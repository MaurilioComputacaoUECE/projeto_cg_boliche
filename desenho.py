"""
Classe Desenho - Gerencia toda a parte visual do jogo (cenário, interface, animações)
Atende aos requisitos: Gradiente por vértice, Textura, Scanline, Clipping, Viewport, Escala
"""

import math
import pygame
from cor import *
from bola import Bola
from pino import Pino
from clip import CohenSutherland


class Desenho:
    def __init__(self, g, largura, altura):
        """
        Inicializa o sistema de desenho com as dimensões da tela e carrega texturas.
        
        Parâmetros:
            g: instância da classe Pixel (motor gráfico)
            largura, altura: dimensões da tela em pixels
        """
        self.g = g
        self.largura = largura
        self.altura = altura
        self.chaoy = 550  # posição Y do chão (onde começa a pista)
        
        # Limites da pista e valas (para colisão e desenho)
        self.limite_pista_esq = self.largura//2 - 110   # borda esquerda da pista
        self.limite_pista_dir = self.largura//2 + 110   # borda direita da pista
        self.limite_vala_esq = self.limite_pista_esq - 60  # início da vala esquerda
        self.limite_vala_dir = self.limite_pista_dir + 60   # início da vala direita

        # Carrega textura para o quadro decorativo
        self.textura = pygame.image.load("imagem_textura/Layout.jpg")
    
    def desenhar_piso_chao(self):
        """
        Desenha o piso do chão com padrão xadrez.
        REQUISITO: Scanline Fill - cada quadrado é preenchido com scanline_fill
        """
        claro = (100, 85, 60)   # cor clara do xadrez
        escuro = (80, 70, 50)   # cor escura do xadrez
        tam = 40                 # tamanho de cada quadrado
        
        for y in range(80, self.chaoy, tam):
            for x in range(0, self.largura, tam):
                # Alterna as cores em xadrez (efeito tabuleiro)
                if ((x // tam) + (y // tam)) % 2 == 0:
                    cor = claro
                else:
                    cor = escuro
                
                vertices = [(x, y), (x + tam, y), (x + tam, y + tam), (x, y + tam)]
                self.g.scanline_fill(vertices, cor)  # Scanline Fill

    def desenhar_tijolos_parede(self):
        """
        Desenha a parede de tijolos na parte superior da tela.
        REQUISITO: Clipping (Cohen-Sutherland) - cada tijolo é recortado pelos limites da tela
        """
        largura_tijolo = 40
        altura_tijolo = 20
        altura_max = 80
        
        # Cria clipper para recortar tijolos que ultrapassam a tela
        clipper = CohenSutherland(0, 0, self.largura, self.altura)
        
        for y in range(0, altura_max, altura_tijolo):
            # Linhas ímpares têm deslocamento (efeito de tijolo real)
            linha_impar = ((y // altura_tijolo) % 2 == 1)
            x = -10 if linha_impar else 0
            
            while x < self.largura:
                x1, x2 = x, x + largura_tijolo - 1
                y1, y2 = y, y + altura_tijolo - 1
                
                # Aplica clipping no tijolo (só desenha o que está dentro da tela)
                resultado = clipper.clip(x1, y1, x2, y2)
                if resultado:
                    cx1, cy1, cx2, cy2 = resultado
                    vertices = [(cx1, cy1), (cx2, cy1), (cx2, cy2), (cx1, cy2)]
                    self.g.scanline_fill(vertices, (180, 80, 40))  # tijolo marrom
                    self.g.poligono(vertices, (150, 150, 150))     # borda cinza
                
                x += largura_tijolo
    
    def desenhar_quadro_textura(self, textura):
        """
        Desenha um quadro com textura na parede.
        REQUISITO: Mapeamento de Textura - aplica imagem Layout.jpg em um polígono
        """
        quadro_x, quadro_y = 580, 20
        quadro_largura, quadro_altura = 40, 40
        
        vertices = [(quadro_x, quadro_y), 
                    (quadro_x + quadro_largura, quadro_y),
                    (quadro_x + quadro_largura, quadro_y + quadro_altura),
                    (quadro_x, quadro_y + quadro_altura)]
        
        uvs = [(0, 0), (1, 0), (1, 1), (0, 1)]  # coordenadas de textura (0 a 1)
        
        self.g.texturizar_poligono(vertices, uvs, textura)  # aplica a imagem
        self.g.poligono(vertices, (150, 100, 50))  # moldura marrom

    def desenhar_fundo_preto_pinos(self):
        """
        Desenha o fundo preto atrás dos pinos (efeito de profundidade)
        REQUISITO: Set Pixel - usa set_pixel para cada ponto do fundo
        """
        fundo_esq = self.limite_vala_esq + 10
        fundo_dir = self.limite_vala_dir - 10
        
        for y in range(0, 80):
            for x in range(fundo_esq, fundo_dir):
                self.g.set_pixel(x, y, PRETO)
    
    def desenhar_tabuas_madeira(self):
        """
        Desenha molduras de madeira ao redor da área dos pinos.
        REQUISITO: Scanline Fill e Polígonos
        """
        fundo_esq = self.limite_vala_esq + 10
        fundo_dir = self.limite_vala_dir - 10
        
        # Tábua superior (0 a 10)
        vertices_topo = [(fundo_esq - 10, 0), (fundo_dir + 10, 0), 
                         (fundo_dir + 10, 10), (fundo_esq - 10, 10)]
        self.g.scanline_fill(vertices_topo, (160, 100, 50))
        self.g.poligono(vertices_topo, (100, 60, 30))
        
        # Tábua inferior (80 a 90)
        vertices_base = [(fundo_esq - 10, 80), (fundo_dir + 10, 80),
                         (fundo_dir + 10, 90), (fundo_esq - 10, 90)]
        self.g.scanline_fill(vertices_base, (160, 100, 50))
        self.g.poligono(vertices_base, (100, 60, 30))
        
        # Tábua vertical esquerda
        vertices_esq = [(fundo_esq - 10, 10), (fundo_esq, 10),
                        (fundo_esq, 80), (fundo_esq - 10, 80)]
        self.g.scanline_fill(vertices_esq, (160, 100, 50))
        self.g.poligono(vertices_esq, (100, 60, 30))
        
        # Tábua vertical direita
        vertices_dir = [(fundo_dir, 10), (fundo_dir + 10, 10),
                        (fundo_dir + 10, 80), (fundo_dir, 80)]
        self.g.scanline_fill(vertices_dir, (160, 100, 50))
        self.g.poligono(vertices_dir, (100, 60, 30))
    
    def desenhar_valas(self):
        """
        Desenha as valas laterais com gradiente de profundidade.
        REQUISITO: Gradiente por vértice (poligono_gradiente)
        """
        escuro = (10, 10, 10)
        meio = (40, 40, 40)
        
        # ========== VALA ESQUERDA (dois retângulos com gradiente) ==========
        metade = (self.limite_pista_esq + self.limite_vala_esq) // 2
        
        # 1º retângulo: escuro → meio
        pontos1_esq = [(self.limite_pista_esq, 80), (metade, 80), 
                       (metade, self.chaoy), (self.limite_pista_esq, self.chaoy)]
        cores1_esq = [escuro, meio, meio, escuro]
        self.g.poligono_gradiente(pontos1_esq, cores1_esq)  # Gradiente horizontal
        
        # 2º retângulo: meio → escuro
        pontos2_esq = [(metade, 80), (self.limite_vala_esq, 80),
                       (self.limite_vala_esq, self.chaoy), (metade, self.chaoy)]
        cores2_esq = [meio, escuro, escuro, meio]
        self.g.poligono_gradiente(pontos2_esq, cores2_esq)
        
        # ========== VALA DIREITA ==========
        metade_dir = (self.limite_pista_dir + self.limite_vala_dir) // 2
        
        pontos1_dir = [(self.limite_pista_dir, 80), (metade_dir, 80),
                       (metade_dir, self.chaoy), (self.limite_pista_dir, self.chaoy)]
        cores1_dir = [escuro, meio, meio, escuro]
        self.g.poligono_gradiente(pontos1_dir, cores1_dir)
        
        pontos2_dir = [(metade_dir, 80), (self.limite_vala_dir, 80),
                       (self.limite_vala_dir, self.chaoy), (metade_dir, self.chaoy)]
        cores2_dir = [meio, escuro, escuro, meio]
        self.g.poligono_gradiente(pontos2_dir, cores2_dir)
        
        # Bordas de madeira
        self.g.linha(self.limite_pista_esq, self.chaoy, self.limite_pista_esq, 80, (120, 100, 70))
        self.g.linha(self.limite_pista_dir, self.chaoy, self.limite_pista_dir, 80, (120, 100, 70))
    
    def desenhar_pista_principal(self):
        """
        Desenha a pista central com gradientes horizontais (efeito de iluminação)
        REQUISITO: Gradiente por vértice (poligono_gradiente)
        """
        largura_pista = self.limite_pista_dir - self.limite_pista_esq
        largura_ret = largura_pista // 5
        
        escuro = (80, 60, 40)
        medio = (120, 95, 65)
        claro = (160, 130, 90)
        
        # Configuração dos 5 retângulos com diferentes gradientes
        configs = [
            (escuro, claro),   # escuro → claro
            (claro, medio),    # claro → médio
            (medio, medio),    # médio uniforme
            (medio, claro),    # médio → claro
            (claro, escuro),   # claro → escuro
        ]
        
        for i in range(5):
            x1 = self.limite_pista_esq + i * largura_ret
            x2 = x1 + largura_ret
            cor_esq, cor_dir = configs[i]
            
            vertices = [(x1, 80), (x2, 80), (x2, self.chaoy), (x1, self.chaoy)]
            cores_vertices = [cor_esq, cor_dir, cor_dir, cor_esq]
            self.g.poligono_gradiente(vertices, cores_vertices)  # Gradiente horizontal
            
            # Bordas internas com cor de transição
            if i > 0:
                cor_borda = (
                    (configs[i-1][1][0] + cor_esq[0]) // 2,
                    (configs[i-1][1][1] + cor_esq[1]) // 2,
                    (configs[i-1][1][2] + cor_esq[2]) // 2
                )
                self.g.linha(x1, self.chaoy, x1, 80, cor_borda)
        
        # Bordas laterais
        self.g.linha(self.limite_pista_esq, self.chaoy, self.limite_pista_esq, 80, configs[0][0])
        self.g.linha(self.limite_pista_dir, self.chaoy, self.limite_pista_dir, 80, configs[-1][1])
    
    def copiar_pixels_para_lateral(self, offset_x):
        """
        Copia os pixels da pista para as laterais (cria pistas falsas decorativas)
        REQUISITO: Clipping (Cohen-Sutherland) - verifica limites antes de copiar
        """
        clipper = CohenSutherland(0, 0, self.largura, self.altura)
        area_x = self.limite_vala_esq
        area_largura = self.limite_vala_dir - self.limite_vala_esq
        
        # Verifica se a área está dentro da tela
        if clipper.clip(area_x, 0, area_x + area_largura, self.chaoy) is not None:
            # Lateral esquerda
            x_esq = area_x + offset_x
            if x_esq + area_largura <= self.largura:
                self.g.blit_simulado(self.g.tela, x_esq, 0, (area_x, 0, area_largura, self.chaoy))
            
            # Lateral direita
            x_dir = self.largura - (area_x + offset_x + area_largura)
            if x_dir >= 0:
                self.g.blit_simulado(self.g.tela, x_dir, 0, (area_x, 0, area_largura, self.chaoy))

    def desenhar_area_lancamento(self, bola_x, bola_y):
        """Desenha a área circular onde a bola fica antes do lançamento"""
        self.g.circulo(bola_x, bola_y, 25, CINZA)
        self.g.circulo(bola_x, bola_y, 18, BRANCO)
        self.g.linha(bola_x - 30, self.chaoy - 5, bola_x + 30, self.chaoy - 5, BRANCO)
    
    def desenhar_forca(self, arrastando, forca, angulo, bola_x, bola_y, chaoy):
        """
        Desenha barra de força usando MATRIZ DE ESCALA (requisito: Escala).
        A altura da barra escala conforme a força (0 a 100%).
        """
        if arrastando:
            from transformacoes import escala, translacao
            from matriz import Vec2
            
            fator = forca / 100.0  # 0 a 1
            
            # Matriz de escala: apenas no eixo Y
            M = translacao(30, chaoy) * escala(1, fator)
            
            # Retângulo base (largura 30, altura 100)
            base = [Vec2(0, 0), Vec2(30, 0), Vec2(30, -100), Vec2(0, -100)]
            pontos = [(int((M * v).x), int((M * v).y)) for v in base]
            
            self.g.scanline_fill(pontos, VERMELHO)
            self.g.poligono(pontos, BRANCO)
            
            # Seta de direção
            if forca > 0:
                x2 = bola_x + forca * math.cos(angulo)
                y2 = bola_y + forca * math.sin(angulo)
                self.g.linha(bola_x, bola_y, x2, y2, BRANCO)
    
    def desenhar_pinos(self, pinos):
        """Desenha todos os pinos (cada pino tem seu próprio método desenhar)"""
        for pino in pinos:
            pino.desenhar(self.g)
    
    def desenhar_bola(self, bola):
        """Desenha a bola (delega para o método desenhar da classe Bola)"""
        bola.desenhar(self.g)

    def desenhar_bola_com_viewport(self, bola):
        """
        Desenha uma viewport ampliada da bola no canto inferior direito.
        REQUISITO: Viewport e Zoom (Escala) - amplia a área ao redor da bola
        """
        self.g.desenhar_janela_viewport(bola.x, bola.y) 
    
    def desenhar_placar(self, pontos, round, max_rounds):
        """Desenha o placar com pontuação e round atual"""
        try:
            fonte = pygame.font.Font(None, 36)
            texto = fonte.render(f"Pontos: {pontos}  Round: {round}/{max_rounds}", True, BRANCO)
            self.g.tela.blit(texto, (20, 20))
        except:
            pass
    
    def desenhar_instrucao(self, lancando, arrastando):
        """Desenha instrução na tela para o jogador"""
        if not lancando and not arrastando:
            try:
                fonte = pygame.font.Font(None, 24)
                texto = fonte.render("Clique na bola e arraste para tras", True, CINZA_CLARO)
                self.g.tela.blit(texto, (self.largura//2 - 150, self.altura - 40))
            except:
                pass
    
    def desenhar_cenario(self, bola, pinos, pontos, lancando, arrastando, forca, angulo, round, max_rounds):
        """Método principal: desenha todo o cenário em ordem"""
        self.desenhar_piso_chao()
        self.desenhar_tijolos_parede()
        self.desenhar_quadro_textura(self.textura)
        self.desenhar_fundo_preto_pinos()
        self.desenhar_tabuas_madeira()
        self.desenhar_valas()
        self.desenhar_pista_principal()
        self.copiar_pixels_para_lateral(-400)
        self.copiar_pixels_para_lateral(400)
        self.desenhar_area_lancamento(bola.x, bola.y)
        self.desenhar_forca(arrastando, forca, angulo, bola.x, bola.y, self.chaoy)
        self.desenhar_pinos(pinos)
        self.desenhar_bola(bola)
        self.desenhar_placar(pontos, round, max_rounds)
        self.desenhar_bola_com_viewport(bola)
        self.desenhar_instrucao(lancando, arrastando)
    
    def desenhar_game_over(self, pontos, round, max_rounds):
        """Desenha a tela de fim de jogo"""
        self.g.limpar(PRETO)
        
        try:
            fonte = pygame.font.Font(None, 48)
            fonte_menor = pygame.font.Font(None, 32)
            
            titulo = fonte.render("FIM DE JOGO", True, AMARELO)
            self.g.tela.blit(titulo, (self.largura//2 - 100, 150))
            
            pontos_texto = fonte_menor.render(f"Pontuação final: {pontos}", True, BRANCO)
            self.g.tela.blit(pontos_texto, (self.largura//2 - 100, 250))
            
            rounds_texto = fonte_menor.render(f"Rounds completados: {round-1}/{max_rounds}", True, CINZA)
            self.g.tela.blit(rounds_texto, (self.largura//2 - 120, 300))
            
            instrucao = fonte_menor.render("Pressione ESC para voltar ao menu", True, CINZA)
            self.g.tela.blit(instrucao, (self.largura//2 - 180, 500))
        except:
            pass
        
        self.g.atualizar()