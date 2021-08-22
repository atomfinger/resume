import json


def simplify(origin: str, destination: str):
    with open(origin, 'r') as f:
        resume = json.loads(f.read())
    resume['basics']['location'] = None
    resume['interests'] = None
    with open(destination, 'w+') as f:
        f.write(json.dumps(resume))
