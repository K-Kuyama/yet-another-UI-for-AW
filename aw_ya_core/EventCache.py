from datetime import datetime, timedelta, timezone, time
import dateutil.tz as tz
import aw_client


LATEST = """events = flood(query_bucket(find_bucket("aw-watcher-window_")));
                    not_afk = flood(query_bucket(find_bucket("aw-watcher-afk_")));
                    not_afk = filter_keyvals(not_afk, "status", ["not-afk"]);
                    events = filter_period_intersect(events, not_afk);
                    RETURN = events"""

LONGEST = """events = flood(query_bucket(find_bucket("aw-watcher-window_")));
                    not_afk = flood(query_bucket(find_bucket("aw-watcher-afk_")));
                    not_afk = filter_keyvals(not_afk, "status", ["not-afk"]);
                    events = filter_period_intersect(events, not_afk);
                    merged_events = merge_events_by_keys(events, ["app", "title"]); 
                    RETURN = sort_by_duration(merged_events);"""


class EventCache:
    
    def __init__(self):
        self.query_for_latest = LATEST
        self.query_for_longest = LONGEST
        self.events = None
        self.length = 0
        self.start_time = None
        self.end_time = None
        
        self.head_p = None
        self.tail_p = None
        self.awc = aw_client.ActivityWatchClient("EventBuffer")
        
        
    def load_events(self, day, kind) -> None:
#        ts = datetime.combine(day, time(0,0,0),tzinfo=timezone.utc)
        ts = datetime.combine(day, time(0,0,0),tzinfo=tz.tzlocal())
        timeperiods = [(ts, ts+timedelta(days=1))]
        query_str =""

        if kind == "longest" :
            query_str = self.query_for_longest
            res = self.awc.query(query_str,timeperiods)
        else:
            query_str = self.query_for_latest
            res = self.awc.query(query_str,timeperiods)
            res[0].reverse()     
        self.events = res[0]
        self.length = len(self.events)


    def get_head_events(self, num):
        self.head_p = 0
        events = self.events[0:num]
        if self.length < num:
            self.tail_p = self.length-1
        else:
            self.tail_p = num-1
        return events, self.head_p, self.tail_p

    def get_current_events(self):
        events = self.events[self.head_p:self.tail_p+1]
        return events, self.head_p, self.tail_p 
    
    def get_prev_events(self, num):
        if self.head_p == 0:
            events = None
        else:
            self.tail_p = self.head_p-1
            self.head_p = self.head_p-num
            events = self.events[self.head_p:self.tail_p+1]
        return events, self.head_p, self.tail_p    
    
    def get_next_events(self, num):
        if self.tail_p == self.length-1:
            events = None
        else:
            self.head_p = self.tail_p+1
            if self.tail_p+num >= self.length:
                self.tail_p = self.length-1
            else:
                self.tail_p = self.head_p+num-1 
            events = self.events[self.head_p:self.head_p+num]              
        return events, self.head_p, self.tail_p    
