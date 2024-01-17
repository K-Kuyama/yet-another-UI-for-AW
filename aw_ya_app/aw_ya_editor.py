'''
Created on 2024/01/12

@author: kuyamakazuhiro
'''


import sys
import os

from voila.app import Voila


def get_resource_path():
    rel_path = sys.argv[0]
    abs_path = os.path.join(os.path.abspath("."), rel_path)
    return os.path.join( os.path.dirname(abs_path),"..")

def start_voila(file_path):
    app = Voila()
    print(f"file_path = {file_path}")
    app.initialize([file_path])
    app.start()


rpath = get_resource_path()
os.environ['YA_DBFILE_PATH']=os.path.join(rpath,"DefDB.db")
start_voila(os.path.join(rpath,"DefEditorApp.ipynb")) 
    