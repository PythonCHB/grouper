
from operator import itemgetter
from collections.abc import Mapping
import heapq

# extra methods to tack on to set to make it "act" like a list.
extra_set_methods = {"append": lambda self, value: self.add(value),
                     "extend": lambda self, sequence: self.update(set(sequence))}


class Grouping(dict):
    """
    Dict subclass for grouping elements of a sequence.

    The values in the dict are a list of all items that have
    corresponded to a given key

    essentially, adding a new item is the same as:

    dict.setdefault(key, []).append(value)

    In other words, for each item added:

    grouper['key'] = 'value'

    If they key is already there, the value is added to the corresponding list.

    If the key is not already there, a new entry is added, with the key as the
    key, and the value is a new list with the single entry of the value in it.

    The __init__ (and update) can take either a mapping of keys to lists,
    or an iterable of items.
    """

    def __init__(self, iterable=(), key_fun=None, value_fun=None):
        """
        Create a new Grouping object.

        :param iterable: an iterable or mapping with initial data.

        :param key_fun=None: key function -- if specified, then the key will be
                             whatever the function returns for each item in the
                             iterable.

        :param value_fun=None: value function -- if specified, then the value
                               will be whatever the function returns for each
                               item in the iterable.

         If neither key_fun nor value_fun are specified, then the items in the
         iterable are processes as (key, value) pairs. (item[0], item[1]))

         If only a key_fun is specified, then the value is the entire item.

         If only a value_fun is specified, then the key is item[0]

        """
        if key_fun is None:
            self.key_fun = itemgetter(0)
            if value_fun is None:
                self.value_fun = itemgetter(1)
            else:
                self.value_fun = value_fun
        else:
            self.key_fun = key_fun
            if value_fun is None:
                self.value_fun = lambda x: x
            else:
                self.value_fun = value_fun


        super().__init__()
        self.update(iterable)

    # Override a few dict methods
    def __setitem__(self, key, value):
        self.setdefault(key, list()).append(value)

    def __repr__(self):
        return f"Grouping({super().__repr__()})"

    def add(self, item):
        """
        add a new item to the grouping the key_fun and value_fun
        used when crating teh gropuing will be used.
        """
    @classmethod
    def fromkeys(cls, iterable):
        return cls(dict.fromkeys(iterable, list()))

    def update(self, iterable=(), key=None):
        '''Extend groups with elements from an iterable or with
        key-group items from a dictionary or another Grouping instance.

        The ``key`` function is ignored for dictionaries and Groupings.

            >>> g = Grouping('AbBa', key=str.casefold)
            >>> g.update(['apple', 'banana'], key=lambda s: s[0])
            >>> g['a']
            ['A', 'a', 'apple']

        '''
        if isinstance(iterable, Mapping):
            for k, g in iterable.items():
                self.setdefault(k, list()).extend(g)
        else:
            for item in iterable:
                self[self.key_fun(item)] = self.value_fun(item)

    def map(self, func):
        """
        Apply a function to each element in every group.
        """
        return {k: [func(v) for v in g] for k, g in self.items()}

    def aggregate(self, func):
        """
        Apply a function to each group.

            >>> g = Grouping(((c.casefold(), c) for c in 'AbBaAa'))
            >>> g.aggregate(''.join)    # concatenate
            {'a': 'AaAa', 'b': 'bB'}
            >>> g.aggregate(set)        # uniques
            {'a': {'A', 'a'}, 'b': {'B', 'b'}}
            >>> g.aggregate(Counter)    # counts
            {'a': Counter({'A': 2, 'a': 2}), 'b': Counter({'B': 1, 'b': 1})}

        Grouping.aggregate behaves similarly to the "map-reduce"
        pattern of programming.

            Grouping(iterable).aggregate(reducer)

        """
        return {k: func(g) for k, g in self.items()}

    def most_common(self, n=None):
        '''List the ``n`` largest groups from largest to smallest.  If
        ``n`` is ``None``, then list all groups.
        '''
        keyfunc = lambda item: len(item[1])
        if n is None:
            return sorted(self.items(), key=keyfunc, reverse=True)
        return heapq.nlargest(n, self.items(), key=keyfunc)




