"""Default illegal stubs for all Value protocol methods."""


class ValueProtocolStubs:
    __slots__ = ()

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def modded_by(self, other):
        return None, self.illegal_operation(other)

    def floordived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other, visited=None):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def execute(self, arguments, interpreter=None, calling_context=None):
        from gladlang.runtime.runtime_result import RuntimeResult

        return RuntimeResult().failure(self.illegal_operation())

    def get_attribute(self, name_token, context=None):
        return None, self.illegal_operation()

    def set_attribute(
        self, name_token, value, context=None, visibility=None, as_final=False
    ):
        return None, self.illegal_operation()

    def get_element_at(self, index):
        return None, self.illegal_operation()

    def set_element_at(self, index, value):
        return None, self.illegal_operation()

    def bitted_and_by(self, other):
        return None, self.illegal_operation(other)

    def bitted_or_by(self, other):
        return None, self.illegal_operation(other)

    def bitted_xor_by(self, other):
        return None, self.illegal_operation(other)

    def lshifted_by(self, other):
        return None, self.illegal_operation(other)

    def rshifted_by(self, other):
        return None, self.illegal_operation(other)

    def bitted_not(self):
        return None, self.illegal_operation()
