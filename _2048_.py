import numpy as np

class _2048(object):
    """Crée une partie du jeu 2048."""
    def __init__(self):
        """Crée l'état de départ de la partie et
            coordonne les différentes fonctions 
            pendant toute la partie"""
        self.matrix = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])#cree une matrix 4x4 vide.
        self.WIN = False#le joueur n'a pas atteind 2048.
        self.FAIL = False#le joueur n'est pas blocke est n'a donc pas perdu.
        self.nb_de_tours = 1
        self.score = 0
        self.step_score = 0
        self.High_value = 2
        self.rangee = np.array([0,0,0,0])
        self.V = np.array([             #possibilite du mouvements vers:
                [True,True,True,True],  #le haut:colonnes 1,2,3,4
                [True,True,True,True],  #le bas:colonnes 1,2,3,4  
                [True,True,True,True],  #la droite:lignes 1,2,3,4
                [True,True,True,True]   #la gauche:lignes 1,2,3,4
                ])
        self.v = np.array([True,True,True,True])#possibilite du mouvement selon haut,bas,droite,gauche, toutes lignes et colonnes combinees
        
        self.matrix = self.remplissage(self.remplissage(self.matrix)) #genere les deux cases aleatoires de depart.
        self.Verif_Globale()#verifie si les mouvements du prochain tour son possibles et selon quelles directions et sens ils le sont.
    
    def tour(self,user_input):
        """gere la progression d'un tour"""
        verif = self.Verif_mouv(user_input)#verifie que le mouvement demander est possible.
        if np.array_equal(verif,np.array([False,False,False,False])):pass#ne fait rien si il n'est pas possible.
        else:#continue normalement si il l'est.
            self.matrix = self.mouvement(verif,self.matrix)#applique le mouvement demande a la grille.
            self.matrix = self.remplissage(self.matrix)#rajoute un 2 ou un 4 aleatoirement sur une case vide de la grille.
            self.Verif_Globale()#verifie si les mouvements du prochain tour son possibles et selon quelles directions et senses ils le sont.
            self.nb_de_tours+=1#incremente les nombre de tours
            self.High_value = max(map(max, self.matrix))
    
    
    def Verif_mouv(self, T):
        """Determine si le mouvement demandé est possible et donne sa 
            direction et son sens si il l'est
            prend les directions provenants de user_input et les compare
            a self.v les directions et sens possibles"""
        return np.logical_and(self.v,T)
    
    def extractor3000(self, numero, direction):
        """Extrait (de la grille du jeu) une colonne ou une ligne selon le mouvement
         demandé.(Ca permet d'évaluer ensuite plus facilement la possibilité du mvt)"""
        """ si le mvt n'est pas dans le sens positif on extrait les elements dans le sens inverse"""
        
        if direction == 'droite': rangee = self.matrix[numero,:]
        elif direction == 'gauche' : rangee = self.matrix[numero,::-1]
        elif direction == 'bas' : rangee = self.matrix[:,numero]
        elif direction == 'haut' : rangee = self.matrix[::-1, numero]
        return rangee
    
    def premiere_case(self,X):
        """renvoie la position de la première case non vide (ie pas égale à 0)"""
        
        n = np.size(X)
        for i in range(n):
            if X[i] != 0:
                return i
        return 3
     
    def Verif_elementaire(self, numero, sens):
        """Renvoie True ou False selon si le mvt demandé sur UNE ligne ou UNE colonne est possible"""
        """utilise extractor3000 pour travailler sur un seul vecteur
        utilise premiere_case pour aller plus vite sur les tests"""
        
        work_on = self.extractor3000(numero, sens)
        start = self.premiere_case(work_on)
        for i in range(start, 3):
            if work_on[i] == work_on[i+1] or work_on[i+1] == 0:
                return True  
        return False
    
    def Verif_Globale(self):
        """utilise 16x la fonction verif_elementaire pour
            determiner selon quelles directions et quels sens 
            le mouvement est possible pour chaque colonne et lignes
            acctualise les deux arrays v et V qui sauvegardent ses donnees
            pendant un tour"""
        self.V = np.array([[self.Verif_elementaire(0,'haut'),self.Verif_elementaire(1,'haut'),self.Verif_elementaire(2,'haut'),self.Verif_elementaire(3,'haut')],
                            [self.Verif_elementaire(0,'bas'),self.Verif_elementaire(1,'bas'),self.Verif_elementaire(2,'bas'),self.Verif_elementaire(3,'bas')],
                            [self.Verif_elementaire(0,'droite'),self.Verif_elementaire(1,'droite'),self.Verif_elementaire(2,'droite'),self.Verif_elementaire(3,'droite')],
                            [self.Verif_elementaire(0,'gauche'),self.Verif_elementaire(1,'gauche'),self.Verif_elementaire(2,'gauche'),self.Verif_elementaire(3,'gauche')]])
        self.v = np.array([np.any(self.V[0,:]),np.any(self.V[1,:]),np.any(self.V[2,:]),np.any(self.V[3,:])])
        if np.array_equal(self.v,np.array([False,False,False,False])):
            self.FAIL=True
            self.High_value = np.amax(self.matrix)
            if self.High_value >= 2048: self.WIN = True
        
    
    
    def remplissage(self,A):
        """Rajoute dans une case vide choisie aleatoirement
            soit un 2 (9 chances sur 10) soit un 4 (1 chance sur 10)"""
        avail = np.isin(A,0)#on cherche les cases vides
        if avail[avail==True].size > 0:
            new_tiles = np.append(np.random.choice([2]*9+[4]),np.zeros(avail[avail==True].size - 1) + 0)# on choisit un chiffre entre 2 et 4 au hasard et pour les autres on les remplit par la vide 
            np.random.shuffle(new_tiles) # permutation
            A[avail] = new_tiles #mettre les nouvelles cases dans la matrice
        return A

    
    def deplacement(self, pos_init, pos_fin):
        """Déplace un élément de la case "pos_init" à la case "pos_fin"
            pos_init différent de pos_fin, attention!
            pas de valeur de retour, modifie directement la rangée"""
        self.rangee[pos_fin] = self.rangee[pos_init]
        self.rangee[pos_init] = 0
    
    
    def fusion(self, pos_init, pos_fin):
        """Fusionne la case "pos_init" avec la case "pos_fin"  
            pos_init différent de pos_fin, attention!
            pas de valeur de retour, modifie directement la rangée"""
        self.rangee[pos_fin] *= -2 # marquage en mettant un signe -
        self.rangee[pos_init] = 0
        self.score -= self.rangee[pos_fin] # soustraction car valeur négative
        self.step_score = -self.rangee[pos_fin]
    
    def mouv_case(self, pos_init, gap=0):
        """Fonction récursive, envoie l'élément de la case "pos_init" où il doit aller
            paramètres:   pos_init (de 0 à 2, pas 3, attention!)
                          gap : intervient lors de la récursivité, augmente de 1 à chaque appel,
                                  correpond au nombre de cases vides trouvées après la case "pos_init"
            pas de valeur de retour, modifie directement la rangée"""
        pos_fin = pos_init + gap + 1
        if pos_fin == 4 :
            self.deplacement(pos_init, pos_fin - 1) # arrive lorsque les cases suivantes sont toutes vides
        elif self.rangee[pos_fin] == 0:
            self.mouv_case(pos_init, gap=gap+1) # récursivité
        elif self.rangee[pos_fin] == self.rangee[pos_init] :
            self.fusion(pos_init, pos_fin)
        elif gap != 0 :
            self.deplacement(pos_init, pos_fin - 1) # une case nous bloque, mais il y avait une case vide avant
    
    def mouvement(self, verif, M , verbose=False):
        """Effectue l'intégralité du mouvement demandé
            verif : matrice contenant un True sur la direction demandée"""
        direction = np.argwhere(verif)[0][0]
        numero_list = np.ravel(np.argwhere(self.V[direction]))
        for numero in numero_list:
            # extraction de la rangee dans le bon sens
            if direction == 0 : self.rangee = M[::-1, numero]
            elif direction == 1 : self.rangee = M[:,numero]
            elif direction == 2 : self.rangee = M[numero,:]
            else : self.rangee = M[numero,::-1]
            
            if verbose : print(self.rangee, end=' -> ')
    
            for i in [2,1,0]: self.mouv_case(i) # modification de la rangee (modifie directement la matrice en même temps)
                
            if verbose : print(self.rangee, '\n')
        return np.absolute(M)

    # Function to execute one action in reinforcement learning
    def one_step(self, action):
        assert action==0 or action==1 or action==2 or action==3, "Action should be number from list [0,1,2,3]"
        # down
        if action == 0:
            move = np.array([False,True,False,False])
        # left
        elif action == 1:
            move = np.array([False,False,False,True])
        # up
        elif action == 2:
            move = np.array([True,False,False,False])
        # right
        else:
            move = np.array([False,False,True,False])
        
        self.tour(move)
        
    # Verify if one action is possible
    def verif_action(self, action):
        if action == 0:
            user_input = np.array([False,True,False,False])
        elif action == 1:
            user_input = np.array([False,False,False,True])
        elif action == 2:    
            user_input = np.array([True,False,False,False])
        else:
            user_input = np.array([False,False,True,False])
        verif = self.Verif_mouv(user_input)
        if np.array_equal(verif,np.array([False,False,False,False])):
            return False
        else:
            return True
        
#M = _2048()