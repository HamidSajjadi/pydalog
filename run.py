from datalog.types import Literal, Predicate, Fact


def run():
    pred = Predicate('father', 2)
    literal = Literal('father', 'X', 'Y')
    fact = Fact('father', 'ali', 'hosein')
    print(fact)
    print(literal)
    # program = Datalog() \
    #     .add_literal('father', 'X', 'Y') \
    #     .add_fact('father', ('ali', 'hossein')) \
    #     .add_rule(('parent', 'X', 'Y'), (('father'), ('X', 'Y')))
    #
    # print(program.get_predicates())


if __name__ == '__main__':
    run()
