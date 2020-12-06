# pydalog
Python implementation of a very basic, inefficient datalog


## Example

#### Create Datalog Program

```python
from datalog import Datalog

program = Datalog() \
        .add_fact('mother', 'sara', 'akbar') \
        .add_fact('mother', 'soghra', 'sara') \
        .add_fact('father', 'ahmad', 'akbar') \
        .add_rule(head=('parent', 'X', 'Y'), body=(('father', 'X', 'Y'),)) \
        .add_rule(head=('parent', 'X', 'Y'), body=(('mother', 'X', 'Y'),)) \
        .add_rule(head=('married', 'X', 'Y'), body=(('mother', 'X', 'Z'), ('father', 'Y', 'Z'))) \
        .add_rule(head=('married', 'Y', 'X'), body=(('married', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Z'), ('parent', 'Z', 'Y')))
```

#### Query Program
Compile the program and fetch new rules using `extend_db()` function
```python
program.extend_db()
```

Query facts with `query(literal)` function. If the literal is a `Fact` (arguments are all constant and not variable) returns a boolean indicating whether this fact is true or not.

If literal is not a fact and has some variables, returns the binding that will make a correct fact from the given literal
```python
program.query('descendant', 'X', 'akbar') # returns [{X: 'sara'}, {X: 'ahmad'}, {X: 'soghra'}]
program.query('married', 'sara', 'ahmad') # returns True
program.query('married', 'sara', 'akbar') # returns False

```

#### Built-In Literals
some arithmetic operators are built in
`=`, `!=`, `<`, `<=`, `>`, `>=`

`=`, `!=` can compare anything. But other built-ins need float as their arguments.

usage:
```python
from datalog.types import Eq, Lt, Gt, Lte, Neq

       program()\
       .add_rule(head=('child', 'X'), body=(('age', 'X', 'Y'), Lt('Y', 12))) \

```






look and run `run.py` for more details

