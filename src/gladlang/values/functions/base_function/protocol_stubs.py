"""Default illegal operation stubs for BaseFunction subclasses."""


class BaseFunctionProtocolStubs:
    __slots__ = ()

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

    def notted(self):
        return None, self.illegal_operation()
