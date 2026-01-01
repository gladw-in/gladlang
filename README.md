# GladLang

**GladLang is a dynamic, interpreted, object-oriented programming language.** This is a full interpreter built from scratch in Python, complete with a lexer, parser, and runtime environment. It supports modern programming features like closures, classes, inheritance, and robust error handling.

![Lines of code](https://sloc.xyz/github/gladw-in/gladlang)

This is the full overview of the GladLang language, its features, and how to run the interpreter.

## Table of Contents

- [About The Language](#about-the-language)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
    - [1. Installation](#1-installation)
    - [2. Usage](#2-usage)
    - [3. Running Without Installation (Source)](#3-running-without-installation-source)
    - [4. Building the Executable](#4-building-the-executable)
- [Language Tour (Syntax Reference)](#language-tour-syntax-reference)
    - [1. Comments](#1-comments)
    - [2. Variables and Data Types](#2-variables-and-data-types)
        - [Variables](#variables)
        - [Numbers](#numbers)
        - [Strings](#strings)
        - [Lists](#lists)
        - [Dictionaries](#dictionaries)
        - [Booleans](#booleans)
        - [Null](#null)
    - [3. Operators](#3-operators)
        - [Math Operations](#math-operations)
        - [Comparisons & Logic](#comparisons--logic)
        - [Increment / Decrement](#increment--decrement)
    - [4. Control Flow](#4-control-flow)
        - [IF Statements](#if-statements)
        - [WHILE Loops](#while-loops)
        - [FOR Loops](#for-loops)
    - [5. Functions](#5-functions)
        - [Named Functions](#named-functions)
        - [Anonymous Functions](#anonymous-functions)
        - [Closures](#closures)
        - [Recursion](#recursion)
    - [6. Object-Oriented Programming (OOP)](#6-object-oriented-programming-oop)
        - [Classes and Instantiation](#classes-and-instantiation)
        - [The `SELF` Keyword](#the-self-keyword)
        - [Inheritance](#inheritance)
        - [Polymorphism](#polymorphism)
    - [7. Built-in Functions](#7-built-in-functions)
- [Error Handling](#error-handling)
- [Running Tests](#running-tests)
- [License](#license)

-----

## About The Language

GladLang is an interpreter for a custom scripting language. It was built as a complete system, demonstrating the core components of a programming language:

  * **Lexer (`lexer.py`):** A tokenizer that scans source code and converts it into a stream of tokens (e.g., `NUMBER`, `STRING`, `IDENTIFIER`, `KEYWORD`, `PLUS`).
  * **Parser (`parser.py`):** A parser that takes the token stream and builds an Abstract Syntax Tree (AST), representing the code's structure.
  * **AST Nodes (`nodes.py`):** A comprehensive set of nodes that define every syntactic structure in the language (e.g., `BinOpNode`, `IfNode`, `FunDefNode`, `ClassNode`).
  * **Runtime (`runtime.py`):** Defines the `Context` and `SymbolTable` for managing variable scope, context (for tracebacks), and closures.
  * **Values (`values.py`):** Defines the language's internal data types (`Number`, `String`, `List`, `Function`, `Class`, `Instance`).
  * **Interpreter (`interpreter.py`):** The core engine that walks the AST and executes the program by visiting each node.
  * **Entry Point (`gladlang.py`):** The main file that ties everything together. It handles command-line arguments, runs files, and starts the interactive shell.

-----

## Key Features

GladLang supports a rich, modern feature set:

  * **Data Types:** Numbers (int/float), Strings, Lists, Dictionaries, Booleans, and Null.
  * **Variables:** Dynamic variable assignment with `LET`.
  * **Advanced Assignments:**
      * **Destructuring:** Unpack lists directly (`LET [x, y] = [1, 2]`).
      * **Slicing:** Access sub-lists or substrings easily (`list[0:3]`).
  * **String Manipulation:**
      * **Interpolation:** JavaScript-style template strings (`` `Hello ${name}` ``).
      * **Multi-line Strings:** Triple-quoted strings (`"""..."""`) for large text blocks.
  * **List Comprehensions:** Pythonic one-line list creation (`[x * 2 FOR x IN list]`).
  * **Dictionaries:** Key-value data structures (`{'key': 'value'}`).
  * **Control Flow:** `IF`, `WHILE`, `FOR`, `BREAK`, `CONTINUE`.
  * **Functions:** First-class citizens, Closures, Recursion, Named/Anonymous support.
  * **Object-Oriented Programming:** Classes, Inheritance, Polymorphism, `SELF` context.
  * **Built-ins:** `PRINT`, `INPUT`, `STR`, `INT`, `FLOAT`, `BOOL`.
  * **Error Handling:** Robust, user-friendly runtime error reporting with full tracebacks.
  * **Advanced Math:** Power (`**`), Floor Division (`//`), and Modulo (`%`) operators.
  * **Rich Comparisons:** Chained comparisons (`1 < x < 10`) and Identity checks (`is`).
  * **Flexible Logic:** Support for `and` / `or` (case-insensitive).

-----

## Getting Started

There are several ways to install and run GladLang.

### 1. Installation

#### Option A: Install via Pip (Recommended)
If you just want to use the language, install it via pip:

```bash
pip install gladlang

```

#### Option B: Install from Source (For Developers)

If you want to modify the codebase, clone the repository and install it in **editable mode**:

```bash
git clone https://github.com/gladw-in/gladlang.git
cd gladlang
pip install -e .

```

---

### 2. Usage

Once installed, you can use the global `gladlang` command.

#### Interactive Shell (REPL)

Run the interpreter without arguments to start the shell:

```bash
gladlang

```

#### Running a Script

Pass a file path to execute a script:

```bash
gladlang "tests/test.glad"

```

---

### 3. Running Without Installation (Source)

You can run the interpreter directly from the source code without installing it via pip:

```bash
python run.py "tests/test.glad"
```

---

### 4. Building the Executable

You can build a **standalone executable** (no Python required) using **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller run.py --paths src -F --name gladlang --icon=favicon.ico

```

This will create a single-file executable at `dist/gladlang` (or `gladlang.exe` on Windows).

**Adding to PATH (Optional):**
To run the standalone executable from anywhere:

* **Windows:** Move it to a folder and add that folder to your System PATH variables.
* **Mac/Linux:** Move it to `/usr/local/bin`: `sudo mv dist/gladlang /usr/local/bin/`

-----

## Language Tour (Syntax Reference)

Here is a guide to the GladLang syntax, with examples from the `tests/` directory.

### 1\. Comments

Comments start with `#` and last for the entire line.

```glad
# This is a comment.
LET a = 10 # This is an inline comment
```

### 2\. Variables and Data Types

#### Variables

Variables are assigned using the `LET` keyword. You can also unpack lists directly into variables using **Destructuring**.

```glad
LET a = 10
LET b = "Hello"
LET my_list = [a, b, 123]

# Destructuring Assignment
LET point = [10, 20]
LET [x, y] = point

PRINT x # 10
PRINT y # 20
```

#### Numbers

Numbers can be integers or floats. All standard arithmetic operations are supported.

```glad
LET math_result = (1 + 2) * 3 # 9
LET float_result = 10 / 4     # 2.5
```

#### Strings

Strings can be defined in three ways:
1.  **Double Quotes:** Standard strings.
2.  **Triple Quotes:** Multi-line strings that preserve formatting.
3.  **Backticks:** Template strings supporting interpolation.

```glad
# Standard
LET s = "Hello\nWorld"

# Multi-line
LET menu = """
1. Start
2. Settings
3. Exit
"""

# Interpolation (Template Strings)
LET name = "Glad"
PRINT `Welcome back, ${name}!`
PRINT `5 + 10 = ${5 + 10}`
```

#### Lists, Slicing & Comprehensions

Lists are ordered collections. You can access elements, slice them, or create new lists dynamically using comprehensions.

```glad
LET nums = [0, 1, 2, 3, 4, 5]

# Indexing & Assignment
PRINT nums[1]        # 1
LET nums[1] = 100

# Slicing [start:end]
PRINT nums[0:3]      # [0, 1, 2]
PRINT nums[3:]       # [3, 4, 5]

# List Comprehension
LET squares = [n ** 2 FOR n IN nums]
PRINT squares        # [0, 1, 4, 9, 16, 25]
```

#### Dictionaries

Dictionaries are key-value pairs enclosed in `{}`. Keys must be Strings or Numbers.

```glad
LET person = {
  "name": "Glad",
  "age": 25,
  "is_admin": TRUE
}

PRINT person["name"]       # Access: "Glad"
LET person["age"] = 26     # Modify
LET person["city"] = "NYC" # Add new key
```

#### Booleans

Booleans are `TRUE` and `FALSE`. They are the result of comparisons and logical operations.

```glad
LET t = TRUE
LET f = FALSE
PRINT t AND f # 0 (False)
PRINT t OR f  # 1 (True)
PRINT NOT t   # 0 (False)
```

**Truthiness:** `0`, `0.0`, `""`, `NULL`, and `FALSE` are "falsy." All other values (including non-empty strings, non-zero numbers, lists, functions, and classes) are "truthy."

#### Null

The `NULL` keyword represents a null or "nothing" value. It is falsy and prints as `0`. Functions with no `RETURN` statement implicitly return `NULL`.

-----

### 3\. Operators

#### Math Operations

GladLang supports standard arithmetic plus advanced operators like Modulo, Floor Division, and Power.

```glad
PRINT 2 ** 3      # Power: 8
PRINT 10 // 3     # Floor Division: 3
PRINT 10 % 3      # Modulo: 1

# Standard precedence rules apply
PRINT 2 + 3 * 4   # 14
PRINT 1 + 2 * 3   # 7
PRINT (1 + 2) * 3 # 9
```

#### Comparisons & Logic

You can compare values, chain comparisons for ranges, and check object identity.

```glad
# Equality & Inequality
PRINT 1 == 1      # True
PRINT 1 != 2      # True

# Chained Comparisons (Ranges)
LET age = 25
IF 18 <= age < 30 THEN
  PRINT "Young Adult"
ENDIF

PRINT (10 < 20) AND (10 != 5) # 1 (True)

# Identity ('is' checks if variables refer to the same object)
LET a = [1, 2]
LET b = a
PRINT b is a      # True
PRINT b == [1, 2] # True (Values match)

# Boolean Operators (case-insensitive)
IF a and b THEN
  PRINT "Both exist"
ENDIF
```

#### Increment / Decrement

Supports C-style pre- and post-increment/decrement operators on variables and list elements.

```glad
LET i = 5
PRINT i++ # 5
PRINT i   # 6
PRINT ++i # 7
PRINT i   # 7

LET my_list = [10, 20]
PRINT my_list[1]++ # 20
PRINT my_list[1]   # 21
```

-----

### 4\. Control Flow

#### IF Statements

Uses `IF...THEN...ENDIF` syntax.

```glad
LET num = -5
IF num < 0 THEN
  PRINT "It is negative."
ENDIF
```

#### WHILE Loops

Loops while a condition is `TRUE`.

```glad
LET i = 3
WHILE i > 0
  PRINT "i = " + i
  LET i = i - 1
ENDWHILE

# Prints:
# i = 3
# i = 2
# i = 1
```

#### FOR Loops

Iterates over the elements of a list.

```glad
LET my_list = ["apple", "banana", "cherry"]
FOR item IN my_list
  PRINT "Item: " + item
ENDFOR
```

**`BREAK` and `CONTINUE`** are supported in both `WHILE` and `FOR` loops.

-----

### 5\. Functions

#### Named Functions

Defined with `DEF...ENDEF`. Arguments are passed by value. `RETURN` sends a value back.

```glad
DEF add(a, b)
  RETURN a + b
ENDEF

LET sum = add(10, 5)
PRINT sum # 15
```

#### Anonymous Functions

Functions can be defined without a name, perfect for assigning to variables.

```glad
LET double = DEF(x)
  RETURN x * 2
ENDEF

PRINT double(5) # 10
```

#### Closures

Functions capture variables from their parent scope.

```glad
DEF create_greeter(greeting)
  DEF greeter_func(name)
    # 'greeting' is "closed over" from the parent
    RETURN greeting + ", " + name + "!"
  ENDEF
  RETURN greeter_func
ENDEF

LET say_hello = create_greeter("Hello")
PRINT say_hello("Alex") # "Hello, Alex!"
```

#### Recursion

Functions can call themselves.

```glad
DEF fib(n)
  IF n <= 1 THEN
    RETURN n
  ENDIF
  RETURN fib(n - 1) + fib(n - 2)
ENDEF

PRINT fib(7) # 13
```

-----

### 6\. Object-Oriented Programming (OOP)

#### Classes and Instantiation

Use `CLASS...ENDCLASS` to define classes and `NEW` to create instances. The constructor is `init`.

```glad
CLASS Counter
  DEF init(self)
    SELF.count = 0 # 'SELF' is the instance
  ENDEF
  
  DEF increment(self)
    SELF.count = SELF.count + 1
  ENDEF
  
  DEF get_count(self)
    RETURN SELF.count
  ENDEF
ENDCLASS
```

#### The `SELF` Keyword

`SELF` is the mandatory first argument for all methods and is used to access instance attributes and methods.

```glad
LET c = NEW Counter()
c.increment()
PRINT c.get_count() # 1
```

#### Inheritance

Use the `INHERITS` keyword. Methods can be overridden by the child class.

```glad
CLASS Pet
  DEF init(self, name)
    SELF.name = name
  ENDEF
  
  DEF speak(self)
    PRINT SELF.name + " makes a generic pet sound."
  ENDEF
ENDCLASS

CLASS Dog INHERITS Pet
  # Override the 'speak' method
  DEF speak(self)
    PRINT SELF.name + " says: Woof!"
  ENDEF
ENDCLASS

LET my_dog = NEW Dog("Buddy")
my_dog.speak() # "Buddy says: Woof!"
```

#### Polymorphism

When a base class method calls another method on `SELF`, it will correctly use the **child's overridden version**.

```glad
CLASS Pet
  DEF introduce(self)
    PRINT "I am a pet and I say:"
    SELF.speak() # This will call the child's 'speak'
  ENDEF
  
  DEF speak(self)
    PRINT "(Generic pet sound)"
  ENDEF
ENDCLASS

CLASS Cat INHERITS Pet
  DEF speak(self)
    PRINT "Meow!"
  ENDEF
ENDCLASS

LET my_cat = NEW Cat("Whiskers")
my_cat.introduce()
# Prints:
# I am a pet and I say:
# Meow!
```

-----

### 7\. Built-in Functions

  * `PRINT(value)`: Prints a value to the console.
  * `INPUT()`: Reads a line of text from the user as a String.
  * `STR(value)`: Casts a value to a String.
  * `INT(value)`: Casts a String or Float to an Integer.
  * `FLOAT(value)`: Casts a String or Integer to a Float.
  * `BOOL(value)`: Casts a value to its Boolean representation (`TRUE` or `FALSE`).

-----

## Error Handling

GladLang features detailed error handling and prints full tracebacks for runtime errors, making debugging easy.

**Example: Name Error** (`test_name_error.glad`)

```
Traceback (most recent call last):
  File test_name_error.glad, line 6, in <program>
Runtime Error: 'b' is not defined
```

**Example: Type Error** (`test_type_error.glad` with input "5")

```
Traceback (most recent call last):
  File test_type_error.glad, line 6, in <program>
Runtime Error: Illegal operation
```

**Example: Argument Error** (`test_arg_error.glad`)

```
Traceback (most recent call last):
  File test_arg_error.glad, line 7, in <program>
  File test_arg_error.glad, line 4, in add
Runtime Error: Incorrect argument count for 'add'. Expected 2, got 3
```

-----

## Running Tests

The `tests/` directory contains a comprehensive suite of `.glad` files to test every feature of the language. You can run any test by executing it with the interpreter:

```bash
python gladlang.py "test_closures.glad"
python gladlang.py "test_lists.glad"
python gladlang.py "test_polymorphism.glad"

```

or 

```bash
gladlang "test_closures.glad"
gladlang "test_lists.glad"
gladlang "test_polymorphism.glad"
```

## License

You can use this under the MIT License. See [LICENSE](LICENSE) for more details.