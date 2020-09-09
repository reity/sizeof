"""Function for measuring memory usage of objects.

Simple function for measuring the size in memory of
common Python data structures.
"""

from __future__ import annotations
import doctest
import sys
import struct
import collections

def arch():
    """
    Determine the architecture.

    >>> arch() in [32, 64]
    True
    """
    return struct.calcsize("P") * 8

def sizeof(obj, deep=False, _exclude=None):
    """
    Estimate the memory consumption of a Python object (either
    the root object itself exclusively or, in the case of a deep
    traversal, the entire tree of objects reachable from it).

    >>> sys.getsizeof([]) == sizeof([])
    True
    >>> sys.getsizeof(123) == sizeof(123)
    True
    >>> sizeof('ab') == sizeof('a') + 1
    True
    >>> xs = [1, 2, 3]
    >>> ys = {'a':1, 'b':2, 'c':3}
    >>> zs = {frozenset([1, 2, 3]): [1, 2, 3], frozenset(['a']): 'bc'}
    >>> sys.getsizeof(xs) == sizeof(xs)
    True
    >>> sys.getsizeof(xs) < sizeof(xs, deep=True)
    True
    >>> sizeof([xs], deep=True) > sys.getsizeof([xs])
    True
    >>> sizeof([xs, ys, zs], deep=True) > 2 * sizeof([xs, xs, xs], deep=True)
    True
    >>> sizeof([xs, xs], deep=True) < sizeof([xs, [1, 2, 3]], deep=True)
    True
    >>> sizeof([xs], deep=True, _exclude=set([id(xs)])) == sizeof([xs])
    True
    """
    if not deep or isinstance(obj, (str, bytes, bytearray, int, float)):
        return sys.getsizeof(obj)

    _exclude = set() if _exclude is None else _exclude

    if id(obj) in _exclude:
        return 0

    if isinstance(obj, collections.abc.Mapping):
        _exclude.add(id(obj))
        iterator = obj.items() if isinstance(obj, dict) else obj.iteritems()
        return sys.getsizeof(obj) + sum(
            sizeof(k, deep=True, _exclude=_exclude) +\
            sizeof(v, deep=True, _exclude=_exclude)
            for (k, v) in iterator
        )

    if isinstance(obj, collections.abc.Container):
        _exclude.add(id(obj))
        return sys.getsizeof(obj) + sum(
            sizeof(v, deep=True, _exclude=_exclude)
            for v in obj
        )

    raise ValueError( # pragma: no cover
        'object not supported by current version of sizeof'
    )

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
