import subprocess as sb
import time
from prompt_toolkit import prompt
from time import sleep
from rich import print
from rich.progress import Progress
import sys
import json
from pathlib import Path
from datetime import datetime
import itertools
import winsound
#^^^^^^^^^ LIBS ^^^^^^^^^^^

glDir = Path(__file__).resolve().parent.parent

colors = None
iMem = None
decleration = None

with open(glDir / "json" / "colors.json","r") as f:
    colors = json.load(f)
with open(glDir / "json" / "iMem.json","r") as f:
    iMem = json.load(f)
with open(glDir / "json" / "commandDecl.json","r") as f:
    decleration = json.load(f)

def read():
    with open(glDir / "json" / "colors.json","r") as f:
        colors = json.load(f)
    with open(glDir / "json" / "iMem.json","r") as f:
        iMem = json.load(f)
    return colors, iMem

logFile = glDir / "log.txt" # LOG!!

spinner = itertools.cycle(["|", "/", "-", "\\"])

global running
running = False

currentDir = "-R:"
while running:
    colors, iMem = read()
    sleep()

def load() -> None:
    sb.run("cls", shell=True)
    colors, iMem = read()
    title()
    if colors is None:
        print("[italic red] Error >: Not loaded colors.json")
    
    tstart = time.time()
    with Progress() as progress:
        loadingbar = progress.add_task("")
        while not progress.finished:
            progress.update(loadingbar,description=f"[green]{next(spinner)}\b", advance=5)
            sleep(0.1)
    

    
    print(f"[italic gray66]took -> {time.time() - tstart:0.2f}s")

    sb.run("cls", shell=True)
    running = True
    title()
    
    if running == True:
        while running:
            running = interpreter(input(f"[{currentDir}] >: "))
    

def interpreter(input: str):
    args = input.split()
    print(args)
    
    if args[0].lower() == "exit":
        sb.run("cls", shell=True)
        return False
    
    try:
        funk = sys.modules[__name__].__dict__[args[0].lower()]
    except:
        pass

    cmin = decleration[args[0]]["minArgs"]
    cmax = decleration[args[0]]["maxArgs"]
    args.pop(0)

    if len(args) < cmin or len(args) > cmax:
        print(f"[red] !>>> Error: param min did not pass or param max passed <{len(args) - 1}>")
        winsound.Beep(550, 500)
        return True
    else:
        params = [] 
        for param in args:
            params.append(param)
    if not len(params) == 0:
        funk(*params)
    else:
        funk()

    return True





def title() -> None:
    # -----------------------]  GUI  [--------------------------------------------
    print(fr'''[bold {colors["logo"]}]
__________________________________________________________________╱╲╲╲╲╲╲__________        
 __╱╲╲╲___________________________________________________________╲╱╱╱╱╲╲╲__________       
  _╲╱╱╱╱╲╲╲___________________________________________________________╲╱╲╲╲__________      
   ____╲╱╱╱╱╲╲╲_______╱╲╲╲╲╲__╱╲╲╲╲╲____╱╲╲╲╲╲╲╲╲╲_____╱╲╲╲____╱╲╲╲____╲╱╲╲╲__________     
    _______╲╱╱╱╱╲╲╲__╱╲╲╲╱╱╱╲╲╲╲╲╱╱╱╲╲╲_╲╱╱╱╱╱╱╱╱╲╲╲___╲╱╱╱╲╲╲╱╲╲╲╱_____╲╱╲╲╲_____╱╲╲╲_    
     ________╱╲╲╲╱╱__╲╱╲╲╲_╲╱╱╲╲╲__╲╱╲╲╲___╱╲╲╲╲╲╲╲╲╲╲____╲╱╱╱╲╲╲╱_______╲╱╲╲╲____╲╱╱╱__   
      _____╱╲╲╲╱╱_____╲╱╲╲╲__╲╱╲╲╲__╲╱╲╲╲__╱╲╲╲╱╱╱╱╱╲╲╲_____╱╲╲╲╱╲╲╲______╲╱╲╲╲__________  
       __╱╲╲╲╱╱________╲╱╲╲╲__╲╱╲╲╲__╲╱╲╲╲_╲╱╱╲╲╲╲╲╲╲╲╱╲╲__╱╲╲╲╱╲╱╱╱╲╲╲__╱╲╲╲╲╲╲╲╲╲__╱╲╲╲_ 
        _╲╱╱╱___________╲╱╱╱___╲╱╱╱___╲╱╱╱___╲╱╱╱╱╱╱╱╱╲╱╱__╲╱╱╱____╲╱╱╱__╲╱╱╱╱╱╱╱╱╱__╲╱╱╱__
          ''')
    print("[italic gray66]>maxl: {version 0.0.1}")
    print("[italic gray66]made by Filip")
    print("[dim grey66]Note: This is a safe sandbox - real files unchanged :P [/dim grey66]")
    winsound.Beep(550, 500)


def getFolderById(id):
    colors, iMem = read()
    if id is None:
        return [data for data in iMem]
    try:
        int(id)
    except:
        print(f"[{colors["err"]}] !>>> Error: nonnumeric entered in id <{id}>")
        winsound.Beep(550, 500)
        return
    segrId = [int(num) for num in id]
    pathSaved = None
    for searchId in segrId:
        if pathSaved is None:
            pathSaved = iMem[searchId]
            continue
        if not pathSaved["type"] == "folder":
            print(f"[{colors["err"]}] !>>> Error: cant provide children for <{pathSaved["type"]}; {pathSaved["id"]}> type")
            winsound.Beep(550, 500)
            return
        try:
            pathSaved["children"]
        except:
            print(f"[{colors["err"]}] !>>> Error: cant find children <{pathSaved[id]}>")
            winsound.Beep(550, 500)
            return
        pathSaved = pathSaved["children"][searchId]
    
    if "file" in pathSaved["type"]:
        print(f"[{colors["err"]}] !>>> Error: cant provide children for <{pathSaved["type"]}> type")
        winsound.Beep(550, 500)
        return
    return pathSaved["children"]

def getItemById(id):
    colors, iMem = read()
    try:
        int(id)
    except:
        print(f"[{colors["err"]}] !>>> Error: nonnumeric entered in id <{id}>")
        return
    segrId = [int(num) for num in id]
    pathSaved = None
    for searchId in segrId:
        if pathSaved is None:
            pathSaved = iMem[searchId]
            continue
        try:
            pathSaved["children"]
        except:
            print(f"[{colors["err"]}] !>>> Error: cant find next children or doesnt exist <{pathSaved[id]}>")
            winsound.Beep(550, 500)
            return
        pathSaved = pathSaved["children"][searchId]
    
    if pathSaved["type"] == "folder":
        print(f"[{colors["err"]}] !>>> Error: cant provide content for <{pathSaved["type"]}> type")
        winsound.Beep(550, 500)
        return
    else:
        return pathSaved

def help():
    print(f'''[{colors["output"]}].>>>[/{colors["output"]}]
                help                          [{colors["output"]}]-> list of commands[/{colors["output"]}] 
                exit                          [{colors["output"]}]-> end >MAXL:[/{colors["output"]}]
                ls [id]                       [{colors["output"]}]-> lists imem of id (none to root)[/{colors["output"]}]
                get [id]                      [{colors["output"]}]-> print value of imem at id[/{colors["output"]}]
                edit [id]                     [{colors["output"]}]-> edits imem at id[/{colors["output"]}]
                new [type] [name] [id]        [{colors["output"]}]-> new val at id[/{colors["output"]}]
                calc [eq]                     [{colors["output"]}]-> simple calculator[/{colors["output"]}]
    ''')

def ls(id=None):
    toprint = getFolderById(id)
    if toprint is None:
        return
    print(f"[{colors["output"]}].>>> ")
    for to in toprint:
        print(str(f"{to["name"]} [{colors["str"]}]<{to["type"]} ; {to["id"]}>"))

def get(id=None):
    if id is None:
        print(f"[{colors["err"]}] !>>> Error: id can not be None <{id}>")
        winsound.Beep(550, 500)
    try:
        itemPath = getItemById(id)
    except:
        return
    
    name = itemPath["name"]
    try:
        content = itemPath["content"]
    except:
        return

    print(f"[{colors["output"]}].>>> ")
    print(f"{name} [{colors["str"]}] <{type} ; {id}>")
    print(f"[{colors["bounders"]}]<:>")
    for i in range(len(content)):
        text = content[i]
        print(f"[{colors["output"]}]{i} -> [{colors["content"]}]{text}")
    print(f"[{colors["bounders"]}]<:>")

def edit(id=None):
    newL = False
    itemPath = getItemById(id)
    get(id)
    try:
        answer = int(input("LineId to edit (enter next in line for new line): "))
    except:
        print(f"[{colors["err"]}] !>>> Error: lineId can not be None or nonnumeric <{answer}>")
        winsound.Beep(550, 500)
        return
    
    if len(itemPath["content"]) == answer:
        itemPath["content"].append("")
        newL = True

    try:
        correction = str(prompt(f"{answer} -> " , default=(itemPath["content"][answer])))
    except:
        print(f"[{colors["err"]}] !>>> Error: lineId out of range <{answer}>")
        winsound.Beep(550, 500)
        return

    segrId = [int(num) for num in id]
    pathSaved = None
    for searchId in segrId:
        if pathSaved is None:
            pathSaved = iMem[searchId]
            continue
        try:
            pathSaved["children"]
        except:
            print(f"[{colors["err"]}] !>>> Error: cant find next children or doesnt exist <{pathSaved["id"]}>")
            winsound.Beep(550, 500)
            return
        pathSaved = pathSaved["children"][searchId]
    
    if correction == "":
        pathSaved["content"].pop(answer)
    else:
        if not newL:
            pathSaved["content"][answer] = correction
        else:
            pathSaved["content"].append(correction)

    with open(glDir / "json" / "iMem.json","w") as f:
        json.dump(iMem, f, indent=4)
    
    print(f"[{colors["output"]}]Saved <{itemPath["name"]} ; {itemPath["type"]}> to {id} ")

def new(type=None, name=None, id=None):
    if (type or name or id) is None:
        print(f"[{colors["err"]}] !>>> Error: all three parameters must be inputted <{[type, name, id]}>")
        winsound.Beep(550, 500)
        return
    
    segrId = [int(num) for num in id]
    last = segrId[-1]
    segrId.pop(-1)
    pathSaved = None
    for searchId in segrId:
        if pathSaved is None:
            pathSaved = iMem[searchId]
            continue
        try:
            pathSaved["children"]
        except:
            print(f"[{colors["err"]}] !>>> Error: cant find next children or doesnt exist <{pathSaved["id"]}>")
            winsound.Beep(550, 500)
            return
        pathSaved = pathSaved["children"][searchId]
    
    if type.lower == "folder":
        pathSaved["children"].append({
            "name": name,
            "id": id,
            "type": type.lower(),
            "children": []
        })
    else:
        pathSaved["children"].append({
            "name": name,
            "id": id,
            "type": type.lower(),
            "content": []
        })

    with open(glDir / "json" / "iMem.json","w") as f:
        json.dump(iMem, f, indent=4)
    
    print(f"[{colors["output"]}]Saved <{pathSaved["children"][last]["name"]} ; {pathSaved["children"][last]["type"]}> to {id} ")

def calc(eq):

    try:
        print(f"[{colors["output"]}].>>> {eval(eq)}")
    except:
        print(f"[{colors["err"]}] !>>> Error: cant eval <{eq}>")
        winsound.Beep(550, 500)
    