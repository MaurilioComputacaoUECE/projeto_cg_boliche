"""
Menu do jogo Boliche
Atende aos requisitos: Rasterização (elipse, círculo, linha), Flood Fill, Input (mouse/teclado)
"""

import pygame
from cor import *

class Menu:
    """
    Classe responsável pelo desenho e interação do menu principal e tela de instruções.
    """
    
    def __init__(self, g, largura, altura):
        """
        Inicializa o menu com as dimensões da tela.
        
        Parâmetros:
            g: instância da classe Pixel (motor gráfico)
            largura, altura: dimensões da tela em pixels
        """
        self.g = g
        self.largura = largura
        self.altura = altura
        self.opcoes = ["JOGAR", "INSTRUCOES", "SAIR"]
        self.opcao_selecionada = 0
        self.fonte_titulo = pygame.font.Font(None, 80)
        self.fonte = pygame.font.Font(None, 48)
        self.fonte_pequena = pygame.font.Font(None, 28)
    
    def desenhar(self):
        """
        Desenha a tela principal do menu.
        Requisitos:
            - Elipse (título)
            - Círculo (bola de boliche)
            - Flood Fill (preenchimento dos botões)
            - Scanline (fundo da tela)
        """
        # Fundo da tela (azul escuro) usando scanline
        tela_pontos = [(0, 0), (self.largura, 0), 
                       (self.largura, self.altura), (0, self.altura)]
        self.g.scanline_fill(tela_pontos, (20, 20, 80))
        
        # Título com elipse
        self.g.elipse(self.largura//2, 100, 350, 70, AMARELO)
        titulo = self.fonte_titulo.render("BOLICHE", True, AMARELO)
        self.g.tela.blit(titulo, (self.largura//2 - 100, 65))
        
        # Bola de boliche (círculo preenchido)
        self.g.circulo_preenchido(self.largura//2, 240, 45, (80, 80, 80))
        
        # Três buracos da bola
        self.g.circulo_preenchido(self.largura//2 - 12, 228, 7, (150, 150, 150))
        self.g.circulo_preenchido(self.largura//2 + 12, 228, 7, (150, 150, 150))
        self.g.circulo_preenchido(self.largura//2, 250, 7, (150, 150, 150))
        
        # Botões do menu
        for i, opcao in enumerate(self.opcoes):
            y = 370 + i * 60
            cor = AMARELO if i == self.opcao_selecionada else (50, 50, 50)
            
            # Contorno do botão
            pontos = [(self.largura//2 - 120, y), 
                      (self.largura//2 + 120, y),
                      (self.largura//2 + 120, y + 45),
                      (self.largura//2 - 120, y + 45)]
            self.g.poligono(pontos, (255, 255, 255))
            
            # Preenchimento do botão com Flood Fill
            self.g.flood_fill(self.largura//2, y + 22, cor, (20, 20, 80))
            
            # Texto do botão (centralizado)
            texto_surface = self.fonte.render(opcao, True, PRETO)
            largura_texto = texto_surface.get_width()
            x_texto = self.largura//2 - largura_texto // 2
            self.g.tela.blit(texto_surface, (x_texto, y + 10))
        
        # Rodapé com instruções
        rodape = self.fonte_pequena.render("SETAS: navegar | ENTER: selecionar", True, CINZA)
        self.g.tela.blit(rodape, (self.largura//2 - 200, self.altura - 30))
        
        self.g.atualizar()
    
    def desenhar_instrucoes(self):
        """
        Desenha a tela de instruções do jogo.
        Requisitos: Linha (separador), Texto informativo
        """
        # Fundo da tela
        tela_pontos = [(0, 0), (self.largura, 0), 
                       (self.largura, self.altura), (0, self.altura)]
        self.g.scanline_fill(tela_pontos, (20, 20, 80))
        
        # Cabeçalho
        self.g.elipse(self.largura//2, 80, 300, 60, AMARELO)
        titulo = self.fonte.render("BOLICHE", True, PRETO)
        self.g.tela.blit(titulo, (self.largura//2 - 70, 60))
        
        subtitulo = self.fonte.render("INSTRUCOES", True, AMARELO)
        self.g.tela.blit(subtitulo, (self.largura//2 - 100, 160))
        
        # Linha separadora (uso do algoritmo de linha)
        for x in range(100, self.largura - 100):
            self.g.set_pixel(x, 150, AMARELO)
        
        # Lista de instruções
        instrucoes = [
            "1. Clique na bola branca",
            "2. Arraste para tras = FORCA",
            "3. Arraste para lado = DIRECAO",
            "4. Solte o mouse = LANCAR",
            "5. Derrube os pinos amarelos"
        ]
        
        y = 300
        for texto in instrucoes:
            linha = self.fonte_pequena.render(texto, True, BRANCO)
            self.g.tela.blit(linha, (150, y))
            y += 40
        
        # Botão de voltar
        voltar = self.fonte_pequena.render("PRESSIONE ESPACO PARA VOLTAR", True, AMARELO)
        largura_voltar = voltar.get_width()
        self.g.tela.blit(voltar, (self.largura//2 - largura_voltar//2, self.altura - 80))
        
        self.g.atualizar()
    
    def processar_clique(self, mx, my):
        """Verifica se um clique ocorreu dentro de algum botão do menu"""
        for i in range(len(self.opcoes)):
            y = 370 + i * 60
            if (self.largura//2 - 100 <= mx <= self.largura//2 + 100 and 
                y <= my <= y + 45):
                return self.opcoes[i]
        return None
    
    def navegar(self, direcao):
        """Navega entre as opções do menu com as setas do teclado"""
        self.opcao_selecionada = (self.opcao_selecionada + direcao) % len(self.opcoes)