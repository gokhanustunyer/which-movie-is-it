
def encode(lst):
    if isinstance(lst, list) or isinstance(lst ,tuple):
        lst = list(lst)
        return " ".join([str(l) for l in lst])
    else:
        raise Exception(
            'Unexpected data type {}'.format(type(lst)))


def decode(lst):
    if isinstance(lst, str):
        return lst.split(' ')
    else:
        raise Exception(
            'Unexpected data type {}'.format(type(lst)))


def tuple_dict(_tuple,reverse=False):
    if type(_tuple) != tuple : return 'Argument must be tuple'
   
    if reverse : 
        return {item[1]:item[0] for item in _tuple if type(item[0]) != float or type(item[0]) != int}
    else:
        return {item[0]:item[1] for item in _tuple if type(item[0]) != float or type(item[0]) != int}
