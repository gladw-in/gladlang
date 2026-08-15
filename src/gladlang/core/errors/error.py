"""Base error class for all GladLang errors – stores position and message."""


class Error:
    def __init__(self, position_start, position_end, error_name, details):
        self.position_start = position_start
        self.position_end = position_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details}\n"
        result += (
            f"File {self.position_start.filename}, line {self.position_start.line + 1}"
        )
        return result
