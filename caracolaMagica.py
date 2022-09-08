# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 00:39:52 2019

@author: YorchXD
"""

import random 
import pygame
import time
#from playsound import playsound

#Clase que ayuda a realizar el intercambio de pantallas con atenuacion. Esta clase fue modificada y se obtuvo desde 
#la siguiente pagina web:
#https://github.com/JarvistheJellyFish/AICivGame/blob/master/crossfade.py
class CrossFade(pygame.sprite.Sprite):

    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        w, h = surface.get_size()
        self.image = pygame.Surface((w, h))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.fade_dir = 1

        #255 es opaca, 0 es transparente
        self.trans_value = 255
        self.fade_speed = 5
        self.delay = 1

        #el incremento aumenta con cada marco (cada llamada para actualizar)
        self.increment = 0
        self.image.set_alpha(self.trans_value)

        self.rect.centerx = w / 2
        self.rect.centery = h / 2

    def update(self):
        self.image.set_alpha(self.trans_value)

        self.increment += 1

        if self.increment >= self.delay:
            self.increment = 0

            if self.fade_dir > 0:
                #Verifica que el valor no sea negativo
                if self.trans_value - self.fade_speed < 0:
                    self.trans_value = 0
                else:
                    self.trans_value -= self.fade_speed

            elif self.fade_dir < 0:
                if self.trans_value + self.fade_speed > 255:
                    self.trans_value = 255

                else:
                    self.trans_value += self.fade_speed


def BienvenidaSalida(screen, imagen, sonido, titulo, texto1,texto2, anchoPantalla):
    pygame.display.set_caption(titulo)

    clock = pygame.time.Clock()
    keepPlaying = True

    logo = pygame.image.load(imagen)
    screen.blit(logo, (0, 0))
    
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 72)
    textsurface = myfont.render(texto1, False, (247,248,245))
    screen.blit(textsurface,((anchoPantalla/2) - textsurface.get_width() // 2, 50))
    textsurface2 = myfont.render(texto2, False, (247,248,245))
    screen.blit(textsurface2,((anchoPantalla/2) - textsurface2.get_width() // 2, 150))
    
    fade = CrossFade(screen)
    all_Sprites = pygame.sprite.Group(fade)
    now = time.time()
    future = now + 12
    play(sonido, None)
    # pygame.mixer.init()
    # pygame.mixer.music.load(sonido)
    # pygame.mixer.music.play()
    pygame.display.flip()
    while keepPlaying:
        clock.tick(60)
        if time.time() > future:
            break

        if fade.trans_value == 0:
            pygame.time.delay(2800)
            fade.fade_dir *= -1

        all_Sprites.clear(screen, logo)
#        all_Sprites.clear(screen, textsurface)
#        all_Sprites.clear(screen, textsurface2)
        screen.blit(textsurface,((anchoPantalla/2) - textsurface.get_width() // 2,50))
        screen.blit(textsurface2,((anchoPantalla/2) - textsurface2.get_width() // 2, 150))
        all_Sprites.update()
        all_Sprites.draw(screen)
        pygame.display.flip()
    return screen

def play(audio, tiempoEspera):
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    if(tiempoEspera!=None):
        time.sleep(tiempoEspera)


def ConsultaCaracola(pantalla, anchoPantalla):
    # inicializa Pygame
    pygame.init()

    # establece el título de la ventana
    pygame.display.set_caption(u'Consulta a la caracola mágica')

    # establece el tamaño de la ventana
    #pantalla = pygame.display.set_mode((1280, 800))

    #Aqui es donde colocamos el fondo a la pantalla
    fondo =pygame.image.load("fondo.png")
    pantalla.blit(fondo, (0, 0)) 
    
    #se lee la imagen del anillo
    anillo = pygame.image.load("anillo.png")

    #posiciona el anillo en la pantalla
    x=649
    y=318
    pantalla.blit(anillo, (x, y)) 
    
    x2,y2=anillo.get_rect().size
    pygame.display.flip()
    
    reloj = pygame.time.Clock()
    
    #validacion de tomar anillo
    toma_anillo=0
    
    #Inicializacion de variable para mover el anillo de la caracola
    x1=649
    y1=318
    
    xtexto=(anchoPantalla/2)
    ytexto=50
    colorCuerda = (247,248,245)
    
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 72)

    # bucle infinito
    while True:
        
        # obtiene un solo evento de la cola de eventos
        event = pygame.event.wait()

        # si se presiona el botón 'cerrar' de la ventana
        if event.type == pygame.QUIT:
            # detiene la aplicación
            break

        # si algún botón del mouse es presionado
        if event.type == pygame.MOUSEBUTTONDOWN and str(event.button)=="1":
            x1,y1 = pygame.mouse.get_pos()
            if(x1>=x and x1<=x+x2 and y1>=y and y1<=y+y2):
                toma_anillo=1
                pantalla.blit(fondo, (0, 0))
                pantalla.blit(anillo,(x,y))
                pygame.draw.line(pantalla, colorCuerda, (x,y), (x,y),0)
                #playsound("Tirar_Cuerda_2.0.mp3")
                play("Tirar_Cuerda_2.0.mp3", None)

        # si algún botón del mouse es soltado
        if event.type == pygame.MOUSEBUTTONUP and str(event.button)=="1" and toma_anillo==1:
            toma_anillo=0
            pantalla.blit(fondo, (0, 0))
            pygame.draw.line(pantalla, colorCuerda, (x+10,y+85), (x+10,y+80),0)
            pantalla.blit(anillo,(x,y))
            reloj.tick(25)  
            pygame.display.flip()
            
            opcion = random.randint(0,7)
            if opcion==0:
                play("Creo_que_no.mp3", 0.8)
                textsurface = myfont.render("Creo que no", False, (247,248,245))
                s = pygame.Surface((textsurface.get_width(), textsurface.get_height()), pygame.SRCALPHA)   
                s.fill((0,0,0,70)) 
                screen.blit(s, ( xtexto- textsurface.get_width() // 2, ytexto))                        
                #pygame.draw.rect(pantalla, pygame.Color(255, 255, 255, 30), pygame.Rect(xtexto- textsurface.get_width() // 2, ytexto, textsurface.get_width(), textsurface.get_height()))
                screen.blit(textsurface,( xtexto- textsurface.get_width() // 2, ytexto))
                pygame.display.flip()
                #playsound("Creo_que_no.mp3")
                
            elif opcion==1:
                play("Nada.mp3", 2.7)
                textsurface = myfont.render("Nada", False, (247,248,245))
                s = pygame.Surface((textsurface.get_width(), textsurface.get_height()), pygame.SRCALPHA) #Obtiene las dimensiones del texto
                s.fill((0,0,0,70)) #Hace que el fondo del texto sea semitransparente
                screen.blit(s, ( xtexto- textsurface.get_width() // 2, ytexto)) #Posiciona el fondo del texto
                screen.blit(textsurface,( xtexto- textsurface.get_width() // 2, ytexto)) #Posiciona el texto sobre el fondo del texto
                pygame.display.flip() #Ayuda a imprimir en patalla el texto
                #playsound("Nada.mp3")
                
            elif opcion==2:
                play("Ninguno.mp3", 0.5)
                textsurface = myfont.render("Ninguno", False, (247,248,245))
                #pygame.draw.rect(pantalla, pygame.Color(255, 255, 255, 30), pygame.Rect(xtexto- textsurface.get_width() // 2, ytexto, textsurface.get_width(), textsurface.get_height()))
                s = pygame.Surface((textsurface.get_width(), textsurface.get_height()), pygame.SRCALPHA)   
                s.fill((0,0,0,70)) 
                screen.blit(s, ( xtexto- textsurface.get_width() // 2, ytexto))  
                screen.blit(textsurface,( xtexto- textsurface.get_width() // 2, ytexto))
                pygame.display.flip()
                #playsound("Ninguno.mp3")
                
            elif opcion == 3:
                play("No.mp3", 0.5)
                textsurface = myfont.render("No", False, (247,248,245))
                s = pygame.Surface((textsurface.get_width(), textsurface.get_height()), pygame.SRCALPHA)   
                s.fill((0,0,0,70)) 
                screen.blit(s, ( xtexto- textsurface.get_width() // 2, ytexto))  
                screen.blit(textsurface,( xtexto- textsurface.get_width() // 2, ytexto))
                pygame.display.flip()
                #playsound("No.mp3")
                             
            elif opcion == 4:
                play("Nooo.mp3", 2.5)
                textsurface = myfont.render("Nooo", False, (247,248,245))
                s = pygame.Surface((textsurface.get_width(), textsurface.get_height()), pygame.SRCALPHA)   
                s.fill((0,0,0,70)) 
                screen.blit(s, ( xtexto- textsurface.get_width() // 2, ytexto))  
                screen.blit(textsurface,( xtexto- textsurface.get_width() // 2, ytexto))
                pygame.display.flip()
                #playsound("Nooo.mp3")
                
            elif opcion == 5:
                play("Probablemente.mp3", 0.7)
                textsurface = myfont.render("Probablemente", False, (247,248,245))
                s = pygame.Surface((textsurface.get_width(), textsurface.get_height()), pygame.SRCALPHA)   
                s.fill((0,0,0,70)) 
                screen.blit(s, ( xtexto- textsurface.get_width() // 2, ytexto))  
                screen.blit(textsurface,( xtexto- textsurface.get_width() // 2, ytexto))
                pygame.display.flip()
                #playsound("Probablemente.mp3")
                
            elif opcion == 6:
                play("Si.mp3", 0.3)
                textsurface = myfont.render("Si", False, (247,248,245))
                s = pygame.Surface((textsurface.get_width(), textsurface.get_height()), pygame.SRCALPHA)  
                s.fill((0,0,0,70)) 
                screen.blit(s, ( xtexto- textsurface.get_width() // 2, ytexto))  
                screen.blit(textsurface,( xtexto- textsurface.get_width() // 2, ytexto))
                pygame.display.flip()
                #playsound("Si.mp3")
                
            elif opcion==7:   
                play("Pregunta_nueva.mp3", 0.3)
                textsurface = myfont.render("Prueba preguntando de nuevo", False, (247,248,245))
                s = pygame.Surface((textsurface.get_width(), textsurface.get_height()), pygame.SRCALPHA)   
                s.fill((0,0,0,70)) 
                screen.blit(s, ( xtexto- textsurface.get_width() // 2, ytexto))  
                screen.blit(textsurface,( xtexto- textsurface.get_width() // 2, ytexto))
                pygame.display.flip()
                #playsound("Pregunta_nueva.mp3")

        # si el mouse es movido
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()==(1,0,0) and toma_anillo==1:
                pantalla.blit(fondo, (0, 0))
                pygame.draw.line(pantalla, colorCuerda, (x+10,y+85), (x1,y1+77),30)
                pygame.draw.ellipse(pantalla, colorCuerda, pygame.Rect((x-10, y+65, 40, 40)), 0)
                pygame.draw.ellipse(pantalla, colorCuerda, pygame.Rect((x1-20, y1+63, 40, 42)), 0)
                pantalla.blit(anillo,(x1,y1))
                x1,y1 = pygame.mouse.get_pos()
                x1=x1-(x2/2)
                y1=y1-(y2/2)
                
        reloj.tick(25)  
        pygame.display.flip()
    
    # finaliza Pygame
    BienvenidaSalida(pantalla, "Salida_2.png","Ah_hablado.mp3", "Salida", "Adios!!!","",anchoPantalla)
    pygame.quit()
    
#Main    
screen=BienvenidaSalida(pygame.display.set_mode((1280, 800)), "Bienvenida.png","Pregunta.mp3", "Bienvenida", "Bienvenido...", "Preguntale algo a la caracola mágica!!!",1280)
ConsultaCaracola(screen, 1280)
        