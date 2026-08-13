"""Interpreter construction: dispatch cache, instruction budget, binary operator table."""


class InterpreterCore:
    def __init__(self, instruction_limit=None):
        self.dispatch_cache = {}
        self.instruction_limit = instruction_limit
        self._binary_operator_dispatch = self._build_binary_operator_dispatch()
