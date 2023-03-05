import pytmx, pygame, pyscroll
from dataclasses import dataclass


@dataclass
class enigme : 
    nom : str
    monde : str
    zone_de_detection : pygame.Rect
    sprite : pygame.image
    monde_de_enigme : str
    spawn = 'spawn'


@dataclass
class Portail :
    monde_origine : str
    poin_origine : str
    monde_arriver : str
    poin_de_sortie : str
    

@dataclass
class Map :
    type : str #"exterieur" = exterrieur "interieur" = "interieur" "enigme + nom_énigme " = enigme
    name : str
    murs : list[pygame.Rect]
    group : pyscroll.PyscrollGroup
    tmx_data : pytmx.TiledMap
    spawn : list[int]
    
    portails : list[Portail]
    enigmes : list[enigme]
    


class Map_manager :

    def __init__(self,screen, player):

        self.maps = dict()#création d'un dico avec tt les maps avec {nom : donné de la classe Map}
        self.curent_map = "manoir_moyen_test1"#remplacer par la verai enfin on espères
        self.player = player
        self.screen = screen


    #----------------------------- Portail --------------------------------#
    #Portail("","","","")

        portail_lavraienfinonespère =   [Portail('lavraienfinonespère',"tp maison test","maison test" , "spawn"),
                                        Portail("lavraienfinonespère","entrer manoir maptest","manoir_grand_test1","entrer manoir"),
                                        Portail("lavraienfinonespère","entrer manoir petit","betatest_manoire","spawn"),
                                        Portail("lavraienfinonespère", "entrer manoir moyen","manoir_moyen_test1","entrer manoir porte principale")
                                        ]
        
        portail_manoir_grand_test1 =    [Portail('manoir_grand_test1',"sortie manoir","lavraienfinonespère",'sortie manoir maptest')
                                        ]
        
        portail_maison_test =           [Portail("maison test", "sortie maison 1", "lavraienfinonespère", "retour maisontest")
                                        ]
        
        portail_betatest_manoire =      [Portail("betatest_manoire","sortie_manoir_petit","lavraienfinonespère","sortie manoir petit(overword)")
                                        ]

        portail_manoir_moyen_test1 =    [Portail("manoir_moyen_test1","sortie porte principal manoir","lavraienfinonespère","sortie manoir moyen")
                                        ]

        portail_enigme_horloge =        [Portail("enigme_horloge","sortie labythinte","manoir_moyen_test1","sortie  horloge")
                                        ]


        égnime_de_manoir_moyen_test1 =  ["horloge"]

        #True = interieur
        #False = exterieur

        self.enregistrer_une_map("exterieur",'lavraienfinonespère',portail_lavraienfinonespère)
        self.enregistrer_une_map("interieur",'manoir_grand_test1', portail_manoir_grand_test1)
        self.enregistrer_une_map("interieur",'maison test',portail_maison_test)
        self.enregistrer_une_map("interieur",'betatest_manoire',portail_betatest_manoire)
        self.enregistrer_une_map("interieur","manoir_moyen_test1",portail_manoir_moyen_test1, égnime_de_manoir_moyen_test1)
        self.enregistrer_une_map("enigme horloge","enigme_horloge",portail_enigme_horloge) 
        
        self.tp_joueur('spawn')
    
    def enregistrer_une_map(self, map_type : str , name_map : str, list_portail = [Portail], nom_enigme = [] ) : #nom_enigme est une list avec le nom de l'enigme

        

        tmx_data = pytmx.util_pygame.load_pygame(f"map/{name_map}.tmx")#on charge la bonne map Kappa
        map_data = pyscroll.data.TiledMapData(tmx_data)
        #afficher ce tmx sur le screen
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        
        
        #gerer le zoom de la cam :
        if map_type == "exterieur" :
            map_layer.zoom = 1.5
        elif map_type == "enigme horloge":
            map_layer.zoom = 2
        elif map_type == "interieur" :
            map_layer.zoom = 2

        self.spawn = tmx_data.get_object_by_name('spawn')
        self.spawn = [self.spawn.x,self.spawn.y]

        #il faut donc dessiner le groupde de calque (différentes couche du jeu pour afficher )
        
        
            #------------------Colisions-----------------#
        self.murs = []
        for obj in tmx_data.objects :
            if obj.type == 'collision' :
                self.murs.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        print(f'il y a {len(self.murs)} mur dans la carte {name_map}')
        
        group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        group.add(self.player)
        
       

        
        enigmes = []
        for i in range(len(nom_enigme)) :
            self.enigme_detect = []
            for enigm in tmx_data.objects :
                #print(nom_enigme[i])
                if enigm.name == 'zonne de detection '+ nom_enigme[i] :
                    #print(enigm.x)
                    self.enigme_detect.append(pygame.Rect(enigm.x,enigm.y,enigm.width,enigm.height))
            
            #print(self.enigme_detect)
            
            sprite_enigme = pygame.image.load('sprite/sprint_enigme/horloge/horloge.jpg')
                    
            enigmes.append(enigme(nom_enigme[i],name_map,self.enigme_detect[i],sprite_enigme,"enigme_"+ nom_enigme[i],))

        
        print(f'il y a {len(enigmes)} enigme(s) dans la carte {name_map}')
        #print(enigmes)
        #on crée un object Map 
        
        self.maps[name_map] = Map(map_type,name_map, self.murs, group, tmx_data, self.spawn, list_portail, enigmes ) 
        

        
    def get_map(self) : return self.maps[self.curent_map]

    def get_group(self) : return self.get_map().group
    
    def get_murs(self) : return self.get_map().murs 

    def get_object(self, name) : return self.get_map().tmx_data.get_object_by_name(str(name))
    

    
    def tp_joueur(self, point_de_tp: str)  :
        point = self.get_object(point_de_tp)
        self.player.position = [point.x, point.y]
        self.player.save_location()
    
    def chect_collison(self,touches) : 
        #portail
        
        for portail in self.get_map().portails :
            #print(portail.monde_origine)
            if portail.monde_origine == self.curent_map :
                poin = self.get_object(portail.poin_origine)
                rect = pygame.Rect(poin.x,poin.y,poin.width,poin.height)

                if self.player.position_pour_les_colision.colliderect(rect) :
                    copy_portail = portail
                    self.curent_map = portail.monde_arriver
                    self.tp_joueur(copy_portail.poin_de_sortie)
        #
        for enigme in self.get_map().enigmes :
            if enigme.monde == self.curent_map :
                detect = enigme.zone_de_detection
                #print(detect)
                rect = pygame.Rect(detect.x,detect.y,detect.width,detect.height)
                if self.player.position_pour_les_colision.colliderect(rect) :
                    if touches[pygame.K_e] :
                        copy_enigme = enigme
                        self.curent_map = enigme.monde_de_enigme
                        self.tp_joueur(copy_enigme.spawn)

                


        #interieur/exté
        if self.get_map().type == "exterieur" :
            self.player.vitesse = 2
        elif self.get_map().type == "interieur" :
            self.player.vitesse = 3
        elif self.get_map().type == "enigme horloge" :
            self.player.vitesse = 2

        #murs
        if self.player.position_pour_les_colision.collidelist(self.get_murs()) > -1 :
            self.player.move_back()




    def dessier_la_carte(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self,touche):
        self.get_group().update()
        self.chect_collison(touche)
