
# -*-encoding:utf-8-*-


def item_to_map(item):
    """ Convert item to map object
    :param item:
    :return:
    """
    if item is None:
        return {}

    res = {}
    keys = dir(item)
    for key in keys:
        # the internal attributes
        if key.startswith("_"):
            continue
        val = getattr(item, key)
        if val is not None:
            res[key] = val
    return res

















