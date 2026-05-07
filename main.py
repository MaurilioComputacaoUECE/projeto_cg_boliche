"""
Arquivo principal do jogo Boliche.
Gerencia o loop principal, alternância entre menu e jogo.
"""

import pygame
from pixel import Pixel
from input import Input
from menu import Menu
from menu_handler import MenuHandler
from jogo import Jogo

# ===== CONFIGURAÇÕES DA TELA =====
WIDTH, HEIGHT = 800, 600

# Inicializa módulos
g = Pixel(WIDTH, HEIGHT)      # Motor gráfico
input = Input()                # Input (mouse/teclado)
menu = Menu(g, WIDTH, HEIGHT) # Tela de menu
menu_handler = MenuHandler(g, input)  # Controla estado do menu
jogo = None                    # Instância do jogo (criada quando necessário)


# ===== LOOP PRINCIPAL =====
while True:
    # Atualiza input (teclado/mouse). Retorna False se janela foi fechada.
    if not input.atualizar():
        break
    
    # Atualiza menu (navegação, cliques). Retorna False se escolheu SAIR.
    if not menu_handler.atualizar(menu):
        break
    
    # ===== ESTADO: JOGO =====
    if menu_handler.get_estado() == "JOGO":
        # Cria instância do jogo na primeira vez
        if jogo is None:
            jogo = Jogo(g, input)
        
        # Processa input do jogo (lançamento da bola)
        jogo.processar_input()
        
        # Atualiza física e colisões
        jogo.atualizar()
        
        # Limpa tela e desenha o jogo
        g.limpar((20, 30, 60))
        jogo.desenhar()
        g.atualizar()
        
        # Verifica se o jogo terminou (todos os rounds completados)
        if jogo.finalizado():
            print(f"Jogo finalizado! Pontos: {jogo.get_pontos()}")
            
            # Aguarda o jogador pressionar ESC para voltar ao menu
            while True:
                if not input.atualizar():
                    break
                if input.esc():
                    break
                pygame.time.delay(16)
            
            # Volta para o menu e reseta o jogo
            menu_handler.set_estado("MENU")
            jogo = None
        
        # Pressionou ESC durante o jogo? Volta ao menu
        if input.esc():
            menu_handler.set_estado("MENU")
            jogo = None
    
    # Pequeno delay para não sobrecarregar a CPU
    pygame.time.delay(16)

# Fecha a janela ao sair
g.fechar()