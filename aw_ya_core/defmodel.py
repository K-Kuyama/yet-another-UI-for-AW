from .datastore import DataStore
from .observation import Observable
import unicodedata
#from numpy.typing.tests.data import pass

"""
class changeReporter:
    def __init__(self):
#        print(f"initializing change reporter {self}")
        self.listners =[]
        
    def setListner(self, obj):
#        print(f"listner {self} append {obj}")
        self.listners.append(obj)
#        print(f"Listners are {self.listners}")        
        
    def commitChange(self,source):
#        print(f"by commited from{source}: {self} notify to {self.listners}")
        for obj in self.listners:
            if not obj == source:
#                print(f"{self} notify to {obj}")
                self._notify(obj)
    
    def _notify(self,obj):
        pass
"""

class AnalysisDefinition(Observable):
    
    def __init__(self):
        super().__init__()
        self.views = []

    def _notify(self,obj):
            obj.notifyTopChange(self)
        
    def loadData(self):
        query_str = f"SELECT * FROM {DataStore().views_table}"
        view_def_list = DataStore().query(query_str)
        for l in view_def_list:
            self.views.append(AnalysisViewDefinition(l))
            
    def reloadData(self):
        self.views = []
        self.loadData()

    def addView(self, name, color, use_def_color):
        x = 1 if use_def_color else 0
        query_str = f"INSERT into {DataStore().views_table} (name, color, use_def_color) values ('{name}','{color}',{x})"
        vid = DataStore().execute(query_str)
#        vid = ret
        self.views.append(AnalysisViewDefinition([vid, name, color, use_def_color]))
#        self._notify()
        return vid
        
    def updateView(self, vid, name, color, use_def_color):
        vlist = [v for v in self.views if v.id==vid]
        if len(vlist)==1:
            vlist[0].name = name
            vlist[0].color = color
            vlist[0].use_default_color = use_def_color
        else :
            return False
            
        x = 1 if use_def_color else 0
        query_str = f"UPDATE {DataStore().views_table} set name='{name}',color='{color}',use_def_color={x} where id={vid}"
        ret = DataStore().execute(query_str)
#        self._notify()
        return ret

    
    def deleteView(self, vid):
        vlist = [v for v in self.views if v.id==vid]
        if len(vlist)==1:
            view = vlist[0]
            view.deleteAll()
            self.views.remove(view)
        else:
            return False
        query_str = f"DELETE from {DataStore().views_table} where id={vid}"
#        query_str = f"""DELETE {DataStore().views_table},{DataStore().category_table},{DataStore().events_table},{DataStore().words_table}
#                                from {DataStore().views_table} LEFT JOIN {DataStore().category_table} ON {DataStore().views_table}.id = {DataStore().category_table}.view_id
#                                    LEFT JOIN {DataStore().events_table} ON {DataStore().category_table}.id = {DataStore().events_table}.category_id
#                                    LEFT JOIN {DataStore().words_table} ON {DataStore().category_table}.id = {DataStore().words_table}.vid
#                                where {DataStore().views_table}.id={vid}"""
        ret = DataStore().execute(query_str)
#        self._notify()
        return ret
            
class AnalysisViewDefinition(Observable):
    
    def __init__(self, v_list):
        super().__init__()
        self.id = v_list[0]
        self.name = v_list[1]
        self.color = v_list[2]
        self.use_default_color = True if v_list[3]==1 else False
        self.categories = []
        self._loadCategories()
        
    def _loadCategories(self):
        query_str =f"SELECT * FROM {DataStore().categories_table} WHERE view_id ={self.id}"
        def_list = DataStore().query(query_str)
        for l in def_list:
            self.categories.append(CategoryDefinition(l))

    def _notify(self, obj):
        obj.notifyViewChange(self)       
            
    def addCategory(self, name, color):
        query_str = f"INSERT into {DataStore().categories_table} (view_id, name, color) values ({self.id},'{name}','{color}')"
        cid = DataStore().execute(query_str)
#        cid = ret
        self.categories.append(CategoryDefinition([cid, self.id, name, color]))
#        self._notify()
        return cid        

        
    def updateCategory(self, cid, name, color):
        clist = [c for c in self.categories if c.id==cid]
        if len(clist)==1:
            clist[0].name = name
            clist[0].color = color
        else :
            return False
            
        query_str = f"UPDATE {DataStore().categories_table} set name='{name}',color='{color}' where id={cid}"
        ret = DataStore().execute(query_str)
#        self._notify()
        return ret

    def deleteCategory(self, cid):
#        print(f"delete {cid}")
        clist = [c for c in self.categories if c.id==cid]
        if len(clist)==1:
            category = clist[0]
            category.deleteAll()
            self.categories.remove(category)
        else:
            return False

        query_str = f"DELETE from {DataStore().categories_table} where id={cid}"
        ret = DataStore().execute(query_str)
#        print(query_str)
#        self._notify()
        return ret
 
    def deleteAll(self):
        for c in self.categories:
            query_str = f"DELETE from {DataStore().categories_table} where id={c.id}"
            DataStore().execute(query_str)
        self.categories = []
        
        
    def getRulesForCategorization(self):
        category_rules_list = []
        rule_dict = None
        for c in self.categories:
            rgx = c.getRegex(True)
            if rgx:
                rule_dict = {
                    "type": "regex",
                    "regex": c.getRegex(True)
                    }
            else:
                rule_dict = {"type":"none"}
            rule_def = ((c.name,),rule_dict)
            category_rules_list.append(rule_def)
        return category_rules_list
    
    
class CategoryDefinition(Observable):
    
    def __init__(self, c_list):
        super().__init__()
        self.id = c_list[0]
        self.view_id = c_list[1]
        self.name = c_list[2]
        self.color = c_list[3]
        self.events =[]
        self.positive_words = []
        self.negative_words = []
        self._loadSelectedEvents()
        self._loadSelectedWords()
        self.proxy = CategoryContentsProxy(self)
        
    def _loadSelectedEvents(self):
        query_str =f"SELECT * FROM {DataStore().events_table} WHERE category_id ={self.id}"
        def_list = DataStore().query(query_str)
        self.events = def_list
    
    def _loadSelectedWords(self):
        query_str =f"SELECT * FROM {DataStore().words_table} WHERE category_id ={self.id} AND positive = 1"
        self.positive_words = DataStore().query(query_str)   
        query_str =f"SELECT * FROM {DataStore().words_table} WHERE category_id ={self.id} AND positive = 0"
        self.negative_words = DataStore().query(query_str)

    def _notify(self, obj):
        obj.notifyCategoryChange(self) 
        
    def addEvent(self, event_data):
        title = event_data[1].replace("'","''")
        query_str = f"INSERT into {DataStore().events_table} (category_id, app, title) values ({self.id},\'{event_data[0]}\',\'{title}\')"
        eid = DataStore().execute(query_str)
#        eid = ret
        self.events.append([eid, self.id, event_data[0], event_data[1]])
#        self._notify()
        return eid

    
    def deleteEvent(self, eid):
        elist = [e for e in self.events if e[0]==eid]
        if len(elist)==1:
            self.events.remove(elist[0])
        else:
            return False

        query_str = f"DELETE from {DataStore().events_table} where id={eid}"
        ret = DataStore().execute(query_str)
#        self._notify()
        return ret
    
    def addWord(self, cid, word, positive):
        x = 1 if positive else 0
        query_str = f"INSERT into {DataStore().words_table} (category_id, word, positive) values ({cid},'{word}',{x})"
        wid = DataStore().execute(query_str)
#        wid = ret
        if positive :
            self.positive_words.append([wid, cid, word])
        else :
            self.negative_words.append([wid, cid, word])
#        self._notify()
        return wid

    
    def deleteWord(self, wid, positive):
        if positive:
            wlist = [w for w in self.positive_words if w[0]==wid]
            if len(wlist)==1:
                self.positive_words.remove(wlist[0])
            else:
                return False
        else:
            wlist = [w for w in self.negative_words if w[0]==wid]
            if len(wlist)==1:
                self.negative_words.remove(wlist[0])
            else:
                return False
        query_str = f"DELETE from {DataStore().words_table} where id={wid}"
        ret = DataStore().execute(query_str)
#        self._notify()
        return ret

    def deleteAll(self):
        for e in self.events:
            query_str = f"DELETE from {DataStore().events_table} where id={e[0]}"
            DataStore().execute(query_str)
        self.events = []
        for pwd in self.positive_words:
            query_str = f"DELETE from {DataStore().words_table} where id={pwd[0]}"
            DataStore().execute(query_str)           
        self.positive_words = []
        for nwd in self.negative_words:
            query_str = f"DELETE from {DataStore().words_table} where id={nwd[0]}"
            DataStore().execute(query_str) 
        self.negative_words = []
    
    def getRegex(self, use_ev=False):
        if len(self.negative_words)==0 and len(self.positive_words)==0:
            return None
        if len(self.negative_words)==0 :
            nega_str=""
        else:
            nega_str="(?!.*("
            for w in self.negative_words:
                if not nega_str =="(?!.*(":
                    nega_str = nega_str+"|"
                nega_str = nega_str+self.appendCCString(w[2])
            nega_str = nega_str + "))"
        posi_str = self.getPositiveRegex(use_ev)

        if nega_str=="" and posi_str=="":
#            full_str ="$^"
            full_str = None
        else:
            full_str = f"^{nega_str}{posi_str}.*$"
        return full_str

    def getPositiveRegex(self, use_ev):
#        print(f" use event data {use_ev}")
        if len(self.positive_words)==0:
            if use_ev:
                if len(self.events)==0:
                    posi_str = ""
            else:
                posi_str = ""
        else:
            posi_str=".*("
            for pw in self.positive_words:
                if not posi_str ==".*(":
                    posi_str = posi_str+"|"
                posi_str = posi_str+self.appendCCString(pw[2])
            if use_ev:
                for ev in self.events:
                    if not posi_str ==".*(":
                        posi_str = posi_str+"|"
                    posi_str = posi_str+ev[3]
            posi_str = posi_str + ")"
        return posi_str
    

    def appendCCString(self, str):
        # append combined character sequence string
        nfd_str = unicodedata.normalize('NFD',str)
        nfc_str = unicodedata.normalize('NFC',str)
        if nfd_str == nfc_str:
            return nfc_str
        else:
            return nfc_str+"|"+nfd_str

    
class CategoryContentsProxy(Observable):
    
    def __init__(self, category):
        super().__init__()
        self.category = category
    def _notify(self, obj):
        obj.notifyCategoryContentsChange(self.category) 
        
