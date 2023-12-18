from datetime import datetime, timedelta
DEBUG_FILE = "debug.txt"

def dprint(model):
    with open(DEBUG_FILE, "a") as o:
        print(datetime.now(), file=o)
        print(model, file=o)
        

def tdeltaToString(timedelta):
    seconds = timedelta.seconds
    hr = seconds//60//60
    mn = seconds//60%60
    sec = seconds%60
    return f"{hr}:{mn}:{sec}"
