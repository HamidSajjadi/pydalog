class InvalidPredicateError(Exception):

    def __init__(self, title: str, message: str):
        error_message = 'Error in predicate {}. {}'.format(title, message)
        super(InvalidPredicateError, self).__init__(error_message)


class RangeRuleError(Exception):
    def __init__(self, title: str):
        error_message = 'Error in rule {}. {}'.format(title,
                                                      'Every variable in rule head should appear in at least one of '
                                                      'the predicates in body')
        super(RangeRuleError, self).__init__(error_message)
