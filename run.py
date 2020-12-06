from datalog import Datalog
from datalog.types import Eq, Lt, Gt, Lte, Neq


def create_program() -> Datalog:
    return Datalog() \
        .add_fact('mother', 'sara', 'akbar') \
        .add_fact('mother', 'soghra', 'sara') \
        .add_fact('father', 'ahmad', 'akbar') \
        .add_fact('dead', 'ahmad') \
        .add_fact('age', 'akbar', 12) \
        .add_fact('age', 'asghar', 16) \
        .add_rule(head=('child', 'X'), body=(('age', 'X', 'Y'), Lt('Y', 12))) \
        .add_rule(head=('not_sixteen', 'X'), body=(('age', 'X', 'Y'), Neq('Y', 16))) \
        .add_rule(head=('teen', 'X'), body=(('age', 'X', 'Y'), Gt('Y', 12), Lte('Y', 16))) \
        .add_rule(head=('orphan', 'Y'), body=(('father', 'X', 'Y'), ('dead', 'Z'), Eq('Z', 'X'))) \
        .add_rule(head=('parent', 'X', 'Y'), body=(('father', 'X', 'Y'),)) \
        .add_rule(head=('parent', 'X', 'Y'), body=(('mother', 'X', 'Y'),)) \
        .add_rule(head=('married', 'X', 'Y'), body=(('mother', 'X', 'Z'), ('father', 'Y', 'Z'))) \
        .add_rule(head=('married', 'Y', 'X'), body=(('married', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Z'), ('parent', 'Z', 'Y')))


def run_extend_db():
    program = create_program()
    program.extend_db()
    print(program)


def run_query():
    program = create_program()
    print(program.query('descendant', 'X', 'akbar'))
    print(program.query('married', 'sara', 'ahmad'))
    print(program.query('married', 'sara', 'akbar'))


if __name__ == '__main__':
    run_extend_db()
    # run_query()
