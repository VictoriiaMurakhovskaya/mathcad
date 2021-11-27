import pathlib
import json
import numpy as np

PATH = 'data/limits.json'


def import_limits():
    file_path = pathlib.Path(__file__).parents[0].resolve() / PATH
    with open(file_path, 'r') as f:
        json_dict = json.load(f)

    numpy_dict = {}
    for k, v in json_dict.items():
        numpy_dict.update({k: [-np.inf if v[0] == '-inf' else v[0],
                               np.inf if v[1] == '+inf' else v[1]]})

    return numpy_dict


values_limits = import_limits()



