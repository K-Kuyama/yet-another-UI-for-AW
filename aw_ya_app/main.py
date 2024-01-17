'''
Created on 2024/01/12

@author: kuyamakazuhiro
'''

import sys
import os
from voila.app import Voila

from IPython.display import *
from aw_ya_editor.defeditor import *



def get_resource_path():
    rel_path = sys.argv[0]
    abs_path = os.path.join(os.path.abspath("."), rel_path)
    return os.path.join( os.path.dirname(abs_path),"..")

def start_voila(file_path):
    app = Voila()
    print(f"file_path = {file_path}")
    app.initialize([file_path])
    app.start()


<<<<<<< HEAD
    def handler(signum, frame):
        if p1:
            print(f"send kill to {p1}")
            p1.kill()        
        if p2:
            print(f"send kill to {p2}")
            p2.kill()
        exit()
        
    signal.signal(signal.SIGINT, handler)
    
    wait_time = 5
    
    rpath = get_resource_path()

    os.environ['YA_DBFILE_PATH']=os.path.join(rpath,"DefDB.db")
    
    command_1 = ["voila", os.path.join(rpath,"DefEditorApp.ipynb")]
    command_2 = ["voila", os.path.join(rpath,"QtDashboardApp.ipynb")]

    p1 = subprocess.Popen(command_1)
    print(p1)
    time.sleep(wait_time)
    p2 = subprocess.Popen(command_2)
    print(p2)

    while True:
#        print(f"waiting {wait_time} sec")
        time.sleep(wait_time)
=======
print("start editor")   
rpath = get_resource_path()
os.environ['YA_DBFILE_PATH']=os.path.join(rpath,"DefDB.db")
start_voila(os.path.join(rpath,"DefEditorApp.ipynb")) 
>>>>>>> dev