import shutil
import os
import threading
import time
from pprint import pprint

ALLOWED = ['pyproject.toml', '.upm', 'poetry.lock', 'envGLOB.py', 'README.md', 'requirements.txt', '__pycache__', 'keep_alive.py', 'spam_data.json', 'detect_spam.py', 'process.py', 'alerts.py', 'main.py', 'cleaner.py', 'envs', 'env_process.py', 'main_backup.py', 'out.txt']

def clean():
    global ALLOWED
    while True:
        
        stuff = os.listdir()
        for item in stuff:
            if item not in ALLOWED:
                print(f"Removed: {item}")
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
        else:
            print("nothing found")
        time.sleep(20)
        #print(os.listdir())

def start_cleaning():
    t1 = threading.Thread(target=clean)
    t1.start()

def create_file():
    k = open("HAHAH.txt", 'w+')
    k.write("asdfsjdflsjf")
    k.close()

    