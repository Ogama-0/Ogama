import pygame
from joureurCopie import Player
import pytmx
import pyscroll

import Cartecode
from Cartecode import Map_manager

class Game : # ici c'est la classe scène
    
    def __init__ (self) :
        
        self.screen = pygame.display.set_mode((1080,720))
        pygame.display.set_caption('projet NSI')
        self.continuer = True
        self.clock = pygame.time.Clock()


        self.nombre_de_frame = 0
        self.seconde_de_jeu = 0
        self.minute_de_jeu = 0
        self.heure_de_jeu = 0
        #--------------------------- joueur ---------------------------------#

        self.player = Player(0,0)

        # --------------------------------- MAP ----------------------------#

        self.map_manager = Map_manager(self.screen, self.player)
        

    def touches_appuiller(self):
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                self.continuer = False

        self.touches = pygame.key.get_pressed()

    
    def GestionEvent(self) : # ici que sont géré les différents évenement comme l'appuit des touches ou le alt f4 ->(QUIT)
        
        self.gestion_sprint()
        self.gestion_deplacement()

    def gestion_sprint(self) :

        if self.touches[pygame.K_LSHIFT] :
            self.player.sprint = 1
        else :
            self.player.sprint = 0

        
    def gestion_deplacement(self):
        a=0 #savoir s i l'anime s'est deja passer  
        if self.touches[pygame.K_UP] :
            self.player.velocité[1] = -1
            self.player.etat_regard_yeux_nanit['etat_regard'] = 3
        elif self.touches[pygame.K_DOWN] :
            self.player.velocité[1] = +1
            self.player.etat_regard_yeux_nanit['etat_regard'] = 4
        else :
            self.player.velocité[1] = 0
            a+=1

        if self.touches[pygame.K_LEFT] :
            self.player.velocité[0] = -1
            self.player.etat_regard_yeux_nanit['etat_regard'] = 1 
        elif self.touches[pygame.K_RIGHT] :
            self.player.velocité[0] = +1
            self.player.etat_regard_yeux_nanit['etat_regard'] = 2
        else :
            self.player.velocité[0] = 0
            a+=1
        
        if self.touches[pygame.K_UP] and self.touches[pygame.K_RIGHT] :
            self.player.etat_regard_yeux_nanit['etat_regard'] = 5
        if self.touches[pygame.K_UP] and self.touches[pygame.K_LEFT] :
            self.player.etat_regard_yeux_nanit['etat_regard'] = 6

        self.player.vitesse += self.player.sprint
        self.player.deplacement = self.player.velocité[0]*self.player.vitesse, self.player.velocité[1]*self.player.vitesse
        self.player.position[0] += self.player.deplacement[0]
        self.player.position[1] += self.player.deplacement[1]

        self.player.Animation(a)

    
    def update (self,touches) : #gestion de logique et la misa a jour des différents perso du jeu et les colisions
        
        self.map_manager.update(touches)

        self.screen.blit(self.player.test_image,(50,50))

        
        


    def affichage(self) : #tout ce qui vas etre afficher dans le screen
        #self.screen.fill("grey") #initialisation de l'écrant (c'étais au debut je laisse tout pour l'instant pour corriger des erreurs plus facilement)
        
        

        self.map_manager.dessier_la_carte()
        self.screen.blit(self.score_text,(20,20))
        #self.player.afficher(self.screen)#affichage du perso avec la methode afficher qui est dans joureur.py
        pygame.display.flip()#on met a jour l'écrant

    
    def minueur(self):

        font = pygame.font.SysFont("monospace",16)

        self.nombre_de_frame+=1
        if self.nombre_de_frame >= 60 :
            self.nombre_de_frame = 0
            self.seconde_de_jeu +=1
            print(self.seconde_de_jeu)
        if self.seconde_de_jeu >= 60 :
            self.seconde_de_jeu = 0
            self.minute_de_jeu += 1
        if self.minute_de_jeu >= 60 :
            self.minute_de_jeu = 0
            self.heure_de_jeu += 1

         
            
        self.score_text = font.render(f"temps de jeu : {self.seconde_de_jeu} seconde",1,(255,255,255))


    def run (self): #boucle de jeu (tout globalemnt et c'est ça qui se rafraichie tout les frames )

        while self.continuer :



            self.player.save_location()
           
            self.minueur()

            self.touches_appuiller()
            #print(f"{self.player.position} touche self.position frame n°{self.player.nombre_de_frame}")
            self.GestionEvent()
            #print(f"{self.player.position} gestion self.position frame n°{self.player.nombre_de_frame}")
            self.update(self.touches)

            #print(f"{self.player.position} update self.position frame n°{self.player.nombre_de_frame}"
            self.affichage()
            
            self.clock.tick(60)# gère a cb1 de fps le jeu tourne (60 c'est bien)
            #print(f"{self.player.position} self.position frame n°{self.player.nombre_de_frame}")

 # ----------------------------Programe pour initialiser le jeu --------------------------#

pygame.init()

game = Game()


game.run()

pygame.quit()