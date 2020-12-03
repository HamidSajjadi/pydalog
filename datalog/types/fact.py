from . import Predicate, Literal, Variable


class Fact(Literal):

    def __init__(self, predicate: Predicate = None, name: str = None, args: list = None):

        for const in args:
            if Variable.is_variable(const):
                raise TypeError('fact can not have variable')

        super().__init__(predicate, name, args)
