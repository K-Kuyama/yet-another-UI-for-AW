from datetime import datetime, timedelta, time
import json
import dateutil.tz as tz
from aw_client import queries
import matplotlib.pyplot as plt
from aw_ya_view.lib import EnhancedJSONEncoder
from aw_ya_core.lib import dprint, removeEscape


def createQueryStrings(categorize1):
    # [[categorize1で分類したリスト],{categorize1のカテゴリー名：categorize2で分類したリスト, .......}]   
    classes_str1 = json.dumps(categorize1, cls=EnhancedJSONEncoder)
    classes_str1 = removeEscape(classes_str1)
    
    return_str = f"""
    events = flood(query_bucket(find_bucket(\"aw-watcher-window_\")));
    not_afk = flood(query_bucket(find_bucket(\"aw-watcher-afk_\")));
    not_afk = filter_keyvals(not_afk, "status", [\"not-afk\"]);
    events = filter_period_intersect(events, not_afk);
    c_events = categorize(events,{classes_str1});
    merged_events = merge_events_by_keys(c_events,[\"$category\"]);
    RETURN = [merged_events]
    """
    return return_str

class SinglePieChart:
    
    def __init__(self, parent, view):
#        dprint("init {self}")
        self.parent = parent
        self.view = view
        
    def createView(self, canvas):
 #       dprint(f"createView {self}")
        categorize1 = self.view.getRulesForCategorization()
        query_str = createQueryStrings(categorize1)
  #      dprint(query_str)

        ts = datetime.combine(self.parent.date, time(0,0,0),tzinfo=tz.tzlocal())
        td = timedelta(days=1)
        timeperiods = [(ts, ts+td)]  
        res = self.parent.awc.query(query_str, timeperiods)
        cat1_info = res[0][0]
        cat1_labels = []
        cat1_data =[]
        cat1_colors =[]
        
        for ev in cat1_info:
            label_str =""
            label = ev['data']['$category'][0]
            label_str = label.encode().decode('unicode-escape')
            cat1_labels.append(label_str)
  
            for c in self.view.categories:
                if c.name == label_str:
                    cat1_colors.append(c.color)
                    break
            if label_str =="Uncategorized":
                cat1_colors.append("lightgray")
            cat1_data.append(ev['duration'])
            
        with self.parent.out:
            wedgeprops={"edgecolor":'white'}
            canvas.pie(cat1_data, labels=cat1_labels, startangle=90, counterclock=False, 
                       wedgeprops=wedgeprops, colors=cat1_colors, labeldistance=0.1, rotatelabels=True)
            
        
        
        