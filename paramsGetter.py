import json


def getParams():
    params = {}
    try:
        with open('params.json', 'r', encoding='utf-8') as f:
            params = json.load(f)
    except IOError as error:
        print(error)
    except Exception as error:
        print(error)
    return params
