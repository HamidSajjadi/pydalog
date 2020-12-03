from .predicate import Predicate
from .variable import Variable

class Fact(Predicate):
    __slots__ = ['predicate', 'constants']

    def __init__(self, predicate: Predicate, constants: list = None):
        def not_correct_arity():
            return (predicate._arity and not constants) or (predicate._arity != len(constants))

        if not_correct_arity():
            raise Exception('arity and number of constants are not compatible')

        for const in constants:
            if isinstance(const, Variable):
                raise TypeError('fact can not have variable')

        super().__init__(predicate.name, constants)
