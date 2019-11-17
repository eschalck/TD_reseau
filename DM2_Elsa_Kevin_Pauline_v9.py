## Devoir maison 2 - Simulation de dynamiques de reseaux
## auteurs : Elsa SCHALCK, Kevin PLESSIS, Pauline MATHIEU

import random as rd
import matplotlib.pyplot as plt

class entite(object):  
    """
    Classe définissant une entité.  
    """             

    def __init__(self,id_entite,coord=[],espace=[50,50]):
        """
        Constructeur qui initialise:
            - id_entite : (int), numéro d'identification de l'entité.  
            - p_connexion : (float), probabilité d’être connectée à une autre entité.
            - p_consultation : (float), probabilité de consulter de l’information à un instant donné.
            - p_appreciation : (float), probabilité d’apprécier cette information.
            - p_transfert : (float), probabilité de transférer une information à son tour.
            - groupe : (string : {"bon_public","mauvais_public"}), groupes auxquels appartient l'entité, en fonction de sa probabilite p_appreciation.
            - connexions : (list), liste des entites auxquelles elle est connectée.
            - position : (list : [x,y]), position de l'entité dans l'espace (2D). 
            
            Arguments: 
            - coord : (list : [x,y]), coordonnées de l'entité dans l'espace (2D) (liste vide par défaut si les coordonnées ne sont pas renseignées). 
            - espace= (list : [x,y]), x = borne supérieur en abscisse du réseau et y = borne supérieure en ordonnée du réseau. ([50,50] par défaut).
        """
        self.id_entite=id_entite
        self.p_connexion= rd.random()
        self.p_consultation= rd.random()
        self.p_appreciation= rd.random()
        self.p_transfert= rd.random()
        
        if self.p_appreciation > 0.5 : # si l'entité a plus de 50% de chance d'apprecier l'information, alors on la catégorise comme une entité 'bon_public"
            self.groupe="bon_public"
        else: # si l'entité a moins de 50% de chance d'apprecier l'information, alors on la catégorise comme une entité 'mauvais_public"
            self.groupe="mauvais_public"
            
        self.connexions=[] 
        
        if coord==[]: # si les coordonnées de l'entité ne sont pas renseignées, on prend des coordonnées aléatoires dans l'espace. 
            self.position=[rd.randint(0,espace[0]),rd.randint(0,espace[1])]
        else : 
            self.position=coord # sinon, on affecte les coordonnées renseignées en entrée à la position de l'entité. 
        

class reseau(object):
    """
    Classe définissant un réseau, lui-même composé d'entités. 
    
    Méthodes de la classe : 
        - distance : calcule la distance entre deux entités du réseau.
        - diametre : calcule le diamètre du réseau. 
        - graphique : affiche une représentation graphique du réseau.
    """    
    
    def __init__(self,id_reseau,nb_entites=10,espace=[50,50]):
        """
        Constructeur qui initialise:
            - id_reseau : (int), numéro d'identification du réseau.  
            - nb_entites : (int), nombre d'entités composant le réseau.
            - espace : (list de type [x,y]), x = borne supérieur en abscisse du réseau et y = borne supérieure en ordonnée du réseau.
            - entites : (list), liste des entités qui composent le réseau. 
            
        Arguments : 
            - id_reseau : obligatoire. 
            - nb_entites : facultatif, 10 par défaut. 
            - espace : facultatif, [50,50] par défaut.
        """
        self.id=id_reseau
        self.nb_entites=nb_entites
        self.espace=espace
        
        # création du nombre d'entités renseigné en entrée
        self.entites=[]
        liste_positions_entites=[]
        for k in range(0,self.nb_entites): 
            position_entite=[rd.randint(0,espace[0]),rd.randint(0,espace[1])]
            while position_entite in liste_positions_entites: #on verifie que la position occupée par l'entité n'est pas déjà prise
                position_entite=[rd.randint(0,espace[0]),rd.randint(0,espace[1])]
            liste_positions_entites+=[position_entite] 
            new_entite=entite(k,position_entite)
            self.entites.append(new_entite)
        
        # connexions entre les entités
        for entite1 in self.entites: 
            for entite2 in self.entites:
                if entite1 != entite2:
                    alea_connexion=rd.random()
                    if alea_connexion<entite1.p_connexion:
                        entite1.connexions+=[entite2]
            
            
    def distance(self,index_entite1,index_entite2):
        """
        Méthode  renvoie la distance dans le reseau entre les entites avec pour index "index_entite1" et "index_entite2".
        
        index_entite1 : (int), index de l'entité 1.
        index_entite2 : (int), index de l'entité 2.
        
        --> (float), distance entre les deux entités considérées. 
        """
        
        self.distance=((self.entites[index_entite1-1].position[0]-self.entites[index_entite2-1].position[0])**2+(self.entites[index_entite1].position[1]-self.entites[index_entite2].position[1])**2)**(1/2)
        return self.distance 

    
    def diametre(self):
        ''' 
        Méthode qui calcule le diamètre du réseau. 
        
        --> (float), diamètre du réseau. 
        '''
        
        #calcul du centre de gravité du réseau
        centre=[0,0]
        nb_entite=len(self.entites)
        for entite in self.entites:
            centre[0]+=entite.position[0]/nb_entite
            centre[1]+=entite.position[1]/nb_entite
        #recherche du point le plus éloigné du centre de gravité et calcul du rayon
        rayon=0
        for entite in self.entites:
            distance_max=((entite.position[0]-centre[0])**2+(entite.position[1]-centre[1])**2)**(1/2)
            if distance_max>rayon:
                rayon=distance_max
        #calcul du diamètre
        self.diametre=2*rayon
        return self.diametre
            

    def graphique(self):
        ''' 
        Méthode qui affiche une représentation graphique du réseau. 
        
        Ajout d'un attribut au réseau : 
            - figure : représentation graphique du réseau. 
        
        '''
        self.figure=plt.figure(figsize=(10, 6))
        # cree un nuage de points contenant chaque entite du reseau.
        x1=[]
        y1=[]
        x2=[]
        y2=[]
        for entite in self.entites:
            if entite.groupe=="bon_public":
                x1.append(entite.position[0])
                y1.append(entite.position[1])
            else:
                x2.append(entite.position[0])
                y2.append(entite.position[1])
        plt.scatter(x1,y1, marker='o', label='Entité bon publique', c='#50C878', s=180)
        plt.scatter(x2,y2, marker='o', label='Entité mauvais publique', c='#F51B00', s=180)
        #crée des lignes entre les points pour les connexions entre les entités du réseau. 
        for i in range(0,self.nb_entites):
            for j in range(0,len(self.entites[i].connexions)):
                x=[self.entites[i].position[0], self.entites[j].position[0]]
                y=[self.entites[i].position[1], self.entites[j].position[1]]
                plt.plot(x,y, color='0.3', linewidth=0.4)
        plt.title("Représentation du réseau "+str(self.id))
        axes=plt.gca()
        axes.set_xlabel('x')
        axes.set_ylabel('y')
        self.figure.legend()
        plt.show()
        

class information(object):
    """
    Classe définissant une information. 
    """    
    
    def __init__(self,id_information):
        """
        Constructeur qui initialise:
            - id_information : (int), numéro d'identification de l'information.  
            - temps_dans_reseau : (int), temps de la simulation (en nombre de pas) que l'information a passé dans le réseau, c’est-à-dire le nombre de pas de temps où elle était consultable par au moins une entité du réseau.
            - statut_global : (string, 'active' ou 'inactive'), statut de l'activité de l'information : ‘active’ si l’information est encore consultable par au moins une entité, ‘inactive’ sinon.
            - nb_entites : (int), nombre d’entites qui ont consulté l’information. 
            
            - liste_entites : (list = [[id_reseau, id_entite, statut, tps_consultabilite, appreciation], [id_reseau, id_entite_2, …]])
            liste des entités qui ont reçu l'information avec les détails de l'information pour cette entité. 
            Pour chaque entité, on a, sous forme de liste, les détails suivants : 
                - id_reseau : (int), identifiant du réseau dans lequel vit l'information.
                - id_entite : (int), identifiant de l'entité qui a reçu l'information. 
                - statut : (string, 'consultable' ou 'consultee' ou 'non_consultable'), statut de l'info dans l'entité considérée : ‘active’ si l’information est encore consultable, 'inactive' sinon. 
                - tps_consultabilite : (int), temps en pas de temps passé par l'information dans l'entité en étant consultable.
                - appreciation : (string, 'a_apprecier', 'bien' ou 'mauvais'), appréciation de l'information par l'entité. 
                        
        Argument : 
            - id_information : obligatoire. 
        """

        self.id_information=id_information
        self.temps_dans_reseau=0
        self.statut_global='active'
        self.nb_entites=0
        self.liste_entites=[]
        

class simulation(object):
    """
    Classe définissant une simulation. 
    
    Méthodes: 
        - avance : avance la simulation d'un pas de temps et réalise tous les changements nécessaires concernant la simulation et les informations qu'elle contient. 
        - simul_temps_max : methode qui simule la simulation tant qu'il y a encore des informations actives dans le réseau et tant que la simulation n'a pas duré plus longtemps qu'un temps maximum.
    """    
    
    def __init__(self,id_simulation,reseau,temps_consultation=3):
        """
        Constructeur qui initialise:
            - id_simulation : (int), numéro d'identification de l'information.  
            - temps : (int), temps (en nombre de pas) de la simulation.
            - temps_consultation : (int), temps exprimé en pas de temps qu’a chaque entité du réseau pour consulter une information dans le cadre de cette simulation.
            - liste_info : (list), liste des informations circulant ou ayant circulé dans le réseau. 
            - reseau : (reseau), reseau dans lequel a lieu la simulation. 
            
        Arguments : 
            - id_simulation : obligatoire. 
            - reseau : obligatoire.
            - temps_consultation : facultatif, 3 pas de temps par défaut. 
        """
        
        self.id_simulation=id_simulation
        self.temps=0 # on part de t=0
        self.temps_consultation=temps_consultation
        self.liste_info=[]
        self.reseau=reseau
        
    def avance(self):
        ''' 
        Méthode qui fait avancer la simulation d'un pas de temps 
        et qui réalise tous les changements nécessaires concernant la simulation et les informations qu'elle contient.  
        
        '''
        
        reseau=self.reseau
        #creation d'une nouvelle information
        nvlle_info=information(self.temps) #l'id de l'information est le moment auquel elle a été créée
        self.liste_info+=[nvlle_info] 
        nvlle_info.liste_entites+=[[reseau.id,rd.randint(0,reseau.nb_entites-1),'consultable',0,'a_apprecier']]
        self.temps+=1
        #liste_entites=[id_reseau, id_entite aléatoire, statut de l'info dans l'entité, temps passé dans l'entité en étant consultable, appréciation]
        
        #on parcourt la liste des informations pour les propager
        for info in self.liste_info:
            if info.statut_global=='active':#on regarde si l'information est encore dans le réseau
                info.temps_dans_reseau+=1 #on incremente le temps passe dans le reseau de 1
                liste_entites_propagees=[] #Correspond a la liste des entites que l'on va rajouter à liste_entite apres propagation
                liste_entite_dans_information=[] #Correspond à la liste des entités contenues dans liste_entite, est utilisé pour le renvoi de l'information
                
                for info_entite in info.liste_entites:
                    id_entite=info_entite[1]
                    liste_entite_dans_information+=[reseau.entites[id_entite]]

                
                for info_entite in info.liste_entites:
                    
                    if info_entite[2]=='consultable': #si l'info est consultable, on peut effectuer plusieurs actions dessus
                        info_entite[3]+=1
                        id_entite=info_entite[1]
                        entite=reseau.entites[id_entite]
                        
                        #appreciation de l'information par l'entite
                        alea_appreciation=rd.random()
                        if alea_appreciation < entite.p_appreciation:
                            info_entite[4]='bien' # On pourrait mettre des valeurs binaires 0 et 1 si besoin pour la représentation?
                        else:
                            info_entite[4]='mauvais'
                            
                        #renvoi de l'information:
                        for entite_connecte in entite.connexions: #on parcourt les entités connectés à l'entité que l'on regarde
                            if entite_connecte not in liste_entite_dans_information: #on vérifie que l'entité connecté ne possède pas déjà l'information 
                                alea_connexion=rd.random()
                                if alea_connexion < entite.p_connexion:
                                    liste_entites_propagees+=[[reseau.id,entite_connecte.id_entite,'consultable',0,'a_apprecier']]
                                    liste_entite_dans_information+=[entite_connecte]
                        
                        #consultation de l'information
                        alea_consultation=rd.random()
                        if alea_consultation<entite.p_consultation:
                            info_entite[2]='consultee'
                            info.nb_entites+=1
                            
                        #si l'info n'a pas été consultée depuis trop longtemps par une entité, elle devient non_consultable
                        #on verifie que le statut n'est pas 'consultee' car il est possible qu'une info soit consultee à l'étape juste avant
                        if info_entite[3]>= self.temps_consultation and info_entite[2]!='consultee':
                            info_entite[2]='non_consultable'
                            
                #on actualiste liste_entites avec les nouvelles entites pour lesquelles l'information a été propagée                
                info.liste_entites+=liste_entites_propagees 
                    
                #derniere etape: on verifie que l'information est active pour toutes ses entités, sinon on donne le statut 'inactive' à l'information
                nb_info = len(info.liste_entites)
                cpt_info_indispo=0
                    
                #nb entités où l'info n'est pas propageable
                for info_entite in info.liste_entites: 
                    if info_entite[2]!='consultable':
                        cpt_info_indispo+=1
                    
                #si on a autant d'entités non-propageables que d'entités, cela signifie que l'info est inactive
                if cpt_info_indispo==nb_info:
                    info.statut_global='inactive'
                        
    def simul_temps_max(self,temps_max=20, visualisation=False):
        """
        Methode qui procède a des itérations de la méthode avance() tant que le pas de temps est inférieur 
        à temps max et qu'il y a encore des informations actives dans le réseau. 
        
        Argument : 
            - temps_max : (int), temps maximum en pas de temps de la simulation.
            - visualisation : (booleen), activation ou non de la visualisaiton de la simulation dans une interface graphique. 
            Par défaut, on ne visualise pas la simulation. 
        """
            
        cpt_pas=0
        statut_infos='actives'
        
        y_infos_actives_tps=[0]
        y_infos_inactives_tps=[0]
        y_infos_bien_tps=[0]
        y_infos_mauvais_tps=[0]
        
        while cpt_pas<temps_max and statut_infos=='actives':
            
            cpt_pas+=1
            
            #visualisation de la simulation dans le temps
            #calculs pour les graphes 1 et 2
            if visualisation==True:
                y_infos_actives_tps=y_infos_actives_tps+[0]
                y_infos_inactives_tps=y_infos_inactives_tps+[0]
                y_infos_bien_tps=y_infos_bien_tps+[0]
                y_infos_mauvais_tps=y_infos_mauvais_tps+[0]
                for info in self.liste_info:
                    if info.statut_global=='active':
                        y_infos_actives_tps[-1]=y_infos_actives_tps[-1]+1
                    else:
                        y_infos_inactives_tps[-1]=y_infos_inactives_tps[-1]+1
                    for i in range(0,len(info.liste_entites)):
                        if info.liste_entites[i][-1]=='bien':
                            y_infos_bien_tps[-1]=y_infos_bien_tps[-1]+1
                        elif info.liste_entites[i][-1]=='mauvais':
                            y_infos_mauvais_tps[-1]=y_infos_mauvais_tps[-1]+1
                        
            
            self.avance()
            cpt_infos_inactives=0
            for info_test in self.liste_info:
                if info_test.statut_global=='inactive':
                    cpt_infos_inactives+=1
            if cpt_infos_inactives==len(self.liste_info):
                statut_infos='inactives'
                print('La simulation s est arrete apres', cpt_pas, ' pas')
        
        if visualisation==True:
            
            #calculs pour les graphes 3 et 4
                
            n=self.reseau.nb_entites
            y_entite_infos_recu=[0]*n
            y_entite_infos_consultees=[0]*n
            y_entite_infos_bien=[0]*n
            y_entite_infos_mauvais=[0]*n

            y_info_bien=[0]*self.temps
            y_info_mauvais=[0]*self.temps
            
            for k in range(0,len(self.liste_info)):
                for i in range(0,len(self.liste_info[k].liste_entites)):
                    identifiant=self.liste_info[k].liste_entites[i][1]
                    y_entite_infos_recu[identifiant]+=1
                    if self.liste_info[k].liste_entites[i][-1]=='bien':
                        y_entite_infos_bien[identifiant]+=1
                        y_info_bien[k]+=1
                    elif self.liste_info[k].liste_entites[i][-1]=='mauvais':
                        y_entite_infos_mauvais[identifiant]+=1
                        y_info_mauvais[k]+=1
                    if self.liste_info[k].liste_entites[i][2]=='consultee':
                        y_entite_infos_consultees[identifiant]+=1
            
            info_max=[]
            info_min=[]
            score_info_max=0
            score_info_min=0
            
            for k in range(0,len(self.liste_info)):
                if y_info_bien[k]>score_info_max:
                    score_info_max=y_info_bien[k]
                    info_max=[k]
                elif y_info_bien[k]==score_info_max:
                    score_info_max=y_info_bien[k]
                    info_max=info_max+[k]
                if y_info_mauvais[k]>score_info_min:
                    score_info_min=y_info_mauvais[k]
                    info_min=[k]
                elif y_info_mauvais[k]==score_info_min:
                    score_info_min=y_info_mauvais[k]
                    info_min=info_min+[k]
            
            #création de la figure
            
            fig, [ax1, ax2, ax3, ax4] = plt.subplots(4, 1, figsize=(10,30))
            fig.suptitle('Visualisation de la simulation '+str(self.id_simulation), fontsize=16)
            plt.figtext(0.1, 0.9, "Arret de la simulation au temps: "+str(self.temps)+"\nTemps maximal de la simulation: "+str(temps_max)+"\nIdentifiant du réseau hôte : "+str(self.reseau.id)+"\nInformation(s) ayant obtenu le plus de mentions 'bien': "+str(info_max)+" (score: "+str(score_info_max)+")\nInformation(s) ayant obtenu le plus de mentions 'mauvais': "+str(info_min)+" (score: "+str(score_info_min)+")", fontweight = 'bold')
            
            #graphe 1 : nombre d'informations actives/inactives en fonction du temps
            barWidth1=0.4
            x_tps=range(0,self.temps+1)
            x_tps_2 = [x + barWidth1 for x in x_tps]
            ax1.bar(x_tps, y_infos_actives_tps, width = barWidth1, color = ['blue' for i in y_infos_actives_tps], label='Informations actives')
            ax1.bar(x_tps_2, y_infos_inactives_tps, width = barWidth1, color = ['orange' for i in y_infos_inactives_tps], label='Informations inactives')
            ax1.legend()
            ax1.set_xlabel('Temps')
            ax1.set_ylabel("Nombre d'informations")
            ax1.set_title("Nombre d'informations actives/inactives au cours du temps")
            
            #graphe 2 : nombre d'appréciations 'bien' et 'mauvais' en fonction du temps
            barWidth2=0.4
            ax2.bar(x_tps, y_infos_bien_tps, width = barWidth2, color = ['green' for i in y_infos_bien_tps], label='Bien')
            ax2.bar(x_tps_2, y_infos_mauvais_tps, width = barWidth2, color = ['red' for i in y_infos_mauvais_tps], label='Mauvais')
            ax2.legend()
            ax2.set_xlabel('Temps')
            ax2.set_ylabel("Nombre d'appréciations")
            ax2.set_title("Nombre d'appréciation 'bien' et 'mauvais' au cours du temps")
            
            #graphe 3 : pour chaque entité : nb info passées, nb infos consultées, nb infos appréciées (bien ou mauvaises)
            
            barWidth3=0.2
            x1=range(0,n)
            x2 = [x + barWidth3 for x in x1]
            x3 = [x + barWidth3 for x in x2]
            x4 = [x + barWidth3 for x in x3]
            
            ax3.bar(x1, y_entite_infos_recu, width = barWidth3, color = ['blue' for i in y_entite_infos_recu], label='Informations reçues')
            ax3.bar(x2, y_entite_infos_consultees, width = barWidth3, color = ['orange' for i in y_entite_infos_consultees], label='Informations consultées')
            ax3.bar(x3, y_entite_infos_bien, width = barWidth3, color = ['green' for i in y_entite_infos_bien], label='Informations appréciées (bien)')
            ax3.bar(x4, y_entite_infos_mauvais, width = barWidth3, color = ['red' for i in y_entite_infos_mauvais], label='Informations appréciées (mauvais)')
            ax3.legend()
            ax3.set_xlabel('Entités (id)')
            ax3.set_ylabel("Nombre d'informations")
            ax3.set_title("Traitement des informations par les entités")
            
            #graphe 4 : nombre d'appréciations (bien ou mauvaises) pour chaque information à la fin de la simulation 
            
            barWidth4=0.4
            x_1=range(0,self.temps)
            x_2=[x + barWidth4 for x in x_1]
            
            ax4.bar(x_1, y_info_bien, width = barWidth4, color = ['green' for i in y_info_bien], label='Bien')
            ax4.bar(x_2, y_info_mauvais, width = barWidth4, color = ['red' for i in y_info_mauvais], label='Mauvais')
            ax4.legend()
            ax4.set_xlabel("Informations")
            ax4.set_ylabel("Nombre d'appréciations")
            ax4.set_title("Bilan des appréciations par information")
            
            plt.show()

''' 
Tests manuels des fonctions 
'''

r=reseau(1)
print('le reseau est :', r.entites)
print('la distance entre les entites 4 et 6 du reseau est :', r.distance(4,6))
print('le diametre du reseau est :', r.diametre())
r.graphique()

simu=simulation(1,r,temps_consultation=10)
simu.simul_temps_max(150, visualisation=True)

#Montre les caractéristiques de toutes les informations
#for info_test in simu.liste_info:
#    print('L info est la numéro: ',info_test.id_information)
#    print('elle a passé ', info_test.temps_dans_reseau,' pas de temps dans le réseau')
#    print('elle est ', info_test.statut_global)
#    print('Elle s est propagée à ', len(info_test.liste_entites), 'entités')
#    print('Elle a été consultée par :', info_test.nb_entites, 'entités')
#    print('la liste des entités ou l info s est propagee est la suivante:' )
#    for entity in info_test.liste_entites:
#        print(entity)

#Montre les caractéristiques des informations inactives
#for info_test in simu.liste_info:
#    if info_test.statut_global=='inactive':
#        print('L info est la numéro: ',info_test.id_information)
#        print('elle a passé ', info_test.temps_dans_reseau,' pas de temps dans le réseau')
#        print('elle est ', info_test.statut_global)
#        print('Elle s est propagée à ', len(info_test.liste_entites), 'entités')
#        print('Elle a été consultée par :', info_test.nb_entites, 'entités')
#        print('la liste des entités ou l info s est propagee est la suivante:' )
#        for entity in info_test.liste_entites:
#            print(entity)

#test pour verifier le critere d'arret de simul_temps_max
cpt_info,cpt_info_inactive=0,0
for info_test in simu.liste_info:
    cpt_info+=1
    if info_test.statut_global=='inactive':
        cpt_info_inactive+=1
print('Il y a ', cpt_info, ' informations dans la simulation')
print('Il y a ', cpt_info_inactive, ' informations inactives dans la simulation')
        
