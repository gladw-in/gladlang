from .constants import *
from .errors import Position, IllegalCharError, InvalidSyntaxError


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def peek(self):
        peek_pos = self.pos.idx + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def skip_comment(self):
        self.advance()

        while self.current_char != "\n" and self.current_char != None:
            self.advance()

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in " \t\r\n":
                self.advance()
            elif self.current_char == "#":
                self.skip_comment()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS + "_":
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == "+":
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "+":
                    tokens.append(
                        Token(TT_PLUSPLUS, pos_start=pos_start, pos_end=self.pos)
                    )
                    self.advance()
                else:
                    tokens.append(Token(TT_PLUS, pos_start=pos_start))

            elif self.current_char == "*":
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "*":
                    tokens.append(Token(TT_POW, pos_start=pos_start, pos_end=self.pos))
                    self.advance()
                else:
                    tokens.append(Token(TT_MUL, pos_start=pos_start))

            elif self.current_char == "/":
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "/":
                    tokens.append(
                        Token(TT_FLOORDIV, pos_start=pos_start, pos_end=self.pos)
                    )
                    self.advance()
                else:
                    tokens.append(Token(TT_DIV, pos_start=pos_start))

            elif self.current_char == "%":
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                self.advance()

            elif self.current_char == "^":
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()

            elif self.current_char == "-":
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "-":
                    tokens.append(
                        Token(TT_MINUSMINUS, pos_start=pos_start, pos_end=self.pos)
                    )
                    self.advance()
                else:
                    tokens.append(Token(TT_MINUS, pos_start=pos_start))
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "^":
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ",":
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == ".":
                tokens.append(Token(TT_DOT, pos_start=self.pos))
                self.advance()

            elif self.current_char == "[":
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "]":
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                self.advance()

            elif self.current_char == "!":
                tok, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(tok)
            elif self.current_char == "=":
                tokens.append(self.make_equals())
            elif self.current_char == "`":
                tokens += self.make_template_string()
            elif self.current_char == "<":
                tokens.append(self.make_less_than())
            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
            elif self.current_char == "{":
                tokens.append(Token(TT_LBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "}":
                tokens.append(Token(TT_RBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == ":":
                tokens.append(Token(TT_COLON, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_string(self):
        string = ""
        pos_start = self.pos.copy()
        self.advance()

        escape_character = False

        while self.current_char != None:
            if escape_character:
                if self.current_char == "n":
                    string += "\n"
                elif self.current_char == "t":
                    string += "\t"
                elif self.current_char == '"':
                    string += '"'
                elif self.current_char == "\\":
                    string += "\\"
                else:
                    string += self.current_char
                escape_character = False
            elif self.current_char == "\\":
                escape_character = True
            elif self.current_char == '"':
                break
            else:
                string += self.current_char
            self.advance()

        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + "_":
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, InvalidSyntaxError(pos_start, self.pos, "Expected '=' after '!'")

    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_EE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_template_string(self):
        tokens = []
        pos_start = self.pos.copy()
        self.advance()

        tokens.append(Token(TT_LPAREN, pos_start=pos_start))

        string_part = ""

        while self.current_char != None and self.current_char != "`":
            if self.current_char == "$" and self.peek() == "{":
                tokens.append(Token(TT_STRING, string_part, pos_start=pos_start))
                string_part = ""

                tokens.append(Token(TT_PLUS, pos_start=self.pos))

                tokens.append(Token(TT_IDENTIFIER, "STR", pos_start=self.pos))
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))

                self.advance()
                self.advance()

                expr_str = ""
                brace_count = 1
                while self.current_char != None and brace_count > 0:
                    if self.current_char == "{":
                        brace_count += 1
                    elif self.current_char == "}":
                        brace_count -= 1

                    if brace_count > 0:
                        expr_str += self.current_char
                        self.advance()

                sub_lexer = Lexer(self.fn, expr_str)
                sub_tokens, error = sub_lexer.make_tokens()

                if sub_tokens and sub_tokens[-1].type == TT_EOF:
                    sub_tokens.pop()

                tokens.extend(sub_tokens)

                tokens.append(Token(TT_RPAREN, pos_start=self.pos))

                tokens.append(Token(TT_PLUS, pos_start=self.pos))

                self.advance()

            else:
                string_part += self.current_char
                self.advance()

        tokens.append(Token(TT_STRING, string_part, pos_start=pos_start))

        tokens.append(Token(TT_RPAREN, pos_start=self.pos))

        self.advance()
        return tokens

    #

    def make_string(self):
        string = ""
        pos_start = self.pos.copy()

        is_multiline = False

        self.advance()

        if self.current_char == '"' and self.peek() == '"':
            is_multiline = True
            self.advance()
            self.advance()

        escape_character = False

        while self.current_char != None:
            if escape_character:
                if self.current_char == "n":
                    string += "\n"
                elif self.current_char == "t":
                    string += "\t"
                elif self.current_char == '"':
                    string += '"'
                elif self.current_char == "\\":
                    string += "\\"
                else:
                    string += self.current_char
                escape_character = False
            elif self.current_char == "\\":
                escape_character = True
            elif self.current_char == '"':
                if is_multiline:
                    if self.peek() == '"':
                        self.advance()
                        if self.peek() == '"':
                            self.advance()
                            break
                        else:
                            string += '""'
                    else:
                        string += '"'
                else:
                    break
            else:
                string += self.current_char

            self.advance()

        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)

    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
