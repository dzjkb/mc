import copy


class List(list):
    def __init__(self, args=[]):
        super(List, self).__init__(args)

    def map(self, func):
        return List([func(item) for item in self])

    def flat_map(self, func):
        return List([r for item in self for r in func(item)])

    def filter(self, func):
        return List([item for item in self if func(item)])

    def multiproc_map(self, func):
        from pathos.multiprocessing import Pool
        pool = Pool()
        result = List(pool.map(func, self))
        pool.close()
        pool.join()
        return result

    def fold(self, func, initial_value):
        value = copy.deepcopy(initial_value)
        for item in self:
            value = func(value, item)
        return value

    def reduce(self, func):
        from mc.option import Some, Nothing
        if self.is_empty():
            return Nothing()
        else:
            value = self[0]
            for item in self[1:]:
                value = func(value, item)
            return Some(value)

    def is_empty(self):
        return len(self) == 0

    def group_by(self, func):
        dictionary = {}
        from mc.dict import Dict
        for item in self:
            val = func(item)
            if val not in dictionary:
                dictionary[val] = List()
            dictionary[val].append(item)
        return Dict(dictionary)

    def foreach(self, func):
        for item in self:
            func(item)

    def sorted(self, key=None):
        return List(sorted(self, key=key))

    def to_dict(self):
        from mc.dict import Dict
        return Dict({i[0]: i[1] for i in self})

    def to_set(self):
        from mc.set import Set
        return Set(self)

    def mk_string(self, sep=", ", left="", right=""):
        return left + sep.join([str(item) for item in self]) + right

    def __add__(self, other):
        return List(list(self) + list(other))
