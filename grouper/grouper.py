
from collections import Counter
from collections.abc import Mapping
import heapq


# extra methods to tack on to set to make it "act" like a list.
extra_set_methods = {"append": lambda self, value: self.add(value),
                     "extend": lambda self, sequence: self.update(set(sequence))}


def counter_append(self, value):
    self[value] += 1


# extra methods to tack on to Mapping to make it "act" like a list.
extra_counter_methods = {"append": counter_append,
                         "extend": lambda self, sequence: self.update(sequence)}


class Grouping(dict):
    """
    Dict subclass for grouping elements of a sequence.

    The values in the dict are a list of all items that have
    corresponded to a given key

    essentially, adding an new item is the same as:

    dict.setdefault(key, []).append(value)

    In other words, for each item added:

    grouper['key'] = 'value'

    If they key is already there, the value is added to the corresponding list.

    If the key is not already there, a new entry is added, with the key as the
    key, and the value is a new list with the single entry of the value in it.

    The __init__ (and update) can take either a mapping of keys to lists,
    or an iterable of (key, value) tuples.

    If the initial data is not in exactly the form desired, an generator
    expression can be used to "transform" the input.

    For example:

        >>> Grouping(((c.casefold(), c) for c in 'AbBa'))
        Grouping({'a': ['A', 'a'], 'b': ['b', 'B']})
    """

    def __init__(self, iterable=(), *, collection=list):
        """
        Create a new Grouping object.

        :param iterable: an iterable or mapping with initial data.

        """
        if hasattr(collection, "append") and hasattr(collection, "extend"):
            self.collection = list
        elif hasattr(collection, "add") and hasattr(collection, "update"):
            # this is very kludgy -- adding append and extend methods to a
            # set or set-like object
            self.collection = type("appendset", (set,), extra_set_methods)
        # Counter is special
        elif issubclass(collection, Counter):
            # has an update, doesn't have an add -- a counter-like?
            self.collection = type("appendcounter", (Counter,), extra_counter_methods)
        else:
            raise TypeError("collection has to be a MutableSequence or set-like object")
        super().__init__()
        self.update(iterable)

    # Override a few dict methods

    def __setitem__(self, key, value):
        self.setdefault(key, self.collection()).append(value)

    def __repr__(self):
        return f"Grouping({super().__repr__()})"

    @classmethod
    def fromkeys(cls, iterable, v=()):
        return cls(dict.fromkeys(iterable, self.collection(v)))

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
                self.setdefault(k, self.collection()).extend(g)
        else:
            for k, g in iterable:
                self[k] = g

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




