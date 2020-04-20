import pygame
import random
from ots import itens
from pygame.locals import *

#Música:
pygame.mixer.init()
track = pygame.mixer.music.load(r'songs/ss.mp3')
#pygame.mixer.music.play()

#Tamanho da Janela:
width, height = 800, 600

gameOver = True
cair = False #Verifica se o personagem caiu
gameRolando = True
cano = []
mover = 1
speed = 4
vel_Y = 0
asas = 0
pontos = 0 #Pontos do Jogador
recordes = 0 #Recordes do Jogador

pygame.init()
win = pygame.display.set_mode((width, height))
passaro0 = pygame.image.load('img/flp00.png')
passaro1 = pygame.image.load('img/flp11.png')
piso = pygame.image.load('img/piso.png')
tubo = pygame.image.load('img/tubo.png')
cena = pygame.image.load('img/fundo.png')
sol = pygame.image.load('img/fundo0.png')
queenimage = pygame.image.load('img/queen.png')

#OBJETOS:
flapyBird = itens.itens(win, 200, height/3, 50, 50, passaro0, 10)
fundo0 = itens.itens(win, 0, 210, 0, 0, cena, 0)
fundo1 = itens.itens(win, width, 210, 0, 0, cena, 0)
fundo2 = itens.itens(win, 0, 0, 0, 0, sol, 0) #Sol
piso0 = itens.itens(win, 0, 466, 0, 0, piso, 0)
piso1 = itens.itens(win, width, 466, 0, 0, piso, 0)
queen = itens.itens(win, 100, 520, 200, 79, queenimage, 0)

#Matriz para adicionaros os canos:
for x in range(2):
    cano.append([0]*4)

for x in range(4):
    cano[0][x] = itens.itens(win, x*210, -100, 87, 310, tubo, 0)
    cano[1][x] = itens.itens(win, x*210, 400, 87, 310, tubo, 0)

def restart():
    global vel_Y, speed, cair, pontos
    pygame.mixer.music.play()
    for x in range(4):
        cano[0][x].x = width + x *220
        cano[1][x].x = width + x *220

        #Mostrar os canos de cima e de baixo ao mesmo tempo:
        visivel = random.randint(0, 1)
        cano[0][x].visivel = visivel
        cano[1][x].visivel = visivel

        #Aqui definimos o tamanho dos canos:
        canoy = random.randint(0, 9) * -(cano[0][0].h/10)
        cano[0][x].y = canoy
        cano[1][x].y = canoy + 470
        cano[1][x].r = 180

    flapyBird.y = height/3
    vel_Y = 0
    cair = False
    pontos = 0

def colidir(a, b):
    return a.x + a.w > b.x and a.x < b.x + b.w and a.y + a.h > b.y and a.y < b.y + b.h


def paint():
    #Manipular os gráficos:
    global asas, mover
    pygame.display.update()
    pygame.time.delay(10)
    fundo2.show()

    #Movendo o cenário:
    if fundo0.x < -width:
        fundo0.x = 0
        fundo1.x = width
    
    fundo0.x -= mover*1
    fundo1.x -= mover*1
    fundo0.show()
    fundo1.show()

    #Canos:
    for x in range(4):
        cano[0][x].show()
        cano[1][x].show()
        cano[0][x].x -= mover*speed
        cano[1][x].x -= mover*speed
        if cano[0][x].x < -cano[0][0].w:
            visivel = random.randint(0,1)
            cano[0][x].visivel = visivel
            cano[1][x].visivel = visivel
            canoy = random.randint(0, 9) * -(cano[0][0].h/10)
            cano[0][x].y = canoy
            cano[1][x].y = canoy + 470
            cano[0][x].x = width
            cano[1][x].x = width
    if piso0.x < -width:
        piso0.x = 0
        piso1.x = width
    
    piso0.x -= mover*5
    piso1.x -= mover*5
    piso0.show()
    piso1.show()

    flapyBird.show() #Passaro
    queen.show()
    asas+=1

    if asas>10:
        flapyBird.img = passaro0
    else:
        flapyBird.img = passaro1

    if asas>20:
        asas = 0
    

def control():
    #Manipular os controles:
    
    global vel_Y, gameOver, mover, cair
    mover = not gameOver

    vel_Y += mover
    flapyBird.y += mover*vel_Y #Dessa forma ele sempre ficará caindo!
    flapyBird.r = mover* (-vel_Y) *3 #Dessa forma dá a impressão que ele está caindo de bico.
    for evento in pygame.event.get():
        #Caso o personagem aperte no "X" para fechar ou "Esc" no teclado, retornará falso, ou seja o programa fecha!
        if (evento.type == pygame.QUIT) or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
            return False
        #Caso o jogador aperte espaço, o jogo irá funcionar normalmente.
        if evento.type == KEYDOWN and evento.key == K_SPACE and gameOver:
            gameOver = False
            restart()
        #O personagem vai pular:
        if evento.type == pygame.MOUSEBUTTONDOWN and not cair:
            vel_Y = mover * -12
    return True

def jogo():
    global gameOver, asas, cair, pontos
    #Verifica se perdeu:
    for x in range(2):
        for w in range(4):
            if not x and 200 < cano[x][w].x < 205 and cano[x][w].visivel and not gameOver:
                pontos += 1
                if flapyBird.y < cano[x][w].y:
                    cair = True
            elif colidir(cano[x][w], flapyBird) and cano[x][w].visivel:
                cair = True         

    if flapyBird.y > piso0.y - flapyBird.h:
        gameOver = True
        flapyBird.r = -90
        asas = 0
        cair = True
        
def textos():
    global pontos, recordes, track, texto, font
    
    #Igualar os recordes:
    if pontos > recordes:
        recordes = pontos
    
    if gameOver and cair:
        font = pygame.font.SysFont('arial', 20, 1)
        pygame.draw.rect(win, 0xd62502, [300, 100, 190, 200], 10) #Cor de fora
        pygame.draw.rect(win, 0xff733f, [305, 104, 180, 190]) #Cor de dentro
        texto = font.render("Pontos: ", 0, (214, 38, 2))
        win.blit(texto, (310, 110))

        texto = font.render(str(pontos), 0, (214, 38, 2))
        win.blit(texto, (380, 146))

        texto = font.render("Maiores Pontos: ", 0, (214, 38, 2))
        win.blit(texto, (310, 184))

        texto = font.render(str(recordes), 0, (214, 38, 2))
        win.blit(texto, (380, 220))

        texto = font.render("Clique em ESPAÇO para começar!", 0, (214, 38, 2))
        win.blit(texto, (350, 530))
    else:
        font = pygame.font.SysFont('arial black', 30)
        txt = font.render(str(pontos)+"", 0, (214, 38, 2), 0x11d1E0)
        win.blit(txt, (380, 146))

restart()
while gameRolando:
    jogo()
    textos()
    paint()
    gameRolando = control()
pygame.quit()

