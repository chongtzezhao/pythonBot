import asyncio
import subprocess

async def fakeFileError(message, line, line_num, fileName):
    await message.channel.send(f"""
```Traceback(most recent call last):
  File "envGLOB.py", line {line_num}, in < module >
    {line}
FileNotFoundError: [Errno 2] No such file or directory: '{fileName}'``` \n<@{message.author.id}>""")


async def fakeImportError(message, module):
    await message.channel.send(f"""
```Traceback (most recent call last):
  File "envGLOB.py", line 1, in < module >
ImportError: module '{module}' is restricted.``` \n<@{message.author.id}>"""
    )


def findBackticks(code):
    index = code.find("`")
    if index==-1: return ''
    if code[index:index+3]=="```":
        nextIndex = code.find("```", index+3)
        if code[index+3:index+9]=="python":
            index+=6
        elif code[index+3:index+5]=="py":
            index+=2
        return code[index+3:nextIndex]+"\n"+findBackticks(code[nextIndex+3:])
    else:
        nextIndex = code.find("`", index+1)
        while code[nextIndex:nextIndex+3]=="```":
            nextIndex = code.find("`", nextIndex+3)
        return code[index+1:nextIndex]+"\n"+findBackticks(code[nextIndex+1:])


def prepend():
    return """
import importlib

def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    not_allowed = ["os"]#, "importlib", "wget", "urllib", "requests"]
    frommodule = globals['__name__'] if globals else None
    if name in not_allowed:
        print(f'50d96c61-f56d-4704-b781-b36cc2953b16 {name} ')

    return importlib.__import__(name, globals, locals, fromlist, level)

__builtins__.__dict__['__import__'] = secure_importer

"""