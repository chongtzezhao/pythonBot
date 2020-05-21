# python bot

This bot runs on python to execute python code for you ^_^

Future: 
- [x] ~~multithreading/multiprocessing to handle multiple requests at once~~ Done using async
- [x] ~~"environments" or "workspaces", i.e. imports, variables and functions will be saved~~ Variables preserved

## Version 0.2.0
- Multiple request handling done with asynchronous subprocess execution using the [https://docs.python.org/3/library/asyncio.html](asyncio) module. Timeout henced increased to 120 seconds
- Environments are implemented using json files. Sets are currently not supported due to lack of native json compatibility.

## Version 0.2.1
- Added a file cleaner/manager which sieves through the files and deletes any new ones. Also able to contact owner (through telegram) to restore original files.

## Version 0.3.0
- Removed all import, file, or directory restrictions, basically going full open source (while hopefully maintaining secrecy of bot token)
- Moved telegram bot token to a secret location to prevent misuse or spam

If all goes well, will move to 1.0, allowing the exec function and executing code in user pms.

Thanks for reading! If you find any bugs or security issues, please let me know on discord, at thepoppycat#3897!