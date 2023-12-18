import ipywidgets as widgets
import re
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from .ChangeListner import ChangeListner
from aw_ya_core.observation import Observer

class WordRecomender:
    
    def __init__(self, cat):
        self.recomendations = []
        self.category = cat
        
    def createRecomendations(self):
        #選択されたイベント文字列から、キーワード候補となる文字列を抽出する。
        #イベント文字列の中で２回以上出現し、キーワード登録されていないものが候補
        token_filters = [CompoundNounFilter(),POSKeepFilter(['名詞'])]
        char_filters = [RegexReplaceCharFilter("\]|\[|\(|\)"," ")]
        a = Analyzer(char_filters=char_filters, token_filters=token_filters)       
        words = dict()
        for e in self.category.events:
            for token in a.analyze(f"{e[2]} {e[3]}"):
                word_str = token.surface
                if len(word_str) <= 1:
                    break
                if word_str in words:
                    words[token.surface] += 1
                else:
                    words[token.surface] = 1
        imlist = sorted(words.items(), key=lambda x:x[1], reverse=True)
        filtered_list = self._deliminateUsedWords(imlist)
        top_list = [x for x in filtered_list if x[1]>0]
        self.recomendations =self._addEventInformation(top_list) 
        
    def _deliminateUsedWords(self, wlist):
        #すでにキーワードとして登録されているものを外す
        defined_word_data = self.category.positive_words + self.category.negative_words
        used_word_list = [x[2] for x in defined_word_data]
        filtered_list = [item for item in wlist if item[0] not in used_word_list]
        #("ワード",出現数)を要素とするリストを返す
        return filtered_list
        
    def _addEventInformation(self, wlist):
        #キーワードが含まれる、イベントの情報を付加する
        wdlist = []
        for w in wlist:
            evlist = []
            for ev in self.category.events:
                if re.search(w[0],f"{ev[2]} {ev[3]}"):
                    evlist.append([ev[2],ev[3]])
            wdlist.append([w[0],w[1],evlist])
        return wdlist
            

def AdjastableCheckbox(name,color):
    #文字長に応じて幅を調整するチェックボックス
    f_size =12
    wn = len(name)
    str_width = wn*f_size
    acb = widgets.Checkbox(
                description=name, 
                value=False,
                disabled=False,
                indent=False,
                layout = widgets.Layout(width=f"{str_width+30}px"),
                style={"background":color}
            ) 
    return acb


class WordInfo:
    #候補となるキーワードに関する情報を表示するウィジェット
    def __init__(self,w_data):
        #w_data ['word', 出現回数, [['app','title'],イベント２,...]]
        self.word = w_data[0]
        self.times = w_data[1]
        self.events = w_data[2]
        self._initialize_widget()
        
    def _initialize_widget(self):
        cb = widgets.Checkbox(description=self.word, value=False, indent=False,
                                      layout = widgets.Layout(width="20%"))
        event_labels = [widgets.Label(value=x[0]+':'+x[1]) for x in self.events]
        event_bx = widgets.VBox(event_labels)
        ac = widgets.Accordion(children=[event_bx],titles=["イベント表示"])
        
        self.widget = widgets.HBox([cb, ac],layout=widgets.Layout(border='1px solid black'))
        
class CategoryEditor(Observer):
    #該当するカテゴリーの設定を行う画面    
    def __init__(self, cd):
        self.catd = cd
        self.name = cd.name
        self.wr = WordRecomender(self.catd)
        self._initialize_widget()
        self._set_view_data()
        self.catd.addObserver(self)
        
    def _initialize_widget(self):
        box_layout = widgets.Layout(display='flex',
                                    flex_flow='row',
                                    justify_content='center',
                                    align_items='center',
                                    width='100%',
                                    height ='32pt')  
        name_label = widgets.Label(value = self.name,layout=box_layout,style={"background":self.catd.color,"font_size":"16pt"})
        self.name_label = name_label
        self.events_box = widgets.VBox([])
        events_viewer = widgets.Accordion(children=[self.events_box],titles=["登録されたイベント"])        
        self.events_viewer = events_viewer
        
        blank = widgets.Label(value=None,layout=widgets.Layout(height='10pt'))
        
        positive_items =[]
        negative_items =[]       
        box_layout = widgets.Layout(display='flex',flex_flow='row wrap',justify_content='flex-start')
        positive_box = widgets.HBox(positive_items, layout=box_layout)
        self.positive_box =positive_box
        negative_box = widgets.HBox(negative_items, layout=box_layout)
        self.negative_box = negative_box
        words_box = widgets.VBox([positive_box,negative_box],layout=widgets.Layout(border='3px solid green'))
        
        
        include_arrow = widgets.Button(description ='▲ 含む',
                                       layout = widgets.Layout(width = '70pt'),
                                       style = {"button_color":self.catd.color, "text_color":"white", "font_weight":"bold"})
        include_arrow.on_click(self.register_positive_words)
        self.include_arrow = include_arrow
        
        not_include_arrow = widgets.Button(description ='▲ 含まない',
                                           layout = widgets.Layout(width = '70pt'),
                                            style = {"text_color":"black", "font_weight":"bold"}) 
        not_include_arrow.on_click(self.register_negative_words)
        
        moveup_buttons = widgets.HBox([include_arrow,not_include_arrow])
        
        cancel_button = widgets.Button(description ='▼ 解除',
                                           layout = widgets.Layout(width = '65pt'),
                                            style = {"text_color":"black", "font_weight":"bold"})   
        cancel_button.on_click(self.cancel_words)
        
        arrow_box_layout = widgets.Layout(display='flex',
                                    flex_flow='row',
                                    justify_content='space-between',
                                    align_items='center',
                                    width='100%',
                                    height ='32pt')  
        arrow_box = widgets.HBox([moveup_buttons,cancel_button],layout=arrow_box_layout)
        text_input = widgets.Text(layout = widgets.Layout(width = '300pt',border='1px solid black'))

        self.text_input = text_input
        input_box = widgets.HBox([widgets.Label(value="キーワード登録"),text_input])
        word_infos = []

        candidate_box = widgets.VBox(word_infos,layout=widgets.Layout(border='2px solid green'))        
        self.candidate_box = candidate_box
#        self.widget = widgets.VBox([name_label, events_viewer, blank, words_box, arrow_box, input_box,candidate_box])
        self.widget = widgets.VBox([events_viewer, blank, words_box, arrow_box, input_box,candidate_box])        
 
    def _set_view_data(self):
        #CategoryDefinitionから元の情報を取得
        self.name_label.value = self.catd.name
        self.name_label.style = {"background":self.catd.color,"font_size":"16pt"}
        self.include_arrow.style = {"button_color":self.catd.color, "text_color":"white", "font_weight":"bold"}
        ev_str_list =[f"{ev[2]}:{ev[3]}" for ev in self.catd.events]
        event_labels = [widgets.Label(value = x,style = {"text_color":"black"}) for x in ev_str_list]       
        self.events_box.children = event_labels
        self._set_word_view_data()
    
    def _set_word_view_data(self):
        #キーワード関連の情報をCategoryDefinitionとWordRecomenderから取得
        positive_words_dict = {
            AdjastableCheckbox(w[2],self.catd.color): w for w in self.catd.positive_words
        }
        self.positive_box.children = [x for x in positive_words_dict.keys()]
        self.positive_words_dict = positive_words_dict
        
        negative_words_dict = {
            AdjastableCheckbox(w[2],"lightgray"): w for w in self.catd.negative_words
        }
        self.negative_box.children = [x for x in negative_words_dict.keys()]
        self.negative_words_dict = negative_words_dict        
        
        self.wr.createRecomendations()
        word_infos =[ WordInfo(w_data).widget for w_data in self.wr.recomendations]
        self.candidate_box.children = word_infos  
        
        self.text_input.value = ""

    #リスナー呼び出し
    def notifyTopChange(self, defmodel):
        pass
        
    def notifyViewChange(self, view):
        pass
        
    def notifyCategoryChange(self, category):
#        print(f"{self} notified categoryChange ")
#        self.name_label.value = self.catd.name
#        self.name_label.style = {"background":self.catd.color,"font_size":"16pt"}
#        print(self.catd.name)
        self._set_view_data()        

    #コールバック関数

    def register_positive_words(self,x):
        self._register_words(True)                
    
    def register_negative_words(self,x):
        self._register_words(False)

    def _register_words(self, kind):
        w_list = []
        word = self.text_input.value
        if not word == "":
            defined_word_data = self.catd.positive_words + self.catd.negative_words
            used_word_list = [x[2] for x in defined_word_data]
            if word in used_word_list:
                print(f"->{word} already has been in the list.")
            else:
                w_list.append(word)                
        for w_info in self.candidate_box.children:
            wcb = w_info.children[0]
            if wcb.value:
                w_list.append(wcb.description)
        for w in w_list:
            self.catd.addWord(self.catd.id, w, kind)
        self._set_word_view_data()
        self.catd.proxy.commitChange(self)
    
    def cancel_words(self,x):
        for cb in self.positive_box.children:
            if cb.value:
                self.catd.deleteWord(self.positive_words_dict[cb][0],True)
        for cb in self.negative_box.children:
            if cb.value:
                self.catd.deleteWord(self.negative_words_dict[cb][0],False)
        self.catd.proxy.commitChange(self)        
        self._set_word_view_data()