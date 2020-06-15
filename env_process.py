import json
import time
import re
import os
from os import listdir
from os.path import isfile, join
import copy
os.environ['TZ'] = 'Singapore'
time.tzset()

GEN_ENV=os.getenv('GEN_ENV')
os.environ['GEN_ENV']='[REDACTED]'

SEP=os.getenv('SEP')
os.environ['SEP']='[REDACTED]'

KEYWORDS = {'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'with', 'yield'}

def load_env(contents):
    mypath = "./envs"
    envs = [f[:-5] for f in listdir(mypath) if isfile(join(mypath, f)) and f[-4:]=='json']
    stuff = (contents.find(' '), contents.find('\n'),  contents.find('`'))
    index = len(contents)
    for val in stuff: 
        if val>-1: index = min(index, val)
    if index==-1: index = len(contents)
    env_name = contents[1:index].strip()
    if env_name not in envs:
        data = {"vars":{}, 'imports':{}, 'time':{'created':time.strftime("%Y-%m-%d %H:%M:%S"), 'modified': time.strftime("%Y-%m-%d %H:%M:%S"), 'accessed':time.strftime("%Y-%m-%d %H:%M:%S")}}
        with open(f'envs/{env_name}.json', 'w+') as outfile:
            json.dump(data, outfile)
    
        return '', env_name
    else:
        data = json.load(open(f'envs/{env_name}.json'))
        out = ''
        for name in data['vars']:
            value = data['vars'][name]
            if name.endswith('-set'): # means the array is actually is a set
                value = set(value)
                name = name[:-4]
            if type(value)==type(''):
                value = value.replace('"', '\\"')
                value = f'"{value}"'
            out+=f'{name} = {value}\n'
        return out, env_name


def output_env(code):
    new_code = code.replace(';', '\n')
    lines = new_code.split('\n')
    output = f"print('{GEN_ENV}')\n"
    for line in lines:
        line = line.strip()
        k = re.match("^[a-zA-Z_][a-zA-Z0-9_]*", line)
        if k:
            start, end = k.span()
            name = line[start:end]
            if name in KEYWORDS: continue
            output+=f"try: print('{name}{SEP}'+str({name})+'{SEP}'+str(type({name})) )\nexcept: print('{name}')\n"
    return output

    
    
def write_env(name, data):
    lines = data.split('\n')
    print(data)
    from_file = json.load(open(f'envs/{name}.json'))
    original = copy.deepcopy(from_file)
    print("json:",from_file)
    print("data:",data)
    for line in lines:
        if not line: continue
        arr = line.split(SEP)
        if len(arr)<3:
            try:
                del from_file['vars'][arr[0]]
            except:
                pass
            continue
        arr[2] = arr[2].split("'")[1]
        if arr[2]=='str': 
            tmp = arr[1]
            print(tmp)
        else:
            tmp=eval(arr[1])
        if arr[2]=='set':
            tmp=list(tmp)
            arr[0] += '-set'
        from_file['vars'][arr[0]]=tmp
    print(original)
    print(from_file)
    print(from_file==original)
    if from_file!=original:
        from_file['time']['modified'] = time.strftime("%Y-%m-%d %H:%M:%S")
    from_file['time']['accessed'] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(f'envs/{name}.json', 'w') as outfile:
        json.dump(from_file, outfile)