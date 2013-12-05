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


def getSubModuleFromString(parent, subModuleString):
    """
    Get the submodule from the parent module
    parent:  a python module
    subModuleString:  a 'dot-notated' sub-module string (i.e. "module1.class1")
    """
    moduleList = subModuleString.split(".")
    subMod = getattr(parent, moduleList[0])
    if len(moduleList) == 1:
        return subMod
    else:
        return getSubModuleFromString(subMod, ".".join(moduleList[1:]))


def random_network_nodes(num, initId, weight_factor):
    from np.lib import network as net
    import numpy
    import itertools as iter
    ids = range(initId, initId + num)
    xs = numpy.random.rand(num)
    ys = numpy.random.rand(num)
    ws = numpy.random.rand(num) * weight_factor
    nodes = [net.Node(node_id, (x, y), (x, y), w) for node_id, x, y, w in iter.izip(ids, xs, ys, ws)]
    return nodes

def random_ds_nodes(num, metric_factor):
    from np.lib import dataset_store as ds
    import numpy
    import itertools as iter
    xs = numpy.random.rand(num)
    ys = numpy.random.rand(num)
    ms = numpy.random.rand(num) * metric_factor
    nodes = [ds.Node((x, y), (x, y), {}) for x, y in iter.izip(xs, ys)]
    for node, m in iter.izip(nodes, ms):
        node.metric = m 
    return nodes
    


