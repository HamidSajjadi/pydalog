from __future__ import annotations
from typing import Dict, List

from .types import Predicate, Literal, Fact, Rule


class Datalog:
    __slots__ = ['__predicates_dict', '__facts', '__literals', '__rules']

    def __init__(self):
        self.__predicates_dict: Dict[str, Predicate] = {}
        self.__facts: List[Fact] = []
        self.__literals: List[Literal] = []
        self.__rules: List[Rule] = []

    def add_predicate(self, predicate: Predicate) -> Datalog:
        if predicate.name not in self.__predicates_dict.keys():
            self.__predicates_dict[predicate.name] = predicate
        else:
            self.__check_literal_arity(predicate)
        return self

    def add_literal(self, name: str = None, args: tuple = None, literal: Literal = None, ) -> Datalog:
        if not literal and not name:
            raise Exception('Provide either and literal object, or a name for the literal')
        if not literal:
            literal = Literal(name=name, args=args)
        literal_pred = literal.predicate()
        self.__add_or_get_predicate(literal_pred)
        self.__literals.append(literal)
        return self

    def add_fact(self, name: str = None, args: tuple = None, fact=None) -> Datalog:
        if not fact and not name:
            raise Exception('Provide either and literal object, or a name for the fact')
        if not fact:
            fact = Fact(name=name, args=args)
        fact.predicate()
        self.add_predicate(fact.predicate())
        self.__facts.append(fact)
        return self

    def get_predicates(self):
        return self.__predicates_dict

    def __check_literal_arity(self, literal):
        """
        check if a literal added to program, is compatible with a predicate added previously
        :param literal:
        :return:
        """
        pred = self.__predicates_dict[literal.name]
        if pred.arity != literal.arity:
            raise Exception('expected {} arity to be {}'.format(literal.name, literal.arity))

    def __add_or_get_predicate(self, predicate: Predicate):
        if predicate.name not in self.__predicates_dict.keys():
            self.__predicates_dict[predicate.name] = predicate
        else:
            predicate = self.__predicates_dict[predicate.name]
        return predicate
