
import itertools

def group_by(a_list, key=id):
    "This function receives a list of values, and stores everything in a dict, where the key is the value returned by the key function, and the value is a list of the values of the original list that have that same key."
    return dict([(k, list(values)) for k, values in itertools.groupby(sorted(a_list, key=key), key=key)])