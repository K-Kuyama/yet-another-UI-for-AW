import ipywidgets as widgets
from aw_ya_core.defmodel import AnalysisDefinition
from aw_ya_core.lib import dprint
import aw_client
import matplotlib.pyplot as plt
from datetime import date
import cProfile
import gc


class Dashboard:
    
    def __init__(self):
        self.awc = aw_client.ActivityWatchClient("qt_ovserver")
        self.avdef = AnalysisDefinition()
        self.avdef.loadData()
        self._init_widget()
      
        plt.rcParams['font.family'] = "Hiragino Sans"
        plt.rcParams['font.size'] = 8.0
        self.fig = None
        self.rows = 2
        self.columns = 2
        self.selected_views =[]
        self.graphs = [] #[(Graphオブジェクト, index)....]
        self.date = None
        self.axis = None
    
    def _init_widget(self):
        view_options =[("",None)]
        view_options = view_options + [(v.name, v) for v in self.avdef.views]
            
#        selector_layout = widgets.Layout(border='3px solid green')
#        self.widget = widgets.HBox([],layout=selector_layout)
        self.widget = widgets.VBox([])
        view_selector1 = widgets.Select(
                                    options=view_options,
                                    value=None,
                                    disabled=False,
                                    rows=1,
                                    description="分類1",
                                    layout=widgets.Layout(width='300px')
                                    )
        self.selector1 = view_selector1
        view_selector2 = widgets.Select(
                                    options=view_options,
                                    value=None,
                                    disabled=False,
                                    rows=1,
                                    description="分類2",                                    
                                    layout=widgets.Layout(width='300px')
                                    )
        self.selector2 = view_selector2
        selector_box = widgets.VBox([view_selector1, view_selector2])

        date_picker = widgets.DatePicker(value=date.today(), layout=widgets.Layout(width='160px'))  
        self.date_picker = date_picker
        update_button = widgets.Button(description = "表示",layout=widgets.Layout(width='60px'))
        #更新ボタンのコールバック設定
        update_button.on_click(self.updateView)
#        selector_layout = widgets.Layout(border='3px solid green')
        datasets = widgets.HBox([selector_box, date_picker, update_button])
#        self.widget.children = [selector_box, date_picker, update_button]
        load_button = widgets.Button(description = "再読込み",layout=widgets.Layout(width='120px'))
        load_button.on_click(self.reload)
        panel_layout = widgets.Layout(display='flex',
                                    flex_flow='row',
                                    justify_content='space-between',
                                    align_items='center',
                                    border='3px solid green')
        panel = widgets.HBox([datasets, load_button],layout=panel_layout)
        self.out = widgets.Output()
        self.widget.children = [panel,self.out]
        
    def reload(self,x):
        self.avdef.reloadData()
        view_options =[("",None)]
        view_options = view_options + [(v.name, v) for v in self.avdef.views]
        self.selector1.options = view_options
        self.selector2.options = view_options
        
    def updateView(self,x):
        x.disabled=True
        dprint(f"start update {gc.get_stats()[2]}")
        self.selected_views = [self.selector1.value, self.selector2.value]
        self.date = self.date_picker.value
        dprint(f"selected {self.selected_views}")
        self.createViews()
#        cProfile.runctx('self.createViews()',globals(),locals(),filename='profile.txt')
        dprint(f"finish update {gc.get_stats()[2]}")
        x.disabled=False
        
    def setView(self,graph,index):
        self.graphs.append((graph,index))
 
    def _setFig(self):
        self.fig = plt.figure(figsize=(8,8))
        axis = dict()
        for graph in self.graphs:
            axis[graph[1]] = self.fig.add_subplot(self.rows, self.columns,graph[1])
            dprint(f"set axis {axis[graph[1]]}")
        self.axis = axis
        
    def _clearAll(self):
#       with self.out:
        dprint(f"clear {self.axis}")
        for ax in self.axis.values():
            ax.cla()
#            ax.text(0.5, 0.5, 'Now Loading...', horizontalalignment='center',verticalalignment='center')
#        plt.show()
        
    def createViews(self):
#        if self.fig == None:
#            self._setFig()
#        else:
#            self._clearAll()
        self.out.clear_output()
        self._setFig()
        for gr in self.graphs:
            gr[0].createView(self.axis[gr[1]])
        self.out.clear_output(wait=True)   
        with self.out:
            plt.show()
        
        