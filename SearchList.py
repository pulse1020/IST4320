import re

def rece(search:str, inputListOrDict, found, key):
    if key == None:
        key = []
    f = 0
    if type(inputListOrDict) == dict:
        for i in inputListOrDict.keys():
            found = re.findall(search.lower(), i.lower())
            if found:
                key.append(i)
                return key, found
        stuff = inputListOrDict.values()
    else: stuff = inputListOrDict
    for i in stuff:
        if type(i) in (list, dict):
            key , found = rece(search, i, found, key)
        elif type(i) == str:
             found = re.findall(search.lower(), i.lower())
        if found:
            if type(inputListOrDict) == dict:
                key.append(list(inputListOrDict.keys())[f])
                return key, found
            elif type(inputListOrDict) == list:
                key.append(f)
                return key, found
        f += 1
    return key, found

def findInList(search:str, inputListOrDict:list or dict, found = 0, key= None) -> list:
    return rece(search, inputListOrDict, found, key)[0][::-1]






