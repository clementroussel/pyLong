class Annotation :
    """ 
    --> définition de l'objet Annotation <-- 
    """
    compteur = 0
    
    def __init__(self) :
        Annotation.compteur += 1
    
        self.actif = True
        
        self.groupe = 0
        
        self.opacite = 1.
        
        self.ordre = 1
        
    def __del__(self) :
        Annotation.compteur -= 1