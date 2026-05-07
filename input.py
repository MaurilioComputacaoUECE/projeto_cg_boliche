import pygame

class Input:
    """Gerencia entrada do mouse e teclado de forma unificada"""
    
    def __init__(self):
        # Mouse
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_esquerdo = False
        self.mouse_direito = False
        self.mouse_meio = False
        self.mouse_esquerdo_click = False
        self.mouse_direito_click = False
        self.mouse_meio_click = False
        
        # Teclado
        self.teclas_pressionadas = set()
        self.teclas_click = set()
    
    def atualizar(self):
        """Atualiza estado dos inputs. Chamar uma vez por frame."""
        self.mouse_esquerdo_click = False
        self.mouse_direito_click = False
        self.mouse_meio_click = False
        self.teclas_click.clear()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.mouse_esquerdo_click = True
                elif evento.button == 2:
                    self.mouse_meio_click = True
                elif evento.button == 3:
                    self.mouse_direito_click = True
            
            if evento.type == pygame.KEYDOWN:
                self.teclas_pressionadas.add(evento.key)
                self.teclas_click.add(evento.key)
            if evento.type == pygame.KEYUP:
                self.teclas_pressionadas.discard(evento.key)
        
        self.mouse_esquerdo = pygame.mouse.get_pressed()[0]
        self.mouse_direito = pygame.mouse.get_pressed()[2]
        self.mouse_meio = pygame.mouse.get_pressed()[1]
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        
        return True
    
    # ========== MOUSE ==========
    
    def mouse_pos(self):
        return (self.mouse_x, self.mouse_y)
    
    def mouse_clicou_esquerdo(self):
        return self.mouse_esquerdo_click
    
    def mouse_clicou_direito(self):
        return self.mouse_direito_click
    
    def mouse_pressionado_esquerdo(self):
        return self.mouse_esquerdo
    
    def mouse_dentro_retangulo(self, x, y, w, h):
        return x <= self.mouse_x <= x + w and y <= self.mouse_y <= y + h
    
    # ========== TECLADO ==========
    
    def tecla(self, tecla):
        return tecla in self.teclas_pressionadas
    
    def esc(self):
        return pygame.K_ESCAPE in self.teclas_pressionadas
    
    def espaco(self):
        return pygame.K_SPACE in self.teclas_pressionadas
    
    def enter(self):
        return pygame.K_RETURN in self.teclas_pressionadas
    
    def seta_cima(self):
        return pygame.K_UP in self.teclas_pressionadas
    
    def seta_baixo(self):
        return pygame.K_DOWN in self.teclas_pressionadas
    
    def seta_esquerda(self):
        return pygame.K_LEFT in self.teclas_pressionadas
    
    def seta_direita(self):
        return pygame.K_RIGHT in self.teclas_pressionadas