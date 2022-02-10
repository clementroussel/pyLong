class Group:
    counter = -1
    
    def __init__(self) :
        Group.counter += 1
        
        self.active = True
        
        self.title = ""
        
        self.annotations = []
        
    def __del__(self) :
        Group.counter -= 1
