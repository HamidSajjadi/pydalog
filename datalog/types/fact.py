from typing import Union

from . import Literal, Variable, Predicate


class Fact(Literal):

    def __init__(self, name: Union[Predicate, str], *args):

        for arg in args:
            if Variable.is_variable(arg):
                raise TypeError('fact can not have variable')

        super().__init__(name, *args)
