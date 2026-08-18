"""Source position tracker – stores file, line, column, and index for error reporting."""


class Position:
    __slots__ = ("index", "line", "column", "filename", "file_text")

    def __init__(self, index, line, column, filename, file_text=None):
        self.index = index
        self.line = line
        self.column = column
        self.filename = filename
        self.file_text = file_text

    def detach_source(self):
        self.file_text = None
        return self

    def advance(self, current_character=None):
        self.index += 1
        self.column += 1

        if current_character == "\n":
            self.line += 1
            self.column = 0

        return self

    def copy(self):
        return Position(
            self.index, self.line, self.column, self.filename, self.file_text
        )
