
# -*- coding:utf-8 -*-

import flask

from Utils.io_bs import item_to_map


class LogicBase(object):
    """ Basic class of logic
    """
    def __init__(self):
        self._items = None
        self._content = None
        self._id_route = None

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, val):
        self._items = val

    def toJson(self):
        """ Convert the items to json format
        :return:
        """
        res = {}
        ii = 0
        for item in self._items:
            m = item_to_map(item)
            if m is None:
                continue
            ii += 1
            res[ii] = m
        return flask.jsonify(res)




