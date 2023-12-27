import ipywidgets as widgets
from datetime import date
from aw_ya_core.EventControler import EventControler
# from qt_config.ChangeListner import ChangeListner
from aw_ya_core.observation import Observer

class EventSelector(Observer):
#指定されたイベント群を表示。
#どのカテゴリに分類されているのかを色で識別可能に

    def __init__(self, vdef):
        self.vdef = vdef
        self.widget = None
        self.events_widget = None
        self.h_parenthesis ="【"
        self.t_parenthesis ="】"
        #各種表示デフォルト値を定義する
        #表示するデータを準備する
        self._initialize_data()
        
        eventSelector_layout = widgets.Layout(border='3px solid green')
        self.widget = widgets.VBox([],layout=eventSelector_layout)
        
        children = self._initialize_widget()
        self.widget.children = children
        
    def _initialize_data(self):
        self.cache_kind = "longest"
        self.date = date.today()
        self.controler = EventControler(self.vdef)
        self._setup_data(self.date, self.cache_kind)
        self.controler.addCategoryObserver(self)
        self.controler.addViewObserver(self)
        self.controler.addCategoryContentsObserver(self)
        
    def _setup_data(self, date_d, kind):
        self.controler.load_events(date_d, kind)
        self.item_length = self.controler.get_item_length()
        ret = self.controler.get_head_items()
        self.items = ret[0]
        self.head_p = ret[1]
        self.tail_p = ret[2]
#        self.categories = self.controler.get_category_data()

                
    def _initialize_widget(self):
        self.categories = self.controler.get_category_data()
        ## ヘッダ部のウィジェットの生成 ##
        cache_selector = widgets.Select(
                                    options=[(_('Longest events'),'longest'), (_('latest events'),'latest')],
                                    value='longest',
                                    disabled=False,
                                    rows=1,
                                    layout=widgets.Layout(width='200px')
                                    )
        self.cache_selector = cache_selector
        
        date_picker = widgets.DatePicker(value=date.today(), layout=widgets.Layout(width='160px'))  
        self.date_picker = date_picker
        
        update_button = widgets.Button(description = _("Reload"),layout=widgets.Layout(width='80px'))
        #更新ボタンのコールバック設定
        update_button.on_click(self.updateData)
        
        condition_board = widgets.HBox([cache_selector,date_picker, update_button])
        
        
        left_arrow = widgets.Button(description ='<',layout = widgets.Layout(width = '25pt'))
        self.left_arrow = left_arrow

        indicator_layout = widgets.Layout(display='flex',
                                    flex_flow='row',
                                    justify_content='center')
        indicator_label = widgets.Label(layout = indicator_layout)
        self.indicator_label = indicator_label
        
        right_arrow = widgets.Button(description ='>',layout = widgets.Layout(width = '25pt'))
        self.right_arrow = right_arrow
        
        #left_arrowとright_arrowのイベントコールバック
        left_arrow.on_click(self.prevData)
        right_arrow.on_click(self.nextData)
        
        operational_board = widgets.HBox([left_arrow, indicator_label,  right_arrow])
               
        header_layout = widgets.Layout(display='flex',
                                    flex_flow='row',
                                    justify_content='space-between')
        header = widgets.HBox([operational_board , condition_board],layout=header_layout)


        ## イベント表示部分の生成 ## 
        events_layout = widgets.Layout(
            overflow='auto',
            border='1px solid black',
            height='300px',
            flex_flow='column',
            display='flex'
        )
        events_widget = widgets.VBox([], layout=events_layout)
        self.events_widget = events_widget

        
        ## フッター部のボタンを生成　##
        bulk_of_buttons = widgets.HBox([])
        self.bulk_of_buttons = bulk_of_buttons
        clear_button = widgets.Button(description =_('Cancel'))
        clear_button.on_click(self.clear_category)
        footer_layout = widgets.Layout(
                                    display='flex',
                                    flex_flow='row',
                                    justify_content='space-between',
                                    align_items='center', 
                                    height = '40pt'
        )
        footer = widgets.HBox([bulk_of_buttons,clear_button], layout=footer_layout)

        ##  データとの紐付け　##
        self._set_view_data()
 
        return [header,events_widget,footer]
        ##　全体をレイアウト　##
#        eventSelector_layout = widgets.Layout(border='3px solid green')
#        self.widget = widgets.VBox([header,events_widget,footer],layout=eventSelector_layout)


    def _set_view_data(self):
        ## ヘッダ部分のデータとの紐付け ##
        from_to_str =_(' - ')
        self.indicator_label.value = f"{self.head_p+1}{from_to_str}{self.tail_p+1}/{self.item_length}"
        if self.head_p == 0:
            self.left_arrow.disabled=True
        else:
            self.left_arrow.disabled=False
        if self.tail_p == self.item_length-1:
            self.right_arrow.disabled=True
        else:
            self.right_arrow.disabled=False 
        
        ##　イベント表示部分とデータの紐付け ##
        self.events_dict ={
            widgets.Checkbox(
                # description=f"{self.h_parenthesis if x[5] else None}{x[0]}:{x[1]}{self.t_parenthesis if x[5] else None}",
                description=f"{x[0]} : {x[1]}",         
                value=False,
                layout = widgets.Layout(width ='100%',
                                        border = '2px solid red' if x[5] else None
                                       ),
                style={"background":x[2]}
            ) : x for x in self.items
        }
        events = [x for x in self.events_dict.keys()]                
        self.events_widget.children = events      
#        print(self.categories)
        ##　フッダーボタンとデータの紐付け ##       
        self.categories_dict ={
            widgets.Button(
                description=x[1],
                style={"button_color":x[2]}
            ) :x for x in self.categories
        }
        cat_buttons = [x for x in self.categories_dict.keys()]
        for cb in self.categories_dict.keys():
            cb.on_click(self.categorize)
        self.bulk_of_buttons.children = cat_buttons


    def _set_event_view(self):
        ##　イベント表示部分とデータの紐付け ##
        # イベント登録、解除時に呼ばれる
        self.events_dict ={
            widgets.Checkbox(
                # description=f"{self.h_parenthesis if x[5] else None}{x[0]}:{x[1]}{self.t_parenthesis if x[5] else None}",
                description=f"{x[0]} : {x[1]}",         
                value=False,
                layout = widgets.Layout(width ='100%',
                                        border = '2px solid red' if x[5] else None
                                       ),
                style={"background":x[2]}
            ) : x for x in self.items
        }
        events = [x for x in self.events_dict.keys()]                
        self.events_widget.children = events

# Observerとしての関数をOverride

    def notifyViewChange(self, view):
 #       with open("debug.txt", "a") as o:
 #           print(f"-> EventSelector notifyViewChange from {view}",file=o)
        self.controler.deleteCategoryObserver(self)
        self._initialize_data()
        children = self._initialize_widget()
        self.widget.children = children
        self.controler.addCategoryObserver(self)
        ret = self.controler.get_current_items()
        self.items = ret[0]
        self._set_event_view()

    def notifyCategoryChange(self,category):
#        with open("debug.txt", "a") as o:
#            print(f"-> EventSelector notifyCategoryChange from {category}",file=o)
#        print(f"CategoryChange notified")
#        self.controler.deleteCategoryObserver(self)
        self._initialize_data()
        children = self._initialize_widget()
        self.widget.children = children
#        self.controler.addCategoryObserver(self)
        ret = self.controler.get_current_items()
        self.items = ret[0]
        self._set_event_view()
 
    def notifyCategoryContentsChange(self,category):
#        with open("debug.txt", "a") as o:
#            print(f"-> EventSelector notifyCategoryContentsChange from {category}",file=o)       
        ret = self.controler.get_current_items()
        self.items = ret[0]
        self._set_event_view()   
        
#コールバック関数

    def updateData(self, x):
        self._setup_data(self.date_picker.value, self.cache_selector.value)
        self._set_view_data()

    def prevData(self, x) :
        ret = self.controler.get_prev_items()
        self.items = ret[0]
        self.head_p = ret[1]
        self.tail_p = ret[2]
        self._set_view_data()
        
    def nextData(self, x):
        ret = self.controler.get_next_items()
        self.items = ret[0]
        self.head_p = ret[1]
        self.tail_p = ret[2]
        self._set_view_data()
        
    def categorize(self, x):
        cid = self.categories_dict[x][0]
        target_elist = [ cb for cb in self.events_widget.children if cb.value == True ]
        if len(target_elist)>0:
            #コントローラへ通知し、表示を変更
            for cb in target_elist:
                item = self.events_dict[cb]
                self.controler.set_defined_event(cid, [item[0],item[1]])
            cdef = self.controler.get_category_definition(self.categories_dict[x][0])
            cdef.commitChange(self)
        ret = self.controler.get_current_items()
        self.items = ret[0]
        self._set_event_view()        
                
                    
    def clear_category(self,x):
        target_elist = [ cb for cb in self.events_widget.children if cb.value == True ]
        if len(target_elist)>0:
            for cb in target_elist:
                item = self.events_dict[cb]
                if item[5]:
                    self.controler.cancel_defined_event(item[4], item[5])
            #ここにコミット文を入れる
        ret = self.controler.get_current_items()
        self.items = ret[0]
        self._set_event_view()                    