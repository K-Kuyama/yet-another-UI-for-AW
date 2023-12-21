from datetime import datetime, timedelta, time
import json
import dateutil.tz as tz
from aw_ya_view.lib import EnhancedJSONEncoder
from aw_ya_core.lib import dprint, tdeltaToString, removeEscape

def createDoubledQueryStrings(categorize1, categorize2):
#    dprint("double args")
    # [[categorize1で分類したリスト],{categorize1のカテゴリー名：categorize2で分類したリスト, .......}]   
    classes_str1 = json.dumps(categorize1, cls=EnhancedJSONEncoder)
    classes_str1 = removeEscape(classes_str1)
    classes_str2 = json.dumps(categorize2, cls=EnhancedJSONEncoder)
    classes_str2 = removeEscape(classes_str2)
    
    return_str = f"""
    events = flood(query_bucket(find_bucket(\"aw-watcher-window_\")));
    not_afk = flood(query_bucket(find_bucket(\"aw-watcher-afk_\")));
    not_afk = filter_keyvals(not_afk, "status", [\"not-afk\"]);
    events = filter_period_intersect(events, not_afk);
    c_events = categorize(events,{classes_str1});
    merged_events1 = merge_events_by_keys(c_events,[\"$category\"]);
    sum_durations = sum_durations(merged_events1);
    c_events = categorize(events,{classes_str2});
    merged_events2 = merge_events_by_keys(c_events,[\"$category\"]);
    RETURN = [sum_durations, merged_events1, merged_events2]
    """
    return return_str


def createQueryStrings(categorize1):
#    dprint("single arg")
    # [[categorize1で分類したリスト],{categorize1のカテゴリー名：categorize2で分類したリスト, .......}]   
    classes_str1 = json.dumps(categorize1, cls=EnhancedJSONEncoder)
    classes_str1 = removeEscape(classes_str1)
#    classes_str2 = json.dumps(categorize2, cls=EnhancedJSONEncoder)
    
    return_str = f"""
    events = flood(query_bucket(find_bucket(\"aw-watcher-window_\")));
    not_afk = flood(query_bucket(find_bucket(\"aw-watcher-afk_\")));
    not_afk = filter_keyvals(not_afk, "status", [\"not-afk\"]);
    events = filter_period_intersect(events, not_afk);
    c_events = categorize(events,{classes_str1});
    merged_events1 = merge_events_by_keys(c_events,[\"$category\"]);
    sum_durations = sum_durations(merged_events1);
    RETURN = [sum_durations, merged_events1]
    """
    return return_str

class InformationBoard:
    def __init__(self,parent):
        self.parent = parent
        
    def createView(self, canvas):
#        categorize1 = self.parent.selected_views[0].getRulesForCategorization()
#        categorize2 = self.parent.selected_views[1].getRulesForCategorization()
        view0 = self.parent.selected_views[0]
        view1 = self.parent.selected_views[1]
        first_view = None
        query_str = None
#        dprint("inside createView")
        if not view0:
            if not view1:
                return 
            else:
                dprint(f"{view0} and {view1}")
                first_view = view1
                categorize2 = view1.getRulesForCategorization()
                query_str = createQueryStrings(categorize2)
        else:
            if not view1:
                dprint(f"{view0} and {view1}")
                first_view = view0
                categorize1 = view0.getRulesForCategorization()
                query_str = createQueryStrings(categorize1)
            else:
                dprint(f"{view0} and {view1}")
                first_view = view0
                categorize1 = view0.getRulesForCategorization()
                categorize2 = view1.getRulesForCategorization()
                dprint("createQueryStrings")
                query_str = createDoubledQueryStrings(categorize1, categorize2)

        # dprint(query_str)
        ts = datetime.combine(self.parent.date, time(0,0,0),tzinfo=tz.tzlocal())
        td = timedelta(days=1)
        timeperiods = [(ts, ts+td)]

        res = self.parent.awc.query(query_str, timeperiods)
        # dprint(res[0])
        
        total_time = res[0][0]
        dprint(type(total_time))
        cat1_info = res[0][1]
        cat2_info = None
        dprint(f"res0 len = {len(res[0])}")
        if len(res[0])>2 :
            cat2_info = res[0][2]
        
        data_dict1 = dict()
        for c in first_view.categories:
            data_dict1[c.name]=[c.color, f"{c.name:<15} : 00:00:00"]   
            data_dict1['Uncategorized']=["lightgray", "Uncategorized : 00:00:00"]
            
        for ev in cat1_info:
            label = ev['data']['$category'][0]
            label_str = label.encode().decode('unicode-escape')
            dt = timedelta(seconds = ev['duration'])
            data_dict1[label_str][1]=f"{label_str:<15} : {tdeltaToString(dt)}"
            
         
        canvas.text(0.5, 0.95, f"総合計時間 : {tdeltaToString(timedelta(seconds =total_time))}", 
                    horizontalalignment='center',verticalalignment='top',
                    fontsize=12)

        dinfo = [data[1] for data in data_dict1.values()]
        displayed_str1 ='\n'.join(dinfo)

        canvas.text(0.1, 0.85, displayed_str1, 
                    horizontalalignment='left',verticalalignment='top',
                    fontsize=8, backgroundcolor = "lightgray")
        dprint(f"cat2_info={cat2_info}")
        if cat2_info:    
            data_dict2 = dict()
            for c in self.parent.selected_views[1].categories:
                data_dict2[c.name]=[c.color, f"{c.name} : 00:00:00"]   
                data_dict2['Uncategorized']=["lightgray", "Uncategorized : 00:00:00"]
            
            for ev in cat2_info:
                label = ev['data']['$category'][0]
                label_str = label.encode().decode('unicode-escape')
                dt = timedelta(seconds = ev['duration'])
                data_dict2[label_str][1]=f"{label_str} : {tdeltaToString(dt)}"   
           
            dinfo = [data[1] for data in data_dict2.values()]
            displayed_str2 ='\n'.join(dinfo)
            canvas.text(0.1, 0.4, displayed_str2, 
                        horizontalalignment='left',verticalalignment='top',
                        fontsize=8, backgroundcolor = "lightgray")
 
        canvas.set_title(f"{self.parent.date} の情報"
                         ,fontsize=12,color="Blue")
            
         
            