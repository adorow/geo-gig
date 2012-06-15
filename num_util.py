
def parse_num(s):
    "Parses a string into a number. If the string is not a number, None is returned."
    try:
        return float(s)
    except ValueError:
        return None