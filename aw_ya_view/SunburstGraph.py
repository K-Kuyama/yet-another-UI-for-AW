from datetime import datetime, timedelta, time
import json
import dateutil.tz as tz
from aw_client import queries
import matplotlib.pyplot as plt
from aw_ya_view.lib import EnhancedJSONEncoder
from aw_ya_core.lib import dprint, removeEscape


def createQueryStrings(categorize1, categorize2):
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
    merged_events = merge_events_by_keys(c_events,[\"$category\"]);
    """
  
    list_str ="{"
    for i, cinfo in enumerate(categorize1):
        c_str = f"""
            events_{i} = filter_keyvals(events, \"$category\" [[{json.dumps(cinfo[0][0], cls=EnhancedJSONEncoder)}]]);
            events_{i} = categorize(events_{i}, {classes_str2});
            merged_events_{i} = merge_events_by_keys(events_{i},[\"$category\"]);
            """
        ad_str = f"""
            events_uncategorized = filter_keyvals(c_events, \"$category\", [[\"Uncategorized\"]]);
            events_intersect = filter_period_intersect(events,events_uncategorized);
            events_uncategorized2 = categorize(events_intersect, {classes_str2});
            merged_events_uncategorized = merge_events_by_keys(events_uncategorized2,[\"$category\"]);
            """
        return_str = return_str + c_str + ad_str
    
        if not list_str == "{":
            list_str = list_str + ","
        list_str = list_str + f"\"{cinfo[0][0]}\" : merged_events_{i}"
    list_str = list_str +", \"Uncategorized\" : merged_events_uncategorized}"
    last_line_str = f"RETURN = [merged_events , {list_str}]"
    return return_str + last_line_str



class SunburstGraph:
    
    def __init__(self, parent):
        self.parent = parent

    def createView(self, canvas):
        categorize1 = self.parent.selected_views[0].getRulesForCategorization()
        categorize2 = self.parent.selected_views[1].getRulesForCategorization()
        
        query_str = createQueryStrings(categorize1, categorize2)

        ts = datetime.combine(self.parent.date, time(0,0,0),tzinfo=tz.tzlocal())
        td = timedelta(days=1)
        timeperiods = [(ts, ts+td)]

        res = self.parent.awc.query(query_str, timeperiods)
            
        cat1_info = res[0][0]
        cat2_dict = res[0][1]
        cat1_labels = []
        cat1_data =[]
        cat1_colors =[]
        cat2_labels = []
        cat2_data =[]
        cat2_colors =[]

        for ev in cat1_info:
            label_str =""
            label = ev['data']['$category'][0]
            label_str = label.encode().decode('unicode-escape')
            cat1_labels.append(label_str)
  
            for c in self.parent.selected_views[0].categories:
                if c.name == label_str:
                    cat1_colors.append(c.color)
                    break
            if label_str =="Uncategorized":
                cat1_colors.append("lightgray")

            cat2_info = cat2_dict[label_str]   
            c1_duration = 0
            for cat in cat2_info:
                label_str =""
                label = cat['data']['$category'][0]
                label_str = label.encode().decode('unicode-escape')
#                print(f"C2:{label_str}")
                cat2_labels.append(label_str)
                cat2_data.append(cat['duration'])
                c1_duration += cat['duration']
                for c in self.parent.selected_views[1].categories:
                    if c.name == label_str:
                        cat2_colors.append(c.color)
                        break
                if label_str =="Uncategorized":
                    cat2_colors.append("lightgray")
            cat1_data.append(c1_duration)
            
        with self.parent.out:
            wedgeprops={"width":0.5, "edgecolor":'white'}
            canvas.pie(cat1_data, radius=0.6, labels=cat1_labels, startangle=90, counterclock=False, 
                       wedgeprops=wedgeprops, colors=cat1_colors, labeldistance=0.1, rotatelabels=True)
            canvas.pie(cat2_data, radius=1.1, labels=cat2_labels, startangle=90, counterclock=False, 
                       wedgeprops=wedgeprops, colors=cat2_colors, labeldistance=0.8, rotatelabels=True)
        
            canvas.set_title(f"時間比率 {self.parent.selected_views[0].name}/{self.parent.selected_views[1].name}"
                         ,fontsize=12,color="Blue")
        
        