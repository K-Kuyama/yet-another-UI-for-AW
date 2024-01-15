from datetime import datetime, timedelta
import sys
import os


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


def addEscape(string):
    dictionary = {
            "(": "\(",
            ")": "\)",
            "{": "\{",
            "}": "\}"
        }
    trans_table = string.maketrans(dictionary)
    escaped_string = string.translate(trans_table)
    return escaped_string


def removeEscape(string):
    escaped_string = string.replace("\(", "(").replace("\)", ")").replace("\{", "{").replace("\}", "}")
    return escaped_string


