from datalog import Datalog


def run():
    # pred = Predicate('father', 2)
    # literal = Literal('father', 'X', 'Y')
    # fact = Fact('father', 'ali', 'hosein')
    # print(fact.match(literal, {'Z': 'ebi'}))
    # exit(0)
    # print(fact)
    # print(literal)
    program = Datalog() \
        .add_fact('mother', 'sara', 'hamid') \
        .add_fact('mother', 'soghra', 'sara') \
        .add_rule(head=('parent', 'X', 'Y'), body=(('father', 'X', 'Y'),)) \
        .add_rule(head=('parent', 'X', 'Y'), body=(('mother', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Z'), ('parent', 'Z', 'Y')))
        # .add_fact('father', 'ali', 'hossein') \

    program.extend_db()
    print(program)


if __name__ == '__main__':
    run()
