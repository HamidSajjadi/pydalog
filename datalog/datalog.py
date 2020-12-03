from typing import Dict

from .types import Predicate, Literal, Fact


class Datalog:
    __slots__ = ['__predicate_map']

    def __init__(self):
        self.__predicate_map: Dict[Predicate, list] = {}

    def add_predicate(self, predicate: Predicate):
        if predicate not in self.__predicate_map.keys():
            self.__predicate_map[predicate] = []
        return self

    def __append_to_predicate(self, predicate, item):
        self.__predicate_map[predicate].append(item)

    def add_literal(self, name: str = None, args: list = None, literal: Literal = None, ):
        if not literal and not name:
            raise Exception('Provide either and literal object, or a name for the literal')
        if not literal:
            literal = Literal(name=name, args=args)
        pred = literal.predicate()
        self.add_predicate(pred)
        self.__append_to_predicate(pred, literal)
        return self

    def add_fact(self, name: str = None, args: list = None, fact=None):
        if not fact and not name:
            raise Exception('Provide either and literal object, or a name for the fact')
        if not fact:
            fact = Fact(name=name, args=args)
        pred = fact.predicate()
        self.add_predicate(pred)
        self.__append_to_predicate(pred, fact)
        return self

    def get_predicates(self):
        return self.__predicate_map
