from aw_ya_view.SinglePieChart import SinglePieChart
from aw_ya_view.SunburstGraph import SunburstGraph
from aw_ya_core.lib import dprint

class PieChart:
    
    def __init__(self, parent):
        dprint(f"{self} : initialize")
        self.parent = parent
        self.graph = None
        

    def createView(self, canvas):
        dprint(f"{self} : createView")
        categorize1 = self.parent.selected_views[0]
        categorize2 = self.parent.selected_views[1]
        if not categorize1:
            if not categorize2:
                return 
            else:
                self.graph = SinglePieChart(self.parent, categorize2)
                self.graph.createView(canvas)
        else:
            if not categorize2:
                dprint(f"{categorize1}:{categorize2}")
                self.graph = SinglePieChart(self.parent,categorize1)
                self.graph.createView(canvas)
            else:
                self.graph = SunburstGraph(self.parent)             
                self.graph.createView(canvas)
                
                    