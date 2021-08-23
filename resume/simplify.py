import json


def simplify(origin: str, destination: str):
    with open(origin, 'r') as f:
        resume = json.loads(f.read())
    resume['basics']['location'] = None
    resume['interests'] = None
    resume['projects'] = None
    resume['education'] = [resume['education'][0]]
    with open(destination, 'w+') as f:
        f.write(json.dumps(resume))
