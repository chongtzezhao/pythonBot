import shutil
import os
import threading
import time
from pprint import pprint
import requests

ALLOWED = ['pyproject.toml', '.upm', 'poetry.lock', 'envGLOB.py', 'README.md', 'requirements.txt', '__pycache__', 'keep_alive.py', 'spam_data.json', 'detect_spam.py', 'process.py', 'alerts.py', 'main.py', 'file_manager.py', 'envs', 'env_process.py', '.gitignore']
RESTORE = ['pyproject.toml', 'poetry.lock', 'README.md', 'requirements.txt', 'keep_alive.py', 'spam_data.json', 'detect_spam.py', 'process.py', 'alerts.py', 'main.py', 'file_manager.py', 'env_process.py', '.gitignore']
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
os.environ['TELEGRAM_BOT_TOKEN']='[REDACTED]'

def clean():
    global ALLOWED
    while True:
        found = False
        for item in os.listdir():
            if item not in ALLOWED:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
                print(f"Removed: {item}")
                found = True
        if not found:
            print("nothing found")
        time.sleep(30)
        #print(os.listdir())

def check():
    global RESTORE
    global TELEGRAM_BOT_TOKEN
    while True:
        for item in RESTORE:
            contents = requests.post('https://definitionBot--thepoppycat.repl.co/pythonBot', data={'file_name':item}).text
            if contents=='file does not exist':
                print(f'Skipped: {file}')
                continue
            try:
                here = open(item).read()
                if contents!=open(item).read():
                    requests.get(
                        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id=956428669&text=yo python bot has critical files edited, name = {item}.\nSend "py restore" (in discord) to restore files')
            except:
                requests.get(
                    f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id=956428669&text=yo python bot has critical files missing.\nname = {item}')
        time.sleep(30)

def restore_files():
    print('restoring...')
    global RESTORE
    for item in RESTORE:
        contents = requests.post('https://definitionBot--thepoppycat.repl.co/pythonBot', data={'file_name':item}).text
        if contents=='file does not exist':
            print(f'Skipped: {file}')
            continue    
        f = open(item, 'w+')
        f.write(contents)
        f.close()
    print('Success!')

def start_managing():
    t1 = threading.Thread(target=clean)
    t1.start()
    t2 = threading.Thread(target=check)
    t2.start()


