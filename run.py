from datalog import Datalog


def run():
    # pred = Predicate('father', 2)
    # literal = Literal('father', 'X', 'Y')
    # fact = Fact('father', 'ali', 'hosein')
    # print(fact)
    # print(literal)
    program = Datalog() \
        .add_fact('father', 'ali', 'hossein') \
        .add_rule(head=('parent', 'X', 'Y'), body=(('father', 'X', 'Y'),))

    print(program)


if __name__ == '__main__':
    run()
