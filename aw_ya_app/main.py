'''
Created on 2024/01/12

@author: kuyamakazuhiro
'''
import subprocess
import signal
import time

def main():
    print("main")

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

    command_1 = ["voila", "DefEditorApp.ipynb"]
    command_2 = ["voila", "QtDashboardApp.ipynb"]

    p1 = subprocess.Popen(command_1)
    print(p1)
    time.sleep(wait_time)
    p2 = subprocess.Popen(command_2)
    print(p2)

    while True:
        print(f"waiting {wait_time} sec")
        time.sleep(wait_time)
