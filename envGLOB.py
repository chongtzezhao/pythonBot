
import importlib

def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    not_allowed = ["os"]#, "importlib", "wget", "urllib", "requests"]
    frommodule = globals['__name__'] if globals else None
    if name in not_allowed:
        print(f'50d96c61-f56d-4704-b781-b36cc2953b16 {name} ')

    return importlib.__import__(name, globals, locals, fromlist, level)

__builtins__.__dict__['__import__'] = secure_importer

y=10
x=4
print('73a3290c-340b-44b1-9899-8542f0894495')

