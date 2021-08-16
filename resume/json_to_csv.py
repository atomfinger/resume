import json

import pandas as pd


def convert_to_csv(origin: str, output: str):
    with open(origin) as f:
        data = json.load(f)
    data = {'resume': data}
    df = pd.DataFrame.from_dict(data)
    df.to_csv(output, sep=";", header=True)
