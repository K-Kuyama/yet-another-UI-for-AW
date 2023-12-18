class Observer:
              
    def notifyTopChange(self, defmodel):
        pass
        
    def notifyViewChange(self, view):
        pass
        
    def notifyCategoryChange(self, category):
        pass

    def notifyCategoryContentsChange(self,category):
        pass
    
class Observable:
    
    def __init__(self):
#        print(f"initializing change reporter {self}")
        self.observers =set()
        
    def addObserver(self, obj):
#        print(f"listner {self} append {obj}")
        if obj not in self.observers:
            self.observers.add(obj)
#        print(f"Listners are {self.listners}")        
        
    def deleteObserver(self, obj):
        self.observers.discard(obj)
        
    def commitChange(self,source):
#        print(f"by commited from{source}: {self} notify to {self.listners}")
        for obj in self.observers:
            if not obj == source:
#                print(f"{self} notify to {obj}")
                self._notify(obj)
    
    def _notify(self,obj):
        # need to override
        pass