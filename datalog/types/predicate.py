from __future__ import annotations


class Predicate:
    __slots__ = ['name', 'arity']

    def __init__(self, name, arity):
        self.name = name
        self.arity = arity

    def __eq__(self, other: Predicate):
        if not other or not isinstance(other, Predicate):
            return False

        if other.name != self.name:
            return False

        if other.arity != self.arity:
            return False

        return True

    def __to_string(self):
        return 'Predicate {}/{}'.format(self.name, self.arity)

    def __hash__(self):
        return hash('predicate' + self.name)

    def __repr__(self):
        return self.__to_string()

    def __str__(self):
        return self.__to_string()
