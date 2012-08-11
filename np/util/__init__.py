import collections

def flatten_to_tuples(d, accum_tuple=()):
    if(type(d)==dict):
        for key in d.keys(): 
            for val in flatten_to_tuples(d[key], accum_tuple + (key,) if accum_tuple else (key,)):
                yield val
    else:
        yield accum_tuple + (d,) 

def flatten(d, prefix):
    if(type(d)==dict):
        for key in d.keys(): 
            for val in flatten(d[key], "%s, %s" % (prefix, key) if prefix else key):
                yield val
    else:
        yield prefix


def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
            return d

