import sys
import re
import io

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(50000)

if hasattr(sys, "setrecursionlimit"):
    sys.setrecursionlimit(2000)

from .runtime import SymbolTable, Context
from .values import Number, BuiltInFunction, List
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("INPUT", BuiltInFunction("INPUT"))
global_symbol_table.set("STR", BuiltInFunction("STR"))
global_symbol_table.set("INT", BuiltInFunction("INT"))
global_symbol_table.set("FLOAT", BuiltInFunction("FLOAT"))
global_symbol_table.set("BOOL", BuiltInFunction("BOOL"))


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    if result.should_return:
        return result.return_value, result.error

    return result.value, result.error


def is_complete(text):
    text = re.sub(r"#.*", "", text)

    temp_text = re.sub(r'""".*?"""', "", text, flags=re.DOTALL)
    if temp_text.count('"""') % 2 != 0:
        return False

    temp_text = re.sub(r"`[^`]*`", "", temp_text, flags=re.DOTALL)
    if temp_text.count("`") % 2 != 0:
        return False

    temp_text = re.sub(r'"[^"\\]*(\\.[^"\\]*)*"', "", temp_text)
    if temp_text.count('"') % 2 != 0:
        return False

    if temp_text.count("(") != temp_text.count(")"):
        return False
    if temp_text.count("[") != temp_text.count("]"):
        return False
    if temp_text.count("{") != temp_text.count("}"):
        return False

    depth = 0
    bracket_level = 0

    pattern = (
        r"(\[|\]|\b(DEF|CLASS|IF|WHILE|FOR|ENDEF|ENDCLASS|ENDIF|ENDWHILE|ENDFOR)\b)"
    )
    tokens = re.finditer(pattern, temp_text)

    start_keys = {"DEF", "CLASS", "IF", "WHILE"}
    end_keys = {"ENDEF", "ENDCLASS", "ENDIF", "ENDWHILE", "ENDFOR"}

    for match in tokens:
        token = match.group()

        if token == "[":
            bracket_level += 1
        elif token == "]":
            bracket_level -= 1

        elif token == "FOR":
            if bracket_level == 0:
                depth += 1

        elif token in start_keys:
            depth += 1

        elif token in end_keys:
            depth -= 1

    return depth <= 0


def main():
    GLADLANG_VERSION = "0.1.2"
    GLADLANG_HELP = f"""
Usage: gladlang [command] [filename] [args...]

Commands:
  <no arguments>           Start the interactive GladLang shell.
  [filename.glad]          Execute a GladLang script file.
  [filename.glad] [args]   Execute script and pass args to INPUT().
  --help                   Show this help message and exit.
  --version                Show the interpreter version and exit.
"""

    if len(sys.argv) == 1:
        print(f"Welcome to GladLang (v{GLADLANG_VERSION})")
        print("Type 'exit' or 'quit' to close the shell.")
        print("--------------------------------------------------")

        full_text = ""
        while True:
            try:
                prompt = "GladLang > " if not full_text else "...        > "
                line = input(prompt)

                if not full_text and line.strip().lower() in ("exit", "quit"):
                    break

                full_text += line + "\n"

                if is_complete(full_text):
                    if full_text.strip() == "":
                        full_text = ""
                        continue

                    result, error = run("<stdin>", full_text)

                    if error:
                        print(error.as_string())
                    elif result:
                        clean_text = re.sub(r"#.*", "", full_text).strip()

                        if clean_text.startswith("LET "):
                            pass
                        elif isinstance(result, Number) and result.value == 0:
                            pass
                        elif (
                            isinstance(result, List)
                            and len(result.elements) == 1
                            and result.elements[0].value == "NULL"
                        ):
                            pass
                        else:
                            print(result)

                    full_text = ""

            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                full_text = ""
                continue
            except EOFError:
                print("\nExiting.")
                break
            except Exception as e:
                print(f"Shell Error: {e}")
                full_text = ""

    elif len(sys.argv) >= 2:
        arg = sys.argv[1]

        if arg == "--help":
            print(GLADLANG_HELP)

        elif arg == "--version":
            print(f"GladLang v{GLADLANG_VERSION}")

        else:
            try:
                filename = arg

                script_args = sys.argv[2:]

                if script_args:
                    sys.stdin = io.StringIO("\n".join(script_args) + "\n")

                with open(filename, "r") as f:
                    text = f.read()

                result, error = run(filename, text)

                if error:
                    print(error.as_string(), file=sys.stderr)

            except FileNotFoundError:
                print(f"File not found: '{filename}'", file=sys.stderr)
            except Exception as e:
                print(f"An unexpected error occurred: {e}", file=sys.stderr)

    else:
        print("Error: Invalid arguments.")
        print(GLADLANG_HELP)


if __name__ == "__main__":
    main()
