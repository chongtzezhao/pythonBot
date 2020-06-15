import shutil
import os
import threading
import time
from pprint import pprint
import requests

ALLOWED = ['pyproject.toml', '.upm', 'poetry.lock', 'envGLOB.py', 'README.md', 'requirements.txt', '__pycache__', 'keep_alive.py', 'process.py', 'alerts.py', 'main.py', 'file_manager.py', 'envs', 'env_process.py', '.gitignore', 'non_program.py']
RESTORE = ['pyproject.toml', 'poetry.lock', 'README.md', 'requirements.txt', 'keep_alive.py', 'process.py', 'alerts.py', 'main.py', 'file_manager.py', 'env_process.py', '.gitignore', 'non_program.py']
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
os.environ['TELEGRAM_BOT_TOKEN']='[REDACTED]'

def check_and_clean():
    while True:
        #check
        error = False
        for item in RESTORE:
            contents = requests.post('https://definitionBot--thepoppycat.repl.co/pythonBot', data={'file_name':item}).text
            if contents=='file does not exist on server':
                print(f'Skipped: {file}')
                continue
            try:
                here = open(item).read()
                if contents!=open(item).read():
                    error = item
                    print(error)
                    requests.get(
                        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id=956428669&text=yo python bot has critical files edited, name = {item}.\nSend "pysync" (in discord) to restore files')
            except Exception as e:
                error = e
                requests.get(
                    f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id=956428669&text=yo python bot has critical files missing.\nname = {item}')
        if not error:
            print('all ok')
        #clean
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
        time.sleep(60)

def restore_files():
    print('restoring...')
    for item in RESTORE:
        contents = requests.post('https://definitionBot--thepoppycat.repl.co/pythonBot', data={'file_name':item}).text
        if contents=='file does not exist':
            print(f'Skipped: {file}')
            continue    
        print(contents, file = open(item, 'w+'))
    print('Success!')

def start_managing():
    t1 = threading.Thread(target=check_and_clean)
    t1.start()

