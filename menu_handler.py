"""
MenuHandler - Gerencia a navegação entre telas (menu principal, instruções, jogo)
Atende aos requisitos: Menu interativo, Input (teclado/mouse)
"""

import pygame
from cor import *

class MenuHandler:
    """
    Controla o estado atual da interface (menu, instruções, jogo)
    e processa as entradas do usuário para navegação.
    """
    
    def __init__(self, g, input):
        """
        Inicializa o gerenciador de estado do menu.
        
        Parâmetros:
            g: instância da classe Pixel (motor gráfico)
            input: instância da classe Input (teclado/mouse)
        """
        self.g = g
        self.input = input
        self.estado = "MENU"      # MENU, INSTRUCOES, JOGO
        self.pontos = 0
    
    def atualizar(self, menu):
        """
        Processa a navegação do menu a cada frame.
        Retorna False se o usuário escolheu SAIR.
        
        Requisitos:
            - Input via teclado (setas e ENTER)
            - Input via mouse (clique nos botões)
            - Menu interativo
        """
        if self.estado == "MENU":
            menu.desenhar()
            
            # ===== NAVEGAÇÃO POR TECLADO =====
            if self.input.seta_cima():
                menu.navegar(-1)
                pygame.time.wait(150)
            if self.input.seta_baixo():
                menu.navegar(1)
                pygame.time.wait(150)
            
            # Seleção com ENTER
            if self.input.enter():
                opcao = menu.opcoes[menu.opcao_selecionada]
                if opcao == "JOGAR":
                    self.estado = "JOGO"
                    print("Iniciando jogo...")
                elif opcao == "INSTRUCOES":
                    self.estado = "INSTRUCOES"
                elif opcao == "SAIR":
                    return False
            
            # ===== NAVEGAÇÃO POR MOUSE =====
            if self.input.mouse_clicou_esquerdo():
                mx, my = self.input.mouse_pos()
                opcao = menu.processar_clique(mx, my)
                if opcao == "JOGAR":
                    self.estado = "JOGO"
                elif opcao == "INSTRUCOES":
                    self.estado = "INSTRUCOES"
                elif opcao == "SAIR":
                    return False
        
        # ===== TELA DE INSTRUÇÕES =====
        elif self.estado == "INSTRUCOES":
            menu.desenhar_instrucoes()
            
            # Pressione ESPAÇO para voltar ao menu
            if self.input.espaco():
                self.estado = "MENU"
        
        return True
    
    def get_estado(self):
        """Retorna o estado atual (MENU, INSTRUCOES, JOGO)"""
        return self.estado
    
    def set_estado(self, estado):
        """Altera o estado atual"""
        self.estado = estado