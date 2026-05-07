"""
Classe Pixel - Motor gráfico base para computação gráfica 2D.
Atende a TODOS os requisitos do trabalho:
- Set Pixel
- Primitivas de Rasterização (Linha, Círculo, Elipse)
- Preenchimento de Regiões (Flood Fill e Scanline)
- Transformações Geométricas (viewport, gradiente)
- Mapeamento de Textura
- Clipping (via viewport)
"""

import pygame
import sys
import math

class Pixel:
    """
    Motor gráfico que implementa todas as primitivas de desenho usando apenas set_pixel.
    """
    
    def __init__(self, largura=800, altura=600):
        """Inicializa a janela gráfica com as dimensões especificadas."""
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Computação Gráfica")
    
    # ========== OPERAÇÕES BÁSICAS ==========
    
    def set_pixel(self, x, y, cor):
        """Requisito a) Set Pixel - desenha um único pixel na tela."""
        if 0 <= x < self.largura and 0 <= y < self.altura:
            self.tela.set_at((x, y), cor)
    
    def limpar(self, cor):
        """Preenche a tela inteira com uma cor (usando fill otimizado)."""
        self.tela.fill(cor)
    
    def atualizar(self):
        """Atualiza a tela (double buffering)."""
        pygame.display.flip()
    
    def verificar_fechar(self):
        """Verifica se o usuário fechou a janela."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.fechar()
                return True
        return False
    
    def fechar(self):
        """Fecha a janela e encerra o Pygame."""
        pygame.quit()
        sys.exit()
    
    # ========== PRIMITIVAS DE RASTERIZAÇÃO ==========
    
    def linha(self, x1, y1, x2, y2, cor):
        """
        Requisito b) Rasterização de Linha.
        Algoritmo de Bresenham para desenho de linhas.
        """
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        erro = dx - dy
        
        x, y = x1, y1
        
        while True:
            self.set_pixel(x, y, cor)
            if x == x2 and y == y2:
                break
            e2 = 2 * erro
            if e2 > -dy:
                erro -= dy
                x += sx
            if e2 < dx:
                erro += dx
                y += sy
    
    def circulo(self, cx, cy, raio, cor):
        """
        Requisito b) Rasterização de Círculo.
        Algoritmo de Bresenham para desenho de circunferência (apenas borda).
        """
        x = 0
        y = raio
        d = 1 - raio
        
        while x <= y:
            # 8 pontos simétricos
            self.set_pixel(cx + x, cy + y, cor)
            self.set_pixel(cx - x, cy + y, cor)
            self.set_pixel(cx + x, cy - y, cor)
            self.set_pixel(cx - x, cy - y, cor)
            self.set_pixel(cx + y, cy + x, cor)
            self.set_pixel(cx - y, cy + x, cor)
            self.set_pixel(cx + y, cy - x, cor)
            self.set_pixel(cx - y, cy - x, cor)
            
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
    
    def elipse(self, cx, cy, rx, ry, cor):
        """
        Requisito b) Rasterização de Elipse.
        Algoritmo de Bresenham para desenho de elipse (apenas borda).
        """
        if rx <= 0 or ry <= 0:
            return
        
        x = 0
        y = ry
        
        rx2 = rx * rx
        ry2 = ry * ry
        tworx2 = 2 * rx2
        twory2 = 2 * ry2
        
        p = int(ry2 - (rx2 * ry) + (0.25 * rx2))
        
        # Região 1
        while twory2 * x <= tworx2 * y:
            self.set_pixel(cx + x, cy + y, cor)
            self.set_pixel(cx - x, cy + y, cor)
            self.set_pixel(cx + x, cy - y, cor)
            self.set_pixel(cx - x, cy - y, cor)
            
            x += 1
            if p < 0:
                p += ry2 + twory2 * (x - 1)
            else:
                y -= 1
                p += ry2 + twory2 * (x - 1) - tworx2 * y
        
        # Região 2
        p = int(ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2)
        while y >= 0:
            self.set_pixel(cx + x, cy + y, cor)
            self.set_pixel(cx - x, cy + y, cor)
            self.set_pixel(cx + x, cy - y, cor)
            self.set_pixel(cx - x, cy - y, cor)
            
            y -= 1
            if p > 0:
                p += -tworx2 * y + rx2
            else:
                x += 1
                p += twory2 * x - tworx2 * y + rx2
    
    # ========== PREENCHIMENTO DE REGIÕES ==========
    
    def poligono(self, vertices, cor):
        """Desenha apenas a borda do polígono (usa linha para cada aresta)."""
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            self.linha(x1, y1, x2, y2, cor)
    
    def flood_fill(self, x, y, cor_nova, cor_fundo):
        """
        Requisito c) Flood Fill.
        Preenchimento por inundação usando pilha manual (iterativo).
        Substitui cor_fundo por cor_nova a partir da posição (x,y).
        """
        pilha = [(x, y)]
        fundo_tuple = cor_fundo
        nova_tuple = cor_nova
        
        if fundo_tuple == nova_tuple:
            return
        
        while pilha:
            x_atual, y_atual = pilha.pop()
            
            if x_atual < 0 or x_atual >= self.largura or y_atual < 0 or y_atual >= self.altura:
                continue
            
            cor_atual = self.tela.get_at((x_atual, y_atual))
            cor_atual_tuple = (cor_atual[0], cor_atual[1], cor_atual[2])
            
            if cor_atual_tuple == fundo_tuple:
                self.set_pixel(x_atual, y_atual, cor_nova)
                pilha.append((x_atual + 1, y_atual))
                pilha.append((x_atual - 1, y_atual))
                pilha.append((x_atual, y_atual + 1))
                pilha.append((x_atual, y_atual - 1))
    
    def scanline_fill(self, vertices, cor):
        """
        Requisito c) Scanline Fill.
        Preenchimento de polígono usando algoritmo de varredura.
        """
        if len(vertices) < 3:
            return
        
        y_min = min(v[1] for v in vertices)
        y_max = max(v[1] for v in vertices)
        
        for y in range(y_min, y_max + 1):
            interseccoes = []
            
            for i in range(len(vertices)):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % len(vertices)]
                
                if (y1 <= y < y2) or (y2 <= y < y1):
                    if y2 != y1:
                        x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                        interseccoes.append(x)
            
            interseccoes.sort()
            
            for i in range(0, len(interseccoes), 2):
                if i + 1 < len(interseccoes):
                    x_inicio = int(interseccoes[i])
                    x_fim = int(interseccoes[i + 1])
                    for x in range(x_inicio, x_fim + 1):
                        self.set_pixel(x, y, cor)
    
    # ========== MAPEAMENTO DE TEXTURA ==========
    
    def texturizar_poligono(self, vertices, uvs, textura):
        """
        Requisito h) Mapeamento de Textura.
        Aplica uma imagem (textura) a um polígono usando scanline mapping.
        """
        n = len(vertices)
        tex_w = textura.get_width()
        tex_h = textura.get_height()
        
        if tex_w == 0 or tex_h == 0:
            return
        
        ys = [p[1] for p in vertices]
        y_min = int(min(ys))
        y_max = int(max(ys))
        
        for y in range(y_min, y_max):
            inters = []
            
            for i in range(n):
                x0, y0 = vertices[i]
                x1, y1 = vertices[(i + 1) % n]
                u0, v0 = uvs[i]
                u1, v1 = uvs[(i + 1) % n]
                
                if y0 == y1:
                    continue
                
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                    u0, v0, u1, v1 = u1, v1, u0, v0
                
                if y < y0 or y >= y1:
                    continue
                
                t = (y - y0) / (y1 - y0)
                x = x0 + t * (x1 - x0)
                u = u0 + t * (u1 - u0)
                v = v0 + t * (v1 - v0)
                
                inters.append((x, u, v))
            
            inters.sort(key=lambda i: i[0])
            
            for i in range(0, len(inters) - 1, 2):
                x_start, u_start, v_start = inters[i]
                x_end, u_end, v_end = inters[i + 1]
                
                if x_start >= x_end:
                    continue
                
                for x in range(int(x_start), int(x_end) + 1):
                    t = (x - x_start) / (x_end - x_start)
                    u = u_start + t * (u_end - u_start)
                    v = v_start + t * (v_end - v_start)
                    
                    tx = int(u * (tex_w - 1))
                    ty = int(v * (tex_h - 1))
                    
                    if 0 <= tx < tex_w and 0 <= ty < tex_h:
                        cor_raw = textura.get_at((tx, ty))
                        self.set_pixel(x, y, (cor_raw[0], cor_raw[1], cor_raw[2]))
    
    # ========== TRANSFORMAÇÕES GEOMÉTRICAS ==========
    
    def viewport(self, ponto, janela, viewport):
        """
        Requisito f) Janela e Viewport.
        Transforma coordenada do mundo para coordenada da tela.
        Suporta zoom (escala) via redimensionamento da janela.
        """
        wx, wy = ponto
        wxmin, wymin, wxmax, wymax = janela
        vxmin, vymin, vxmax, vymax = viewport
        
        sx = (vxmax - vxmin) / (wxmax - wxmin)
        sy = (vymin - vymax) / (wymax - wymin)  # Inverte Y (Pygame)
        
        vx = vxmin + (wx - wxmin) * sx
        vy = vymax + (wy - wymin) * sy
        
        return (int(vx), int(vy))
    
    def poligono_gradiente(self, vertices, cores_vertices):
        """
        Requisito: Gradiente de cores por vértice.
        Preenche polígono interpolando cores entre os vértices.
        """
        n = len(vertices)
        y_min = int(min(v[1] for v in vertices))
        y_max = int(max(v[1] for v in vertices))
        
        for y in range(y_min, y_max + 1):
            inters = []
            
            for i in range(n):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % n]
                c1 = cores_vertices[i]
                c2 = cores_vertices[(i + 1) % n]
                
                if y1 == y2:
                    continue
                
                if y1 > y2:
                    x1, y1, x2, y2 = x2, y2, x1, y1
                    c1, c2 = c2, c1
                
                if y < y1 or y >= y2:
                    continue
                
                t = (y - y1) / (y2 - y1)
                x = x1 + t * (x2 - x1)
                r = int(c1[0] + (c2[0] - c1[0]) * t)
                gv = int(c1[1] + (c2[1] - c1[1]) * t)
                b = int(c1[2] + (c2[2] - c1[2]) * t)
                inters.append((x, r, gv, b))
            
            inters.sort(key=lambda i: i[0])
            
            for i in range(0, len(inters), 2):
                if i + 1 >= len(inters):
                    continue
                
                x1, r1, g1, b1 = inters[i]
                x2, r2, g2, b2 = inters[i + 1]
                
                for x in range(int(x1), int(x2) + 1):
                    if x2 != x1:
                        t = (x - x1) / (x2 - x1)
                        r = int(r1 + (r2 - r1) * t)
                        gv = int(g1 + (g2 - g1) * t)
                        b = int(b1 + (b2 - b1) * t)
                    else:
                        r, gv, b = r1, g1, b1
                    self.set_pixel(x, y, (r, gv, b))
    
    # ========== FIGURAS PREENCHIDAS (OTIMIZADAS) ==========
    
    def circulo_preenchido(self, cx, cy, raio, cor):
        """
        Desenha círculo totalmente preenchido usando Bresenham + linhas horizontais.
        """
        x = 0
        y = raio
        d = 1 - raio
        limites = {}
        
        while x <= y:
            for yy in (cy + y, cy - y, cy + x, cy - x):
                if yy not in limites:
                    limites[yy] = [cx, cx]
                limites[yy][0] = min(limites[yy][0], cx - x if yy in (cy + y, cy - y) else cx - y)
                limites[yy][1] = max(limites[yy][1], cx + x if yy in (cy + y, cy - y) else cx + y)
            
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
        
        for y_linha, (x1, x2) in limites.items():
            if 0 <= y_linha < self.altura:
                for xs in range(max(0, x1), min(self.largura, x2 + 1)):
                    self.set_pixel(xs, y_linha, cor)
    
    def elipse_preenchida(self, cx, cy, rx, ry, cor):
        """Desenha elipse totalmente preenchida usando Bresenham + linhas horizontais."""
        if rx <= 0 or ry <= 0:
            return
        
        x = 0
        y = ry
        limites = {}
        
        rx2 = rx * rx
        ry2 = ry * ry
        tworx2 = 2 * rx2
        twory2 = 2 * ry2
        
        # Região 1
        p = int(ry2 - (rx2 * ry) + (0.25 * rx2))
        while twory2 * x <= tworx2 * y:
            for yy in (cy + y, cy - y):
                if yy not in limites:
                    limites[yy] = [cx, cx]
                limites[yy][0] = min(limites[yy][0], cx - x)
                limites[yy][1] = max(limites[yy][1], cx + x)
            
            for yy in (cy + x, cy - x):
                if yy not in limites:
                    limites[yy] = [cx, cx]
                limites[yy][0] = min(limites[yy][0], cx - y)
                limites[yy][1] = max(limites[yy][1], cx + y)
            
            x += 1
            if p < 0:
                p += ry2 + twory2 * (x - 1)
            else:
                y -= 1
                p += ry2 + twory2 * (x - 1) - tworx2 * y
        
        # Região 2
        p = int(ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2)
        while y >= 0:
            for yy in (cy + y, cy - y):
                if yy not in limites:
                    limites[yy] = [cx, cx]
                limites[yy][0] = min(limites[yy][0], cx - x)
                limites[yy][1] = max(limites[yy][1], cx + x)
            
            y -= 1
            if p > 0:
                p += -tworx2 * y + rx2
            else:
                x += 1
                p += twory2 * x - tworx2 * y + rx2
        
        # Preenche
        for y_linha, (x1, x2) in limites.items():
            if 0 <= y_linha < self.altura:
                for xs in range(max(0, x1), min(self.largura, x2 + 1)):
                    self.set_pixel(xs, y_linha, cor)
    
    def gradiente_pista(self, x1, x2, y1, y2, cor_esq, cor_dir, curva=1):
        """
        Desenha gradiente horizontal em uma região retangular.
        Útil para efeitos de iluminação na pista.
        """
        largura = x2 - x1
        
        for y in range(y1, y2):
            for x in range(x1, x2):
                t = (x - x1) / largura
                t_curvo = t ** curva
                r = int(cor_esq[0] + (cor_dir[0] - cor_esq[0]) * t_curvo)
                gv = int(cor_esq[1] + (cor_dir[1] - cor_esq[1]) * t_curvo)
                b = int(cor_esq[2] + (cor_dir[2] - cor_esq[2]) * t_curvo)
                self.set_pixel(x, y, (r, gv, b))
    
    def blit_simulado(self, origem, destino_x, destino_y, rect=None):
        """
        Simula blit usando apenas set_pixel.
        
        Parâmetros:
            origem: superfície de origem 
            destino_x, destino_y: posição onde desenhar
            rect: (x, y, largura, altura) da área a copiar (opcional)
        """
        if rect:
            x_origem, y_origem, largura, altura = rect
        else:
            x_origem, y_origem = 0, 0
            largura = origem.get_width()
            altura = origem.get_height()
        
        for y in range(altura):
            for x in range(largura):
                # Pega a cor da origem
                cor = origem.get_at((x_origem + x, y_origem + y))
                # Desenha no destino
                self.set_pixel(destino_x + x, destino_y + y, cor)
    
    def desenhar_janela_viewport(self, bola_x, bola_y, zoom_largura=180, zoom_altura=130, tamanho_zoom=80):
        """
    Desenha uma janela (viewport) ampliada de uma área ao redor de um ponto.
    
    REQUISITO: Janela e Viewport (transformação de coordenadas + zoom)
    
    Parâmetros:
        bola_x, bola_y: centro da área a ser ampliada (janela do mundo)
        zoom_largura, zoom_altura: tamanho da viewport na tela (em pixels)
        tamanho_zoom: tamanho da janela do mundo (quanto menor, maior o zoom)
    
    Funcionamento:
        1. Define uma janela do mundo ao redor da bola (tamanho_zoom x tamanho_zoom)
        2. Define uma viewport na tela (canto inferior direito)
        3. Para cada pixel da viewport, mapeia de volta para a janela do mundo
        4. Copia o pixel para a viewport
        5. Desenha uma borda branca ao redor
    """
        # Calcula posição da viewport (canto inferior direito)
        viewport_x = self.largura - zoom_largura - 10
        viewport_y = self.altura - zoom_altura - 10
        
        # Janela do mundo (área ampliada)
        janela_mundo = (bola_x - tamanho_zoom, bola_y - tamanho_zoom,
                        bola_x + tamanho_zoom, bola_y + tamanho_zoom)
        
        # Copia os pixels da janela do mundo para a viewport
        for y in range(zoom_altura):
            for x in range(zoom_largura):
                # Mapeia pixel da viewport para o mundo
                u = janela_mundo[0] + x * (tamanho_zoom * 2) / zoom_largura
                v = janela_mundo[1] + y * (tamanho_zoom * 2) / zoom_altura
                
                if 0 <= u < self.largura and 0 <= v < self.altura:
                    cor = self.tela.get_at((int(u), int(v)))
                    self.set_pixel(viewport_x + x, viewport_y + y, cor)
        
        # Borda da viewport
        self.poligono([(viewport_x, viewport_y),
                    (viewport_x + zoom_largura, viewport_y),
                    (viewport_x + zoom_largura, viewport_y + zoom_altura),
                    (viewport_x, viewport_y + zoom_altura)], (255, 255, 255))