from re import sub


def convert_to_camel_case(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", " ")
    return ''.join([s[0], s[1:]])
