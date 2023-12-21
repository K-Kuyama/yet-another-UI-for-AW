from datetime import datetime, timedelta, time
import json
import dateutil.tz as tz
from aw_client import queries
import matplotlib.pyplot as plt
from aw_ya_view.lib import EnhancedJSONEncoder
from aw_ya_core.lib import dprint, removeEscape

def createQueryStrings(categorize1):
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


def addElementValue(list1, list2):
    list_sum =[]
    for i, x in enumerate(list1):
        list_sum.append(list1[i]+list2[i])
    return list_sum



class HourlyGraph:
    
    def __init__(self,parent, index):
        self.parent = parent
        self.view = None
        self.index = index
    
    def createView(self, canvas):
        if self.index == 2:
            self.view = self.parent.selected_views[1]
        else:
            self.view = self.parent.selected_views[0]
        if not self.view:
            return 
        
        c_name = [c.name for c in self.view.categories]
        c_name.append("Uncategorized")
            
        data_dict = dict()
        for c in self.view.categories:
            data_dict[c.name]=[c.color,[]]   
            data_dict['Uncategorized']=["lightgray",[]]
            
        query_str = createQueryStrings(self.view.getRulesForCategorization())
        for hr in range(24):
            ts = datetime.combine(self.parent.date, time(hr,0,0),tzinfo=tz.tzlocal())
            td = timedelta(hours=1)
            timeperiods = [(ts, ts+td)]

            res = self.parent.awc.query(query_str, timeperiods)
            cat1_info = res[0][0]
  
        
            for c in c_name:
                if len(cat1_info)==0:
                    data_dict[c][1].append(0)
                else:
                    exist = False
                    for ev in cat1_info:
                        label = ev['data']['$category'][0]
                        label_str = label.encode().decode('unicode-escape')
                        if label_str == c:
                            data_dict[c][1].append(ev['duration']/3600)
                            exist = True
                    if not exist:
                        data_dict[c][1].append(0)
        
        x_ax =[x for x in range(24)]
        height = [0 for x in range(24)]
        for c_data in data_dict.items():
            canvas.bar(x_ax, c_data[1][1], bottom = height, facecolor = c_data[1][0], label = c_data[0], align="edge")
            height = addElementValue(height, c_data[1][1])
        canvas.set_xticks(x_ax)
        canvas.set_ylim(0,1)
        canvas.legend()
        canvas.set_title(f"時間帯グラフ　{self.view.name}",fontsize=12,color="Blue")
   