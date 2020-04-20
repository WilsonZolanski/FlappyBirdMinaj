import pygame

"""
Variavéis padrões:
x x y = Altura x Largura.
w x h = Altura x Largura
"""
class itens:
    def __init__(self, win, x, y, w, h, img, r):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r #Rotação
        self.visivel = True 
        self.img = img #Imagem
        self.win = win #Janela
    
    def show(self):
        #Função para mostrar os objetos: 
        imagem = pygame.transform.rotate(self.img, self.r)
        if self.visivel:
            #Se estiver visivel, mostra a imagem na posição X x Y!
            self.win.blit(imagem, (self.x, self.y))
