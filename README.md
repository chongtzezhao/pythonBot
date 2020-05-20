# python bot

This bot runs on python to execute python code for you ^_^

Future: 
- [x] ~~multithreading/multiprocessing to handle multiple requests at once~~ Done using async
- [x] ~~"environments" or "workspaces", i.e. imports, variables and functions will be saved~~ Variables preserved

## Version 0.2.0
- Multiple request handling done with asynchronous subprocess execution using the [https://docs.python.org/3/library/asyncio.html](asyncio) module. Timeout henced increased to 120 seconds
- Environments are implemented using json files. Sets are currently not supported due to lack of native json compatibility.

