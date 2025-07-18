from json import load, dump

def openHistory(id):
    with open(f"context/{id}.json", 'r') as file:
        try:
            return load(file)
        except Exception as e:
            return None

def putHistory(id, prompt, result):
    data = {
        "user": prompt,
        "model": result
    }
    fetch = openHistory(id)
    AllData = []
    if not fetch is None:
        AllData = fetch
    AllData.append(data)
    with open(f"context/{id}.json", 'w') as file:
        dump(AllData, file, indent=4)

def createHistory(id):
    with open(f"context/{id}.json", 'w'):
        pass