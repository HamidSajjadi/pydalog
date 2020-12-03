from datalog.types import Literal, Variable, Fact, Rule, Constant, Predicate
from datalog import Datalog


def run():
    pred = Predicate('father', 2)
    literal = Literal(predicate=pred, args=['X', 'y'])
    print(literal)

    program = Datalog() \
        .add_literal('father',['X', 'Y']) \
        .add_fact('father', ['ali', 'hossein'])

    print(program.get_predicates())


if __name__ == '__main__':
    run()
