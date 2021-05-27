from pprint import pprint

from parse_ingredient.grammar import Grammar


class Quantity:
    def __init__(self, quantity=None, uom=None):
        self.quantity = quantity
        self.uom = uom

    def postprocess(self):
        if self.quantity is None and self.uom is None:
            return
        if self.quantity is None:
            self.quantity = 1
        if self.uom is None:
            self.uom = 's'

        if self.uom == 'mg':
            self.quantity /= 1000
            self.uom = 'g'
        elif self.uom == 'g':
            pass
        elif self.uom == 'kg':
            self.quantity *= 1000
            self.uom = 'g'
        elif self.uom == 'ml':
            pass
        elif self.uom in ['litre', 'ltr', 'litres']:
            self.quantity *= 1000
            self.uom = 'ml'
        elif self.uom in ['s', 'each']:
            self.uom = 's'
        elif self.uom in ['tbsp', 'tsp', 'tablespoon']:
            self.uom = 'small'
        elif self.uom == 'pinch':
            self.uom = 'small'
        else:
            self.quantity = None
            self.uom = None


def merge_quantity(res, tmp):
    def merge_items(a, b):
        if a is None:
            return b
        elif b is None:
            return a
        else:
            return None

    return Quantity(quantity=merge_items(res.quantity, tmp.quantity),
                    uom=merge_items(res.uom, tmp.uom))


def parse_quantity_json(quantity_json):
    assert len(quantity_json.keys()) == 1
    key = list(quantity_json.keys())[0]
    if key == "UOM":
        return Quantity(quantity=None, uom=quantity_json[key][0]['terminal'])
    elif key == "UOMCOOK":
        if len(quantity_json[key]) == 1:
            return Quantity(quantity=None, uom=quantity_json[key][0]['terminal'])
        else:
            return parse_quantity_json(quantity_json[key][1])
    elif key == "UOMCOOKMODIF":
        return Quantity(quantity=None, uom=None)
    elif key == "DISCRETE":
        return Quantity(quantity=None, uom=quantity_json[key][0]['terminal'])
    elif key == "NUMBER":
        if len(quantity_json[key]) == 1:
            if quantity_json[key][0].keys() == {'default'}:
                return Quantity(quantity=float(quantity_json[key][0]['default']), uom=None)
            elif quantity_json[key][0].keys() == {'SPECIALNUMBER'}:
                return parse_quantity_json(quantity_json[key][0])
        else:
            v1 = parse_quantity_json(quantity_json[key][0])
            v2 = parse_quantity_json(quantity_json[key][1])
            if v1.quantity is not None and v2.quantity is not None:
                return Quantity(quantity=v1.quantity / v2.quantity, uom=None)
    elif key == "DENOMINATOR":
        return parse_quantity_json(quantity_json[key][1])
    elif key == "SPECIALNUMBER":
        vals = {'½': 1 / 2, '¼': 1 / 4, '¾': 3 / 4, '⅓': 1 / 3, '⅛': 1 / 8}
        return Quantity(quantity=vals[quantity_json[key][0]['terminal']], uom=None)
    elif key == "MODIFIER":
        return Quantity(quantity=None, uom=None)
    elif key == "QUANTITY":
        if quantity_json[key][0].keys() == {'XNUMBER'}:
            v1 = parse_quantity_json(quantity_json[key][0])
            v2 = parse_quantity_json(quantity_json[key][1])
            if v2.quantity is not None:
                return Quantity(v1.quantity * v2.quantity, v2.uom)
            else:
                return v2
        else:
            res = Quantity(quantity=None, uom=None)
            for item in quantity_json[key]:
                tmp = parse_quantity_json(item)
                res = merge_quantity(res, tmp)
            return res
    elif key == "XNUMBER":
        return parse_quantity_json(quantity_json[key][0])
    elif key == "OTHER":
        if quantity_json[key][0]['terminal'] == 'per kg':
            return Quantity(quantity=1.0, uom='g')
        elif quantity_json[key][0]['terminal'] == 'each':
            return Quantity(quantity=1.0, uom='s')
        elif quantity_json[key][0]['terminal'] in ['a pinch of', 'pinch', 'pinch of']:
            return Quantity(quantity=1.0, uom='pinch')
    elif key == "CONTAINER":
        return Quantity(quantity=None, uom=None)
    elif key == "ITEM":
        return parse_quantity_json(quantity_json[key][0])
    elif key == "RESULT":
        return parse_quantity_json(quantity_json[key][0])


grammar = Grammar('../parse_ingredient/grammar.txt')


def retrieve_quantity(quantity_str):
    if quantity_str is None:
        return Quantity(quantity=None, uom=None)
    data = grammar.parse(quantity_str)
    if len(data) == 0:
        return Quantity(quantity=None, uom=None)
    val = parse_quantity_json(data[0][0])
    val.postprocess()
    return val
