from __future__ import annotations

from typing import Dict, List, Union

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

    def add_literal(self, literal: Union[str, Literal] = None, *args) -> Datalog:
        if not literal:
            raise Exception('Provide either and literal object, or a name for the literal')
        if not isinstance(literal, Literal):
            print(*args)
            literal = Literal(literal, *args)
        literal_pred = literal.predicate()
        self.__add_or_get_predicate(literal_pred)
        self.__literals.append(literal)
        return self

    def add_fact(self, fact: Union[str, Fact] = None, *args) -> Datalog:
        if not fact:
            raise Exception('Provide either and literal object, or a name for the fact')
        if not isinstance(fact, Fact):
            fact = Fact(fact, *args)
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

    def add_rule(self, head: Union[tuple, Literal], body: tuple, label: str = None):
        if not label:
            label = 'r' + str(len(self.__rules) + 1)
        head_as_literal = head if isinstance(head, Literal) else Literal(head[0], head[1:])
        bodies_as_literal = [b if isinstance(b, Literal) else Literal(b[0], b[1:]) for b in body]
        rule = Rule(label, head=head_as_literal, body=bodies_as_literal)
        self.__rules.append(rule)
        return self

    def __str__(self):
        final_string = ''
        if len(self.__facts):
            final_string += ',\n'.join([fact.__str__() for fact in self.__facts]) + '\n'
        if len(self.__literals):
            final_string += ',\n'.join([literal.__str__() for literal in self.__literals]) + '\n'
        if len(self.__rules):
            final_string += ',\n'.join(rule.__str__() for rule in self.__rules) + '\n'

        return final_string
