from abc import abstractclassmethod, ABC

class ChangeListner(ABC):
        
    @abstractclassmethod        
    def notifyTopChange(self, defmodel):
        pass
        
    @abstractclassmethod
    def notifyViewChange(self, view):
        pass
        
    @abstractclassmethod
    def notifyCategoryChange(self, category):
        pass
    