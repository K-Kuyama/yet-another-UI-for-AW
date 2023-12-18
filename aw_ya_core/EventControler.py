from .EventCache import EventCache
import re
from _ast import Break
# from pandas.tests.io.excel.test_odf import cd_and_set_engine
# from pip._vendor.pygments.formatters.html import ctags
from aw_ya_core.lib import dprint


class EventControler:
    
    def __init__(self, view_def):
        self.ecache = EventCache()
        
        self.max_displayed = 20
        self.vdef = view_def

    def load_events(self, day, kind):
        self.ecache.load_events(day,kind)
        
    def get_item_length(self):
        return self.ecache.length
    
    def get_head_items(self):
        # items["app","title","bg_color","str_color", cid, eid]
        ret = self.ecache.get_head_events(self.max_displayed)
        items = self._append_info(ret[0])
        return items, ret[1], ret[2] 
    
    def get_current_items(self):
        ret = self.ecache.get_current_events()
        items = self._append_info(ret[0])
        return items, ret[1], ret[2] 
    
    def get_prev_items(self):      
        ret = self.ecache.get_prev_events(self.max_displayed)
        items = None
        if not ret[0]==None:
            items = self._append_info(ret[0])
        return items, ret[1], ret[2]         
        
    def get_next_items(self):   
        ret = self.ecache.get_next_events(self.max_displayed)
        items = None
        if not ret[0]==None:
            items = self._append_info(ret[0])
        return items, ret[1], ret[2] 
    
    def _append_info(self, row_data):
        #イベントデータに設定色情報とカテゴリーidを付加する
        items =[]
        for ev in row_data:
            cols = self._get_colors(ev)
            items.append(
            [ev["data"]["app"],ev["data"]["title"],cols[0],cols[1],cols[2],cols[3]]
            )
        return items
    
    def _get_colors(self, ev):
        #含まれるwordや、カテゴリ固定のイベントとのマッチング情報から
        #チェックボックスへの設定色を取り出す。文字列色は固定イベントの場合白、それ以外は黒
        
        # デフォルト色をセット
        bg_color ="White"
        str_color = "Black"
        
        app_str = ev["data"]["app"]
        title_str = ev["data"]["title"]
        cid = None
        eid = None
        for c in self.vdef.categories:
            for ed in c.events:
                if ed[2]==app_str and ed[3]==title_str:
                    bg_color = c.color
                    str_color = "White"
                    cid = c.id
                    eid = ed[0]
                    return bg_color,str_color, cid, eid
                
        for c in self.vdef.categories:
            rgx =c.getRegex()
#            dprint(f"RGX : {rgx}")
            if rgx: 
                if re.search(rgx, app_str+title_str):
                    bg_color = c.color
                    cid = c.id
                    break
            else:
                cid = c.id
        return bg_color,str_color, cid, eid
    
        """
        for c in self.vdef.categories:
            for ed in c.events:
                if ed[2]==app_str and ed[3]==title_str:
                    bg_color = c.color
                    str_color = "White"
                    cid = c.id
                    eid = ed[0]
                    break
#            c.getRegex() 
            if re.search(c.getRegex(), app_str+title_str):
                bg_color = c.color
                cid = c.id
                break
        return bg_color,str_color, cid, eid
        """

    #イベントのカテゴリ設定解除時に解除後の表示色を調べるために呼ばれる。 
    def get_color(self,ev_pair):
#        dprint("----")
        bg_color ="White"
        for c in self.vdef.categories:
#            dprint(f"{c.name} regex {c.getRegex()}") 
            rgx = c.getRegex()
            if rgx:
                if re.search(c.getRegex(), ev_pair[0]+ev_pair[1]):
                    bg_color = c.color
                    break
        return bg_color
        
    def set_defined_event(self, cid, ev_data):
        clist = [c for c in self.vdef.categories if c.id==cid]
        if len(clist)==1:
            return clist[0].addEvent(ev_data) 
        else :
            return False
        
        
    def cancel_defined_event(self, cid, eid):
        clist = [c for c in self.vdef.categories if c.id==cid]
        if len(clist)==1:
            clist[0].deleteEvent(eid) 
        else :
            return False        

    def get_category_data(self):
        clist = [[c.id,c.name,c.color] for c in self.vdef.categories]
        return clist

    def get_category_definition(self, cid):
        for c in self.vdef.categories:
            if c.id == cid:
                return c
        return False

#EventSelectorの代理でオブザーバーとして登録    
    def addCategoryObserver(self,obj):
#        with open("debug.txt", "a") as o:
#            print(f"add observer -> {self.vdef.categories}",file=o)
        for cd in self.vdef.categories:
            cd.addObserver(obj)
            
    def deleteCategoryObserver(self, obj):
        for cd in self.vdef.categories:
            cd.deleteObserver(obj)      
            
    def addViewObserver(self, obj):
        self.vdef.addObserver(obj)
        
    def deleteViewObserver(self, obj):
        self.vdef.deleteObserver(obj)
        
    def addCategoryContentsObserver(self, obj):
        for cd in self.vdef.categories:
            cd.proxy.addObserver(obj)
 
    def deleteCategoryContentsObserver(self, obj):
        for cd in self.vdef.categories:
            cd.proxy.deleteObserver(obj)              