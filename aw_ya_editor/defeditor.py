import ipywidgets as widgets
from aw_ya_editor.EventSelector import EventSelector
from aw_ya_core.defmodel import AnalysisDefinition
from aw_ya_editor.itembuilder import ViewBuilder, CategoryBuilder
from aw_ya_editor.categoryeditor import CategoryEditor
from aw_ya_core.observation import Observer

class AnalysisDefEditor(Observer):
    
    def __init__(self):
        self.ad = AnalysisDefinition()
        self.ad.loadData()
        self._initialize_widget()
        self.ad.addObserver(self)

        
    def _initialize_widget(self):
        self.view_builder = ViewBuilder(self.ad)
        self.view_panels =[]
        self.vtab = self._initialize_vtab()
        self.widget = widgets.VBox([self.view_builder.widget, self.vtab])

    def _initialize_vtab(self):
        vtab = widgets.Tab()
        titles = []
        for vp in self.view_panels:
            vp.vdef.deleteObserver(vp)
        self.view_panels = []
        for vd in self.ad.views:
            self.view_panels.append(AnalysisViewPanel(vd))
            titles.append(vd.name)
            vd.addObserver(self)           
        vtab.children = [vp.widget for vp in self.view_panels]
        vtab.titles = titles
        self.vtab = vtab
        return vtab
        
    def notifyTopChange(self, defmodel):
        self.vtab = self._initialize_vtab()
        self.widget.children=[self.view_builder.widget, self.vtab]
        
    def notifyViewChange(self, view):
        titles = [v.name for v in self.ad.views]
        index = self.vtab.selected_index
        self.vtab.titles = titles
        self.vtab.selected_index = index
        

        
class AnalysisViewPanel(Observer):
    
    def __init__(self, vd):
        self.vdef = vd
        self.widget = widgets.VBox([])
        self._set_widgets()
        self.vdef.addObserver(self)
        
        
    def _set_widgets(self):
        box_layout = widgets.Layout(display='flex',
                                    flex_flow='row',
                                    justify_content='center',
                                    align_items='center',
                                    width='100%',
                                    height ='24pt')  
#        self.title_label = widgets.Label(value = self.vdef.name,
#                        layout = box_layout,
#                        style={"background":self.vdef.color,"font_size":"18pt"}
#                     )
        self.es = EventSelector(self.vdef)
        blank_panel = widgets.Label(layout=widgets.Layout(height='24pt'))
        self.category_builder = CategoryBuilder(self.vdef)
        self.category_panels = []
        self.ctab = self._initialize_ctab()
#        self.widget.children = [self.title_label, self.es.widget, blank_panel, self.category_builder.widget, self.ctab]
        self.widget.children = [self.es.widget, blank_panel, self.category_builder.widget, self.ctab]       

    def _initialize_ctab(self):
        ctab = widgets.Tab()
        titles = []
        for cp in self.category_panels:
            cp.catd.deleteObserver(cp)
        self.category_panels = []
        for cd in self.vdef.categories:
            self.category_panels.append(CategoryEditor(cd))
            titles.append(cd.name)
            cd.addObserver(self)
        ctab.children = [ce.widget for ce in self.category_panels]
        ctab.titles = titles
        return ctab

    def __delete__(self):
        print(f"{self} deleted")
    
        
    def notifyViewChange(self, view):
        self.ctab = self._initialize_ctab()
#        self.widget.children = [self.title_label, self.es.widget, self.category_builder.widget, self.ctab]
        self.widget.children = [self.es.widget, self.category_builder.widget, self.ctab]
        
    def notifyCategoryChange(self, category):      
        titles = [v.name for v in self.vdef.categories]
        index = self.ctab.selected_index
        self.ctab.titles = titles
        self.ctab.selected_index = index