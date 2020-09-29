import json

path = "./"
a = {
    "awaiting":[],
    "finished":[]
}

with open(path + 'hotKeyword.txt', 'w+') as f:
    #print(f.read())
    print(str(a))
    a = json.dumps(a, ensure_ascii=False)
    print(a)
    f.write(str(a))
    f.closed