class Constant:
    __slots__ = ['_value']

    def __init__(self, value):
        if not value:
            raise Exception('Provide a name for variable')
        self._value = value

    def __str__(self) -> str:
        return self._value.__str__()
