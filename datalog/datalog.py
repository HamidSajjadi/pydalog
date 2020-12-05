from __future__ import annotations

from typing import Dict, List, Union, Set, Iterable, TypedDict, Tuple

from .types import Predicate, Literal, Fact, Rule, Variable


class PredicateDictInterface(TypedDict):
    predicate: Predicate
    facts: Set[Fact]
    rules: Set[Rule]
    dependencies: Set[Predicate]
    dependants: Set[Predicate]


class Datalog:
    __slots__ = ['__predicates_dict', '__facts', '__literals', '__rules']

    def __init__(self):
        self.__predicates_dict: Dict[str, PredicateDictInterface] = {}
        self.__facts: Set[Fact] = set()
        self.__literals: List[Literal] = []
        self.__rules: List[Rule] = []

    def add_predicate(self, predicate: Predicate) -> Datalog:
        self.__add_or_get_predicate(predicate)
        return self

    def add_literal(self, literal: Union[str, Literal] = None, *args) -> Datalog:
        if not literal:
            raise Exception('Provide either and literal object, or a name for the literal')
        if not isinstance(literal, Literal):
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
        predicate = self.__add_or_get_predicate(fact.predicate())
        self.__add_fact(fact, predicate)
        return self

    def add_rule_object(self, rule: Rule):
        if rule not in self.__rules:
            self.__add_dependency(rule.head.predicate(), [b.predicate() for b in rule.body])
            if 'rules' not in self.__predicates_dict[rule.head.name]:
                self.__predicates_dict[rule.head.name]['rules'] = set()
            self.__predicates_dict[rule.head.name]['rules'].add(rule)
            self.__rules.append(rule)
        return self

    def add_rule(self, head: Union[tuple, Literal], body: tuple, label: str = None):
        if not label:
            label = 'r' + str(len(self.__rules) + 1)
        head_as_literal = head if isinstance(head, Literal) else Literal(head[0], *head[1:])
        head_pred = self.__add_or_get_predicate(head_as_literal)

        bodies_as_literal = []
        bodies_pred = []
        for b in body:
            b_literal = b if isinstance(b, Literal) else Literal(b[0], *b[1:])
            bodies_as_literal.append(b_literal)
            bodies_pred.append(self.__add_or_get_predicate(b_literal))
        bodies_as_literal = [b if isinstance(b, Literal) else Literal(b[0], *b[1:]) for b in body]

        self.__add_dependency(head_pred, bodies_pred)

        rule = Rule(label, head=head_as_literal, body=bodies_as_literal)
        self.__rules.append(rule)
        if 'rules' not in self.__predicates_dict[rule.head.name]:
            self.__predicates_dict[rule.head.name]['rules'] = set()
        self.__predicates_dict[rule.head.name]['rules'].add(rule)
        return self

    def match_rules(self, rules: Iterable[Rule]) -> List[Fact]:
        new_facts = []
        for rule in rules:
            answers, facts = self.match_rule(rule)
            new_facts.extend(facts)
        return new_facts

    def match_rule(self, rule: Rule) -> Tuple[List[Dict[Variable, str]], List[Fact]]:
        answers: List[Dict[Variable, str]] = []
        for i, literal in enumerate(rule.body):
            for fact in self.get_predicate_facts(literal.predicate()):
                temp_binding = fact.match(literal)
                if temp_binding:
                    match_found = True
                    for other_literal in rule.body[i:]:
                        if not fact.match(other_literal, temp_binding):
                            match_found = False
                            break
                    if match_found:
                        answers.append(temp_binding)
        new_facts = []
        for ans in answers:
            new_fact = Fact(rule.head.predicate(), *ans.values())
            if new_fact not in self.__facts:
                self.add_fact(new_fact)
                new_facts.append(new_fact)
        return answers, new_facts

    def extend_db(self):
        new_facts = self.match_rules(self.__rules)
        # print(new_facts)
        while len(new_facts):
            effected_rules = set()
            for fact in new_facts:
                effected_rules.update(self.__predicates_dict[fact.name]['rules'])
            temp_new = self.match_rules(effected_rules)
            new_facts = temp_new
            print("====")
            print(new_facts)
            print("==========")

    def get_predicate_facts(self, pred: Predicate) -> Set[Fact]:
        return self.__predicates_dict[pred.name]['facts']

    def get_predicate_dependencies(self, original_pred: Union[str, Predicate]) -> Iterable[Predicate]:

        ## check predicate exists in datalog predicates
        if not isinstance(original_pred, Predicate):
            if original_pred not in self.__predicates_dict.keys():
                raise Exception('predicate {} not found'.format(original_pred))
            pred = self.__predicates_dict[original_pred]['predicate']
        else:
            if original_pred.name not in self.__predicates_dict.keys():
                raise Exception('predicate {} not found'.format(original_pred))
            pred = original_pred

        if 'dependencies' in self.__predicates_dict[pred.name].keys():
            return self.__predicates_dict[pred.name]['dependencies']
        else:
            return []

    def predicates(self):
        return self.__predicates_dict

    def literals(self):
        return self.__literals

    def facts(self):
        return self.__facts

    def rules(self):
        return self.__rules

    def __check_literal_arity(self, literal):
        """
        check if a literal added to program, is compatible with a predicate added previously
        :param literal:
        :return:
        """
        pred = self.__predicates_dict[literal.name]['predicate']
        if pred.arity != literal.arity:
            raise Exception('expected {} arity to be {}'.format(literal.name, literal.arity))

    def __add_or_get_predicate(self, predicate: Union[Predicate, Literal]):
        if isinstance(predicate, Literal):
            predicate = predicate.predicate()
        elif not isinstance(predicate, Predicate):
            raise TypeError('Predicate type is not correct')
        if predicate.name not in self.__predicates_dict.keys():
            self.__predicates_dict[predicate.name] = {'predicate': predicate, 'rules': set(), 'facts': set(),
                                                      'dependencies': set(), 'dependants': set()}
        else:
            self.__check_literal_arity(predicate)
            predicate = self.__predicates_dict[predicate.name]['predicate']
        return predicate

    def __add_dependency(self, head_pred: Predicate, bodies_pred: List[Predicate]):

        if 'dependencies' in self.__predicates_dict[head_pred.name]:
            self.__predicates_dict[head_pred.name]['dependencies'].update(bodies_pred)
        else:
            self.__predicates_dict[head_pred.name]['dependencies'] = set(bodies_pred)

        for b in bodies_pred:
            if 'dependant' not in self.__predicates_dict[b.name]:
                self.__predicates_dict[b.name]['dependants'] = set()
            self.__predicates_dict[b.name]['dependants'].add(head_pred)

    def __add_fact(self, fact: Fact, predicate: Predicate):
        self.__facts.add(fact)
        if 'facts' in self.__predicates_dict[predicate.name].keys():
            self.__predicates_dict[predicate.name]['facts'].add(fact)
        else:
            self.__predicates_dict[predicate.name]['facts'] = {fact}

    def __str__(self):
        final_string = ''

        if len(self.__facts):
            list_of_facts = list(self.__facts)
            list_of_facts.sort()
            final_string += ',\n'.join([fact.__str__() for fact in list_of_facts]) + '\n'
        if len(self.__literals):
            list_of_literals = list(self.__literals)
            list_of_literals.sort()
            final_string += ',\n'.join([literal.__str__() for literal in list_of_literals]) + '\n'
        if len(self.__rules):
            final_string += ',\n'.join(rule.__str__() for rule in self.__rules) + '\n'

        return final_string
