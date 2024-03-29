'''
Created on 2024/01/12

@author: kuyamakazuhiro
'''


import sys
import os

print(sys.path)
from voila.app import Voila

from IPython.display import *
#from aw_ya_editor.defeditor import AnalysisDefEditor


def get_resource_path():    
    rel_path = sys.argv[0]
    abs_path = os.path.join(os.path.abspath("."), rel_path)
    if getattr(sys,'frozen',False):
        return os.path.join(os.path.dirname(abs_path),"_internal")
    else:
        #return os.path.join( os.path.dirname(abs_path),"..")
        return os.path.dirname(abs_path)

def start_voila(file_path):
    app = Voila()
    print(f"file_path = {file_path}")
    app.initialize([file_path])
    app.start()


def aw_ya_launcher():
    rpath = get_resource_path()
    os.environ['YA_DBFILE_PATH']=os.path.join(rpath,"DefDB.db")
    start_voila(os.path.join(rpath,sys.argv[1])) 
    

if __name__ == "__main__":
    aw_ya_launcher()   
