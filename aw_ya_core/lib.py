from datetime import datetime, timedelta
DEBUG_FILE = "debug.txt"


def dprint(model):
    with open(DEBUG_FILE, "a") as o:
        print(datetime.now(), file=o)
        print(model, file=o)


def tdeltaToString(timedelta):
    seconds = timedelta.seconds
    hr = seconds//60//60
    mn = seconds//60 % 60
    sec = seconds % 60
    return f"{hr: 2d}:{mn: 02d}:{sec: 02d}"


def addEscape(str):
    dictionary = {
            "(": "\(",
            ")": "\)",
            "{": "\{",
            "}": "\}"
        }
    trans_table = str.maketrans(dictionary)
    escaped_string = str.translate(trans_table)
    return escaped_string


def removeEscape(str):
    escaped_string = str.replace("\(", "(").replace("\)", ")").replace("\{", "{").replace("\}", "}")
    return escaped_string
