import sys
import ipywidgets as widgets
from IPython.display import display

class EditorPanel:
    #ビルダの基底クラス    
    def __init__(self, defmodel):
        self.defmodel = defmodel
#        self._initialize_widget()
        
    def _initialize_widget(self):
        property_editor = PropertyEditor()        
        item_list_editor = ItemListEditor(self, property_editor)
        self.item_list_editor = item_list_editor

        editor_pair = widgets.HBox([item_list_editor.widget, property_editor.out])

        self.widget = widgets.Accordion(children=[editor_pair], 
                                        titles=([f"{self.str}定義の追加・削除・編集"]))

    def setData(self, items):
        self.item_list_editor.setData(items)
        
    def commit_change(self): 
        self.defmodel.commitChange(self)
        
class ViewBuilder(EditorPanel):
    
    def __init__(self, defmodel):
        super().__init__(defmodel)
        self.items = defmodel.views
        self.str = "ビュー"
        super()._initialize_widget()
        self.setData(self.items)
        
    def add_item(self,  name, color):
        self.defmodel.addView(name,color,False)
        self.setData(self.items)
        #ADEに通知
        
    def update_item(self, item, name, color):
        self.defmodel.updateView(item.id, name, color,False)
        self.setData(self.items)
        #AnalisisyViewPanelに通知
        
    def delete_item(self, item):
        self.defmodel.deleteView(item.id)
        self.setData(self.items)
        #ADEに通知        

        
class CategoryBuilder(EditorPanel):

    def __init__(self, defmodel):
        super().__init__(defmodel)
        self.items = defmodel.categories
        self.str = "カテゴリー"
        super()._initialize_widget()
        self.setData(self.items)
        
    def add_item(self, name, color):
        self.defmodel.addCategory(name,color)
        self.setData(self.items)
        #AnalisisViewPanelに通知
        
    def update_item(self, item, name, color):
        self.defmodel.updateCategory(item.id, name, color)
        self.setData(self.items)
        #CategoryPanelに通知
        
    def delete_item(self, item):
        self.defmodel.deleteCategory(item.id)
        self.setData(self.items)
        #AnalisisViewPanelに通知              
        
        
        
class PropertyEditor:   
    
    # アイテムの属性を定義するエディター
    # ポップアップ風に動的に表示・非表示が可能

    def __init__(self):
        self.caller = None
        self.name = "Blank"
        self.color = "white"
        self._initialize_widget()
        
    def _initialize_widget(self):
        self.name_text = widgets.Text(
                            value = self.name,
                            description='Label Strings:')

        self.color_picker = widgets.ColorPicker(
                            concise=False,
                            description='Color:',
                            value=self.color)
        save_button = widgets.Button(
                            description ='Save',
                            layout = widgets.Layout(width = '45pt') )
    
        save_button.on_click(self._closeEditPanel)
    
        save_button_panel = widgets.HBox(
                            [save_button],
                            layout=widgets.Layout(display='flex', flex_flow='row',
                                                justify_content='center'))

        self.widget = widgets.VBox([self.name_text, self.color_picker,save_button_panel],
                            layout=widgets.Layout(border='1px solid black', 
                                                display='flex', flex_flow='colomun',
                                                justify_content='center'))
        # 動的に表示・非表示を切り替えるためにOutputウィジェットを作る
        self.out = widgets.Output()

    def showEditPanel(self, caller):
        self.caller = caller
        self.name_text.value = caller.name
        self.color_picker.value = caller.color
        # Outputウイジェットをクリア
        self.out.clear_output()
        # Outputウイジェットの上にエディタを表示
        with self.out:
            display(self.widget)


    def _closeEditPanel(self, x):
#        print(f"{self} setProperties to {self.caller}")
        self.caller.setProperties(self.name_text.value, self.color_picker.value)
        self.caller.my_parent.unlock()
        #Outputウイジェットをクリアし、エディタを消去
        self.out.clear_output()        
        
        
class ItemListEditor:
    #　アイテム（ビューやカテゴリー）を編集するエディタ
    
    def __init__(self, builder, p_editor):
        self.builder = builder
        self.property_editor = p_editor
        widget_list = []
        widget_list_box =widgets.VBox(widget_list, layout=widgets.Layout(border='1px solid black'))
        self.widget_list_box = widget_list_box
        add_button = widgets.Button(description ='アイテムの追加',
                               layout = widgets.Layout(width = '100pt'),
                                style = {"text_color":"white", "font_weight":"bold", "button_color":"gray"}
                                )
        add_button.on_click(self.addItem)
        self.widget = widgets.VBox([widget_list_box,add_button])
        
    def setData(self, items):
        self.item_dict ={
#            ItemRowWidget(x.name, x.color, self) :x for x in items
            ItemRowWidget(x, self) :x for x in items
        }
        self.widget_list_box.children = [x.widget for x in self.item_dict.keys()]
        
    def updateItem(self, w, name, color):
        self.builder.update_item(self.item_dict[w], name, color)
#        self.builder.commit_change()
        #item = self.item_dict[w]
        #item.name = w.name
        #item.color = w.color
        
    def removeItem(self, w):
        self.builder.delete_item(self.item_dict[w])
        self.builder.commit_change()
        # del self.item_dict[w]
        # self.widget_list_box.children = [x.widget for x in self.item_dict.keys()]
        
    def addItem(self, x):
        self.builder.add_item("not defined","lightgray")
        self.builder.commit_change()

    def lock(self):
        self.widget.children[1].disabled=True
        for x in self.widget.children[0].children:
            x.children[1].disabled=True
            x.children[2].disabled=True
            
    def unlock(self):
        self.widget.children[1].disabled=False
        for x in self.widget.children[0].children:
            x.children[1].disabled=False
            x.children[2].disabled=False        
        
class ItemRowWidget:
    
    def __init__(self, item, parent):
        self.item = item
        self.name = item.name
        self.color = item.color      
        self.editor = parent.property_editor
        self.my_parent = parent
        self.my_parent_widget = None      
        self._initialize_widget()


    def _initialize_widget(self):        
        self.name_label = widgets.Label(
                            value=self.name,
                            layout = widgets.Layout(width = '180pt'),
                            style={"background": self.color}
                            )
        self.remove_button = widgets.Button(description ='削除',
                                            disabled = False,
                                layout = widgets.Layout(width = '36pt'),
                                style = {"button_color":self.color,
                                    "text_color":"white"}
                                )
        self.remove_button.on_click(self._removeItem)
        self.edit_button = widgets.Button(description ='編集',
                                            disabled = False,
                                    layout = widgets.Layout(width = '36pt'),
                                    style = {"button_color":self.color,
                                        "text_color":"white"}
                                    )
        self.edit_button.on_click(self._showEditPanel)
        self.widget = widgets.HBox([self.name_label, self.remove_button, self.edit_button])

        
    def setProperties(self, name, color):
#        with open("debug.txt", "a") as o:
#            print(f"-> {self}'s setProperties called.",file=o)
#            print(f"-> commit to {self.item}",file=o)
        self.my_parent.updateItem(self,name,color)
        self.item.commitChange(self)
    
    def _showEditPanel(self, x):
        self.editor.showEditPanel(self)
        self.my_parent.lock()
        
    def _removeItem(self, x):
        self.my_parent.removeItem(self)
        
        