from collections.abc import Collection
from math import e, modf, floor, sqrt
from itertools import filterfalse, chain
from copy import copy
import unittest


# DO NOT CHANGE ANY CODE BETWEEN LINE X AND LINE Y
# ******* THIS IS LINE X ******************

GOLDEN = (1.0 + 5.0 * 0.5) / 2.0


def swap(a, b):
    return b, a


# ***************************************************
# why do we inherit from Collection rather than Set?
# because Set requires too many methods to be defined


class CuckooSet(Collection):

    # *** course helper routines *******
    def _hash2_(self, obj, table_size):
        try:
            h = hash(obj)  # may raise exception
        except Exception:
            raise TypeError("unhashable key")

        h %= table_size

        f1, _ = modf(h * e)
        f2, _ = modf(h * GOLDEN)
        h1 = floor(table_size * f1)
        h2 = floor(table_size * f2)
        if h1 == h2:
            h2 = (h2 + 7) % table_size
        return h1, h2

    def _members_(self, tab):  # returns iterator
        return filterfalse((lambda x: x is None), tab)

    def _allmembers_(self):
        return chain(self._members_(self.htab1), self._members_(self.htab2))

    # ** course methods ****

    def __init__(self, iter=[], *, s=128):
        if s < 4:
            raise ValueError("set size too small")
        self._size_ = s
        self._MAXSWAPS_ = floor(s * 0.6)
        self.htab1 = [None] * s
        self.htab2 = [None] * s
        for i in iter:
            self.add(i)

    def __len__(self):
        count1 = len(list(self._members_(self.htab1)))
        count2 = len(list(self._members_(self.htab2)))
        return count1 + count2

    def _resize_(self):
        oldself = copy(self)
        self.__init__(oldself, s=oldself._size_ * 2)

    def __str__(self):
        fstr = ""
        for v in self._allmembers_():
            if len(fstr):
                fstr += ", "
            fstr += str(v)
        return fstr

    def __iter__(self):
        return self._allmembers_()
# ******* THIS IS LINE Y ******************

    def __contains__(self, x):
        if x is None:
            raise ValueError("key may not be None")

        (hash0, hash1) = self._hash2_(x, self._size_)
        return self.htab1[hash0] == x or self.htab2[hash1] == x

    def add(self, x):
        # Check if element already exists (prevent duplicates)
        if x in self:
            return  # Element already exists, no need to add
            
        copy = x
        try:
            hash0, hash1 = self._hash2_(copy, self._size_)
        except Exception:
            # only have to raise error once because everything else is hashable by default
            raise TypeError("unhashable key")

        counter = 0
        while True:
            if self.htab1[hash0] is None:
                self.htab1[hash0] = copy
                return True

            copy, self.htab1[hash0] = swap(copy, self.htab1[hash0])
            hash0, hash1 = self._hash2_(copy, self._size_)

            if self.htab2[hash1] is None:
                self.htab2[hash1] = copy
                return True

            copy, self.htab2[hash1] = swap(copy, self.htab2[hash1])
            hash0, hash1 = self._hash2_(copy, self._size_)
            counter += 1

            if counter == self._MAXSWAPS_:
                counter = 0
                self._resize_()

    def remove(self, x):
        if x is None:
            raise ValueError("key may not be None")

        if x not in self:
            # not sure what type of error we're supposed to raise
            raise ValueError("key is not in table")

        self.discard(x)

    def discard(self, x):
        if x is None:
            raise ValueError("key may not be None")

        hash0, hash1 = self._hash2_(x, self._size_)
        if self.htab1[hash0] == x:
            self.htab1[hash0] = None
        elif self.htab2[hash1] == x:
            self.htab2[hash1] = None
