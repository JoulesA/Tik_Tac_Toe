################ MODULOS
import pygame
import sys
import numpy as np
import random

from pygame import mixer
#import pygame.gfxdraw

###############  PYGAME VARIABLES
pygame.init()

WIDITH = 600
HEIGTH = 600
LINE_WIDTH = 15

COLOR_01 = (38, 70, 83)
COLOR_02 = (42, 157, 143)
COLOR_03 = (233, 196, 106)
COLOR_04 = (244, 162, 97)
COLOR_05 = (231, 111, 81)

LINE_COLOR = COLOR_04
LINE2_COLOR = COLOR_02

# Configuracion de letras
font = pygame.font.SysFont('montserrat', 20, bold=True)
Title_Font = pygame.font.SysFont('montserrat', 150, bold=True)
Subtitle_Font = pygame.font.SysFont('montserrat', 50, bold=True)
Sub_Font = pygame.font.SysFont('montserrat', 100, bold=True)

# Parametros de la ventana 
screen = pygame.display.set_mode((WIDITH,HEIGTH))
pygame.display.set_caption('# TIC TAC TOE #')

# Musica de fondo 
#mixer.music.load('my-patch.mp3')
mixer.music.load('BG_Music.wav')
mixer.music.play(-1) # Para que la cancion de arriba se reproduzca en loop 

#################### FUNCIONES PARA ENTORNO
class btn():
    def __init__(self, txt, x , y, bg_color = COLOR_04, txt_color = (250,250,250)):
        self.txt = txt
        self.x = x
        self.y = y
        self.bg_color = bg_color
        self.txt_color = txt_color
        self.figure = None

    def drawBtn(self, ventana, bg_color = COLOR_04): # Ventana hace referencia a la variable donde esta el contenedor de la ventana
        self.figure = pygame.Rect(self.x,self.y,150,150) # Posicion, ancho, alto
        #fontType = pygame.font.SysFont("Calibri",30)

        pygame.draw.rect(ventana, bg_color, self.figure, 0, 5)
        #texto = font.render(self.txt, True, self.txt_color)
        #ventana.blit(texto,(figure.x+(figure.width-texto.get_width))/2,(figure.y+(figure.height-texto.get_height))/2)
    
    def clickBtn(self,validation, ventana,pos):
        global position, bestCasilla
        if self.figure.collidepoint(pygame.mouse.get_pos()):
            #pygame.draw.rect(ventana, (0, 255, 0), self.figure)
            if validation:
                position[pos] = 2
                if not winCase():
                    cat()

def hashtagDraw():
    # Linea horizontal
    pygame.draw.line(screen, LINE2_COLOR, (20,200), (580,200), LINE_WIDTH)
    pygame.draw.circle( screen, LINE2_COLOR, (20,200), LINE_WIDTH/2 )
    pygame.draw.circle( screen, LINE2_COLOR, (580,200), LINE_WIDTH/2 )

    # Linea horizontal
    pygame.draw.line(screen, LINE2_COLOR, (20,400), (580,400), LINE_WIDTH)
    pygame.draw.circle( screen, LINE2_COLOR, (20,400), LINE_WIDTH/2 )
    pygame.draw.circle( screen, LINE2_COLOR, (580,400), LINE_WIDTH/2 )

    # Linea vertical
    pygame.draw.line(screen, LINE2_COLOR, (200,20), (200,580), LINE_WIDTH)
    pygame.draw.circle( screen, LINE2_COLOR, (200,20), LINE_WIDTH/2 )
    pygame.draw.circle( screen, LINE2_COLOR, (200,580), LINE_WIDTH/2 )

    # Linea vertical
    pygame.draw.line(screen, LINE2_COLOR, (400,20), (400,580), LINE_WIDTH)
    pygame.draw.circle( screen, LINE2_COLOR, (400,20), LINE_WIDTH/2 )
    pygame.draw.circle( screen, LINE2_COLOR, (400,580), LINE_WIDTH/2 )

def title_txt(x,y):
    txt= Title_Font.render('TIC', True, COLOR_03)
    screen.blit(txt, [x,y])

    txt= Title_Font.render('TAC', True, COLOR_02)
    screen.blit(txt, [x+53,y+50])

    txt= Title_Font.render('TOE', True, COLOR_04)
    screen.blit(txt, [x+106,y+100])

xp = 0
yp = 0
def animation_title(x,y):
    global xp, yp
    #xp = 0
    #yp = 0
    x_vel = 0.75
    y_vel = 0.5
    if xp <= x:
        xp += x_vel
    if yp <= y:
        yp += y_vel
    
    title_txt(xp,yp)

############################ FUNCIONES VENTANA 
# Game
def gameLoop(): 
    global position, bestCasilla

    running = True
    while running:

        ############# Graficos
        # Tablero
        screen.fill(COLOR_03)
        hashtagDraw()

        # Botones casilla 
        BOTONES = []
        for i in range (3):
            for j in range (3):
                BOTONES.append(btn("Text", 25+200*(i) , 25+200*(j)))
        
        for i in range(len(BOTONES)):
            BOTONES[i].drawBtn(screen,COLOR_04)

        # Revision de casillas: pinta las casillas deacuerdo al vector de posicion tirado
        for i, val in enumerate(position):
            if position[i] == 1:
                pygame.draw.rect(screen, COLOR_05, BOTONES[i].figure,0,5)
                txt = Title_Font.render('O', True, COLOR_03)
                screen.blit(txt,[BOTONES[i].figure.x+(BOTONES[i].figure.width - txt.get_width())/2,BOTONES[i].figure.y+(BOTONES[i].figure.height - txt.get_height())/2])
        
            elif position[i] == 2:
                pygame.draw.rect(screen, COLOR_01, BOTONES[i].figure,0,5)
                txt = Title_Font.render('X', True, COLOR_03)
                screen.blit(txt,[BOTONES[i].figure.x+(BOTONES[i].figure.width - txt.get_width())/2,BOTONES[i].figure.y+(BOTONES[i].figure.height - txt.get_height())/2])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
            click = False            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            for i in range(9):
                BOTONES[i].clickBtn(click,screen,i)

        winLines()
        pygame.display.update()


# Init Window
def initWin(pauseButton = False):
    global position, bestCasilla, win
    while True:
        click = False
        screen.fill(COLOR_01)
        #title_txt(90,25)
        animation_title(90,25)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event. type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    print ('click on: '+ str(mx) +' , '+ str(my))

        if pauseButton:                                             #Continuar
            button_1 = pygame.Rect(200, 300, 200, 50)
            pygame.draw.rect(screen, COLOR_05, button_1,0,5)
            txt_btn1 = font.render('Continuar', True, COLOR_03)
            screen.blit(txt_btn1, [button_1.x+(button_1.width - txt_btn1.get_width())/2,button_1.y+(button_1.height -txt_btn1.get_height())/2])


            if button_1.collidepoint(pygame.mouse.get_pos()):       
                pygame.draw.rect(screen, COLOR_03, button_1,3,5)
                if click:
                    gameLoop()  
        
        button_2 = pygame.Rect(200, 375, 200, 50)
        button_3 = pygame.Rect(200, 525, 200, 50)
        
        pygame.draw.rect(screen, COLOR_05, button_2,0,5)
        pygame.draw.rect(screen, COLOR_05, button_3,0,5)

        button_4 = pygame.Rect(200, 450, 200, 50)               #Select Color
        pygame.draw.rect(screen, COLOR_05, button_4,0,5)
        txt_btn4 = font.render('Configuración', True, COLOR_03)
        screen.blit(txt_btn4, [button_4.x+(button_4.width - txt_btn4.get_width())/2,button_4.y+(button_4.height -txt_btn4.get_height())/2])

        # Primero recuadros, luego texto que si no no se ven xd
        txt_btn2 = font.render('Nuevo juego', True, COLOR_03)
        screen.blit(txt_btn2,[button_2.x+(button_2.width - txt_btn2.get_width())/2,button_2.y+(button_2.height - txt_btn2.get_height())/2])
        txt_btn3 = font.render('Salir', True, COLOR_03)
        screen.blit(txt_btn3, [button_3.x+(button_3.width - txt_btn3.get_width())/2,button_3.y+(button_3.height -txt_btn3.get_height())/2])

        if button_2.collidepoint((mx, my)):                     # New Game
            pygame.draw.rect(screen, COLOR_03, button_2,3,5)
            if click:
                pauseButton = True
                win = False
                position = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                bestCasilla = [5, 1, 3, 7, 9, 2, 4, 6, 8]
                if random.randint(1,2) == 1:
                    cat() 
                gameLoop()
        
        if button_3.collidepoint((mx, my)):                     # Salida 
            pygame.draw.rect(screen, COLOR_03, button_3,3,5)
            if click:
                pygame.quit()
                sys.exit()
        
        if button_4.collidepoint((mx, my)):                     # Salida 
            pygame.draw.rect(screen, COLOR_03, button_4,3,5)
            if click:
                Config()
                
        pygame.display.flip()

def Config():
    global COLOR_01, COLOR_02, COLOR_03, COLOR_04, COLOR_05, LINE2_COLOR,LINE_COLOR

    running = True
    while running:
        click = False
        screen.fill(COLOR_04)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        txt= Subtitle_Font.render('Selección', True, COLOR_02)
        screen.blit(txt, [(600-txt.get_width())/2,100])
        txt= Subtitle_Font.render('de', True, COLOR_02)
        screen.blit(txt, [(600-txt.get_width())/2,150])
        txt= Subtitle_Font.render('Color', True, COLOR_02)
        screen.blit(txt, [(600-txt.get_width())/2,200])

        btn1 = pygame.Rect(50, 400, 100, 100)
        pygame.draw.rect(screen, (2, 48, 71), btn1,0,5)
        txt= Sub_Font.render('O', True, (251, 133, 0))
        screen.blit(txt, [btn1.x+18,btn1.y-23])
        txt= Sub_Font.render('X', True, (142, 202, 230))
        screen.blit(txt, [btn1.x+2,btn1.y])
        

        btn2 = pygame.Rect(250, 400, 100, 100)
        pygame.draw.rect(screen, (233, 196, 106), btn2,0,5)#3
        txt= Sub_Font.render('O', True, (231, 111, 81))#5
        screen.blit(txt, [btn2.x+18,btn2.y-23])
        txt= Sub_Font.render('X', True, (38, 70, 83))#1
        screen.blit(txt, [btn2.x+2,btn2.y])
        

        btn3 = pygame.Rect(450, 400, 100, 100)
        pygame.draw.rect(screen, (235, 94, 40), btn3,0,5)
        txt= Sub_Font.render('O', True, (37, 36, 34))
        screen.blit(txt, [btn3.x+18,btn3.y-23])
        txt= Sub_Font.render('X', True, (255, 252, 242))
        screen.blit(txt, [btn3.x+2,btn3.y])
        

        if btn1.collidepoint(pygame.mouse.get_pos()):       
            pygame.draw.rect(screen, (33, 158, 188), btn1,3,5)
            if click:
                COLOR_01 = (142, 202, 230)
                COLOR_02 = (33, 158, 188)
                COLOR_03 = (2, 48, 71)
                COLOR_04 = (255, 183, 3)
                COLOR_05 = (251, 133, 0)
                LINE_COLOR = COLOR_04
                LINE2_COLOR = COLOR_02 
            
        if btn2.collidepoint(pygame.mouse.get_pos()):       
            pygame.draw.rect(screen, (42, 157, 143), btn2,3,5)
            if click:
                COLOR_01 = (38, 70, 83)
                COLOR_02 = (42, 157, 143)
                COLOR_03 = (233, 196, 106)
                COLOR_04 = (244, 162, 97)
                COLOR_05 = (231, 111, 81)
                LINE_COLOR = COLOR_04
                LINE2_COLOR = COLOR_02

        if btn3.collidepoint(pygame.mouse.get_pos()):       
            pygame.draw.rect(screen, (204, 197, 185), btn3,3,5)
            if click:
                COLOR_01 = (255, 252, 242)
                COLOR_02 = (204, 197, 185)
                COLOR_03 = (235, 94, 40)
                COLOR_04 = (64, 61, 57)
                COLOR_05 = (37, 36, 34)
                LINE_COLOR = COLOR_04
                LINE2_COLOR = COLOR_02
            
        btns = pygame.Rect(250, 525, 100, 50)
        pygame.draw.rect(screen, COLOR_03, btns,0,5)
        txt= font.render('Atras', True, COLOR_02)
        screen.blit(txt, [btns.x+(btns.width-txt.get_width())/2,btns.y+(btns.height-txt.get_height())/2])
        if btns.collidepoint(pygame.mouse.get_pos()):       
            pygame.draw.rect(screen, COLOR_05, btns,3,5)
            if click:
                running = False

        pygame.display.flip()

######################################### GAME
#Variables del juego 
position = [0, 0, 0, 0, 0, 0, 0, 0, 0]
turno = 1
bestCasilla = [5, 1, 3, 7, 9, 2, 4, 6, 8]
win = False
sec = [[1, 2, 3],[4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9],[1, 5, 9], [3, 5, 7]]

def winLines ():
    if win:
        for i in range(len(sec)):
                if position[sec[i][0]-1] == position[sec[i][1]-1] and position[sec[i][1]-1] == position[sec[i][2]-1]:
                    
                    if i == 3 :
                        pygame.draw.line(screen, LINE2_COLOR, (100,100), (500,100), LINE_WIDTH)
                        pygame.draw.circle( screen, LINE2_COLOR, (100,100), LINE_WIDTH/2 )
                        pygame.draw.circle( screen, LINE2_COLOR, (500,100), LINE_WIDTH/2 )

                    elif i == 4:
                        pygame.draw.line(screen, LINE2_COLOR, (100,300), (500,300), LINE_WIDTH)
                        pygame.draw.circle( screen, LINE2_COLOR, (100,300), LINE_WIDTH/2 )
                        pygame.draw.circle( screen, LINE2_COLOR, (500,300), LINE_WIDTH/2 )

                    elif i == 5:
                        pygame.draw.line(screen, LINE2_COLOR, (100,500), (500,500), LINE_WIDTH)
                        pygame.draw.circle( screen, LINE2_COLOR, (100,500), LINE_WIDTH/2 )
                        pygame.draw.circle( screen, LINE2_COLOR, (500,500), LINE_WIDTH/2 )

                    elif i == 0:
                        pygame.draw.line(screen, LINE2_COLOR, (100,100), (100,500), LINE_WIDTH)
                        pygame.draw.circle( screen, LINE2_COLOR, (100,100), LINE_WIDTH/2 )
                        pygame.draw.circle( screen, LINE2_COLOR, (100,500), LINE_WIDTH/2 )

                    elif i == 1:
                        pygame.draw.line(screen, LINE2_COLOR, (300,100), (300,500), LINE_WIDTH)
                        pygame.draw.circle( screen, LINE2_COLOR, (300,100), LINE_WIDTH/2 )
                        pygame.draw.circle( screen, LINE2_COLOR, (300,500), LINE_WIDTH/2 )

                    elif i == 2:
                        pygame.draw.line(screen, LINE2_COLOR, (500,100), (500,500), LINE_WIDTH)
                        pygame.draw.circle( screen, LINE2_COLOR, (500,100), LINE_WIDTH/2 )
                        pygame.draw.circle( screen, LINE2_COLOR, (500,500), LINE_WIDTH/2 )

                    elif i == 6:
                        pygame.draw.line(screen, LINE2_COLOR, (100,100), (500,500), LINE_WIDTH+1)
                        pygame.draw.circle( screen, LINE2_COLOR, (100,100), LINE_WIDTH/2 )
                        pygame.draw.circle( screen, LINE2_COLOR, (500,500), LINE_WIDTH/2 )

                    elif i == 7:
                        pygame.draw.line(screen, LINE2_COLOR, (500,100), (100,500), LINE_WIDTH+1)
                        pygame.draw.circle( screen, LINE2_COLOR, (500,100), LINE_WIDTH/2 )
                        pygame.draw.circle( screen, LINE2_COLOR, (100,500), LINE_WIDTH/2 )

def winCase():
    global win
    for e in range (1,3):
        for i in range(len(sec)):
            if position[sec[i][0]-1] == e and position[sec[i][1]-1] == e and position[sec[i][2]-1] == e:

                if e == 1:
                    print ('Gana gato')
                    print (i)
                    win = True
                    return True
                elif e == 2:
                    print ('Gana humano')
                    win = True
                    return True
                else:
                    print('No se ha ganado')
                    return False
                
# Gato cuchillo de palo, no gana pero como jode.
def cat():
    global position, bestCasilla
    for e in range (1,3):
        for i in range(len(sec)):
            if position[sec[i][0]-1] == e and position[sec[i][1]-1] == e and position[sec[i][2]-1] == 0:
                position[sec[i][2]-1] = 1
                winCase()
                return

            elif position[sec[i][0]-1] == e and position[sec[i][1]-1] == 0 and position[sec[i][2]-1] == e:
                position[sec[i][1]-1] = 1
                winCase()
                return

            elif position[sec[i][0]-1] == 0 and position[sec[i][1]-1] == e and position[sec[i][2]-1] == e:
                position[sec[i][0]-1] = 1
                winCase()
                return
            
            elif e==2 and i==len(sec)-1:
                for j in range(len(bestCasilla)):
                    if position[bestCasilla[j]-1] == 0:
                        position[bestCasilla[j]-1] = 1
                        winCase()
                        return

                    elif j == len(bestCasilla)-1:
                        print('Gato')
                        winCase()
                        return
   # winCase()

# RUN YEAH!
initWin()