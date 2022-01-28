class Group:
    counter = -1
    
    def __init__(self) :
        Group.counter += 1
        
        self.active = True
        
        self.title = "group {}".format(Group.counter)
        
        self.annotations = []
        
    def __del__(self) :
        Group.counter -= 1
