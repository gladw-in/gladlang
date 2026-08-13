# GladLang

**GladLang is a dynamic, interpreted, object-oriented programming language.** This is a full interpreter built from scratch in Python, complete with a lexer, parser, and runtime environment. It supports modern programming features like closures, classes, inheritance, and robust error handling.

GladLang source files use the `.glad` file extension.

![Lines of code](https://sloc.xyz/github/gladw-in/gladlang)

This is the full overview of the GladLang language, its features, and how to run the interpreter.

## Table of Contents

- [About The Language](#about-the-language)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
    - [1. Installation](#1-installation)
    - [2. Usage](#2-usage)
    - [3. Running Without Installation (Source)](#3-running-without-installation-source)
- [Language Tour (Syntax Reference)](#language-tour-syntax-reference)
    - [1. Comments](#1-comments)
    - [2. Variables and Data Types](#2-variables-and-data-types)
        - [Variables](#variables)
        - [Numbers](#numbers)
        - [Strings](#strings)
        - [Lists, Slicing & Comprehensions](#lists-slicing--comprehensions)
        - [Dictionaries](#dictionaries)
        - [Booleans](#booleans)
        - [Null](#null)
        - [Enums](#enums)
    - [3. Operators](#3-operators)
        - [Math Operations](#math-operations)
        - [Compound Assignments](#compound-assignments)
        - [Bitwise Operators](#bitwise-operators)
        - [Comparisons, Logic & Type Checking](#comparisons-logic--type-checking)
        - [Conditional (Ternary) Operator](#conditional-ternary-operator)
        - [Increment / Decrement](#increment--decrement)
    - [4. Control Flow](#4-control-flow)
        - [IF Statements](#if-statements)
        - [Switch Statements](#switch-statements)
        - [WHILE Loops](#while-loops)
        - [FOR Loops](#for-loops)
    - [5. Functions](#5-functions)
        - [Named Functions](#named-functions)
        - [Anonymous Functions](#anonymous-functions)
        - [Closures](#closures)
        - [Recursion](#recursion)
        - [Function Overloading](#function-overloading)
    - [6. Object-Oriented Programming (OOP)](#6-object-oriented-programming-oop)
        - [Classes and Instantiation](#classes-and-instantiation)
        - [The `THIS` Keyword](#the-this-keyword)
        - [Inheritance & The SUPER Keyword](#inheritance--the-super-keyword)
        - [Multiple Inheritance & MRO](#multiple-inheritance--mro)
        - [Method & Constructor Overloading](#method--constructor-overloading)
        - [Polymorphism](#polymorphism)
        - [Access Modifiers](#access-modifiers)
        - [Static Members](#static-members)
    - [7. Built-in Functions](#7-built-in-functions)
- [Error Handling](#error-handling)
- [Running Tests](#running-tests)
- [License](#license)

-----

## About The Language

GladLang is an interpreter for a custom scripting language. It was built as a complete system, demonstrating the core components of a programming language:

  * **Lexer:** A tokenizer that scans source code and converts it into a stream of tokens (e.g., `NUMBER`, `STRING`, `IDENTIFIER`, `KEYWORD`, `PLUS`).
  * **Parser:** A parser that takes the token stream and builds an Abstract Syntax Tree (AST), representing the code's structure.
  * **AST Nodes:** A comprehensive set of nodes that define every syntactic structure in the language (e.g., `BinOpNode`, `IfNode`, `FunDefNode`, `ClassNode`).
  * **Runtime:** Defines the `Context` and `SymbolTable` for managing variable scope, context (for tracebacks), and closures.
  * **Values:** Defines the language's internal data types (`Number`, `String`, `List`, `Dict`, `Function`, `Class`, `Instance`).
  * **Interpreter:** The core engine that walks the AST. It uses a "Zero-Copy" architecture with Dependency Injection for high-performance execution and low memory overhead.
  * **Entry Point:** The main file that ties everything together. It handles command-line arguments, runs files, and starts the interactive shell.

-----

## Key Features

GladLang supports a rich, modern feature set:

  * **Data Types:** Numbers (int/float, plus **Hex/Octal/Binary** literals), Strings, Lists, Dictionaries, Booleans, and Null.
  * **Variables:** Dynamic variable assignment with `LET`.
  * **Advanced Assignments:**
      * **Destructuring:** Unpack lists in assignments (`LET [x, y] = [1, 2]`) and loops (`FOR [x, y] IN points`).
      * **Slicing:** Access sub-lists or substrings easily (`list[0:3]`).
  * **String Manipulation:**
      * **Interpolation:** JavaScript-style template strings (`` `Hello ${name}` ``).
      * **Multi-line Strings:** Triple-quoted strings (`"""..."""`) for large text blocks.
  * **Comprehensions:**
      * **List Comprehensions:** Supports nesting (`[x+y FOR x IN A FOR y IN B]`).
      * **Dictionary Comprehensions:** Create dicts programmatically (`{k: v FOR k IN list}`).
  * **Dictionaries:** Key-value data structures (`{'key': 'value'}`).
  * **Control Flow:**
      * Full support for `IF` / `ELSE IF`, `SWITCH` / `CASE`.
      * **Universal Iteration:** `FOR` loops over Lists, Strings (chars), and Dictionaries (keys).
      * **C-Style Iteration:** Traditional `FOR` loops (`FOR (LET I = 0; I < 10; I++)`) featuring strict block scoping and safe closure capturing.
  * **Functions:** First-class citizens, Closures, Recursion, Named/Anonymous support, and **Overloading** (by argument count).
  * **Object-Oriented:** Full OOP support with `CLASS`, `INHERITS`, Access Modifiers, and **Method/Constructor Overloading**. Object instantiation is **$O(1)$** due to constructor caching.
  * **Advanced Inheritance:** Support for **Multiple** and **Hybrid** inheritance with strict C3-style **Method Resolution Order (MRO)**. 
  * **Parent Delegation:** Full support for `SUPER` in both constructors and overridden methods, plus explicit parent targeting.
  * **Static Members:** Java-style `STATIC` fields, methods, and constants (`STATIC FINAL`).
  * **Operators:** Ternary Operator (`condition ? true : false`) for concise conditional logic.
  * **Enums:** Fully encapsulated, immutable `ENUM` types with auto-incrementing values and explicit assignments.
  * **OOP Safety:** Runtime checks for circular inheritance, LSP violations, strict unbound method type-checking, and secure encapsulation.
  * **Error Management:** Gracefully handle errors with `TRY`, `CATCH`, and `FINALLY`.
  * **Constants:** Declare immutable values using `FINAL`. These use **Atomic Locking** (`set_if_absent`) to prevent race conditions and are fully protected from shadowing or modification.
  * **Memory Safety:** Built-in protection against Denial-of-Service attacks. List repetition is capped at **1,000,000** elements, and a global **Instruction Budget** prevents infinite loop lockups.
  * **Logical Accuracy:** Full **Short-Circuit Evaluation** for `AND`/`OR` operators and corrected math logic for compound assignments like `+=`.
  * **Built-ins:** `PRINTLN`, `PRINT`, `INPUT`, `STR`, `INT`, `FLOAT`, `BOOL`, `LEN`, `LENGTH`, `PRINTF`, `TIME`, `RANDOM`, `DELAY`.
  * **Error Handling:** Robust, user-friendly runtime error reporting with full tracebacks.
  * **Advanced Math:** Compound assignments (`+=`, `*=`), Power (`**`), Modulo (`%`), and automatic float division.
  * **Rich Comparisons:** Chained comparisons (`1 < x < 10`), Identity checks (`IS`), and runtime type-checking (`INSTANCEOF`).
  * **Boolean Logic:** Strict support for `AND` / `OR` / `NOT`.
-----

## Getting Started

There are several ways to install and run GladLang.

### 1. Installation

#### Option A: Install via Pip (Recommended)
If you just want to use the language, install it via pip:

```bash
pip install gladlang

```

#### Option B: Use from Releases

Pre-built binaries for Windows, Linux, and macOS are available on the [GitHub Releases](https://github.com/gladw-in/gladlang/releases/latest) page.

#### Option C: Install from Source (For Developers)

If you want to modify the codebase, clone the repository and install it in **editable mode**:

```bash
git clone --depth 1 https://github.com/gladw-in/gladlang.git
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

#### Inline Execution
Run code directly from your terminal string:

```bash
gladlang "PRINTLN 10 + 5"

```

---

### 3. Running Without Installation (Source)

You can run the interpreter directly from the source code without installing it via pip:

```bash
python run.py "tests/test.glad"

```

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
# Immutable Constants
FINAL PI = 3.14159

# Variable Assignment
LET a = 10
LET b = "Hello"
LET my_list = [a, b, 123]

# Destructuring Assignment
LET point = [10, 20]
LET [x, y] = point

PRINTLN x # 10
PRINTLN y # 20

```

#### Numbers

Numbers can be integers or floats. You can also use **Hexadecimal**, **Octal**, and **Binary** literals.

```glad
LET math_result = (1 + 2) * 3 # 9
LET float_result = 10 / 4     # 2.5

# Number Bases
LET hex_val = 0xFF      # 255
LET oct_val = 0o77      # 63
LET bin_val = 0b101     # 5

```

#### Strings

Strings can be defined in three ways:

1. **Double Quotes:** Standard strings.
2. **Triple Quotes:** Multi-line strings that preserve formatting.
3. **Backticks:** Template strings supporting interpolation.

```glad
# Standard
LET s = "Hello\nWorld"

# Multi-line
LET menu = """
1. Start
2. Settings
3. Exit
"""

# Indexing
LET char = "GladLang"[0]  # "G"
PRINTLN "Hello"[1]        # "e"

# Escapes (work in "..." and `...`)
PRINTLN "Line 1\nLine 2"
PRINTLN `Column 1\tColumn 2`

# Interpolation (Template Strings)
LET name = "Glad"
PRINTLN `Welcome back, ${name}!`
PRINTLN `5 + 10 = ${5 + 10}`

```

#### Lists, Slicing & Comprehensions

Lists are ordered collections. You can access elements, slice them, or create new lists dynamically using comprehensions.

```glad
LET nums = [0, 1, 2, 3, 4, 5]

# Indexing & Assignment
PRINTLN nums[1]      # 1
LET nums[1] = 100

# Slicing [start:end]
PRINTLN nums[0:3]    # [0, 1, 2]
PRINTLN nums[3:]     # [3, 4, 5]

# List Comprehension
LET squares = [n ** 2 FOR n IN nums]
PRINTLN squares      # [0, 1, 4, 9, 16, 25]

# Nested List Comprehension
LET pairs = [[x, y] FOR x IN [1, 2] FOR y IN [3, 4]]
# Result: [[1, 3], [1, 4], [2, 3], [2, 4]]

```

#### Dictionaries

Dictionaries are key-value pairs enclosed in `{}`. Keys must be Strings or Numbers.

```glad
LET person = {
  "name": "Glad",
  "age": 25,
  "is_admin": TRUE
}

PRINTLN person["name"]     # Access: "Glad"
LET person["age"] = 26     # Modify
LET person["city"] = "NYC" # Add new key

# Dictionary Comprehension
LET keys = ["a", "b", "c"]
LET d = {k: 0 FOR k IN keys} 
PRINTLN d # {'a': 0, 'b': 0, 'c': 0}

```

#### Booleans

Booleans are `TRUE` and `FALSE`. They are the result of comparisons and logical operations.

```glad
LET t = TRUE
LET f = FALSE
PRINTLN t AND f # 0 (False)
PRINTLN t OR f  # 1 (True)
PRINTLN NOT t   # 0 (False)

```

**Truthiness:** `0`, `0.0`, `""`, `NULL`, and `FALSE` are "falsy." All other values (including non-empty strings, non-zero numbers, lists, functions, and classes) are "truthy."

#### Null

The `NULL` keyword represents a null or "nothing" value. It is falsy and prints as `null`. Functions with no `RETURN` statement implicitly return `NULL`.

**Important:** `NULL` is a distinct value representing "nothing". It is falsy (e.g., `IF NULL THEN ...` is false). It is **not** numerically equal to `0` (e.g., `NULL == 0` → `FALSE`). For identity checks, use the `IS` operator (`NULL IS NULL` → `TRUE`; `NULL IS 0` → `FALSE`). Functions with no `RETURN` statement implicitly return `NULL`.

#### Enums

GladLang supports strict, immutable `ENUM` types. Enums can be zero-indexed implicitly, or you can assign explicit values. They also support comma-separated cases. 

```glad
# Basic Enum (Implicit 0-indexing)
ENUM Colors
  RED
  GREEN
  BLUE
ENDENUM

PRINTLN Colors.RED.value   # 0
PRINTLN Colors.GREEN.value # 1

# Explicit & Auto-Incrementing Values
ENUM HTTPStatus
  OK = 200
  NOT_FOUND = 404
  CUSTOM_ERROR       # Implicitly becomes 405
ENDENUM

# Comma-Separated
ENUM Days
  MON, TUE, WED, THU, FRI
ENDENUM
```

-----

### 3\. Operators

#### Math Operations

GladLang supports standard arithmetic plus advanced operators like Modulo, Floor Division, and Power.

```glad
LET sum = 10 + 5    # 15
LET diff = 20 - 8   # 12
LET prod = 5 * 4    # 20
LET quot = 100 / 2  # 50.0 (Always Float)

PRINTLN 2 ** 3      # Power: 8
PRINTLN 10 // 3     # Floor Division: 3
PRINTLN 10 % 3      # Modulo: 1

# Standard precedence rules apply
PRINTLN 2 + 3 * 4   # 14
PRINTLN 1 + 2 * 3   # 7
PRINTLN ((1 + 2) * 3) # 9

```

#### Compound Assignments

GladLang supports syntactic sugar for updating variables in place.

```glad
LET score = 10

score += 5   # score is now 15
score -= 2   # score is now 13
score *= 2   # score is now 26
score /= 2   # score is now 13.0
score %= 5   # score is now 3.0

```

#### Bitwise Operators

Perform binary manipulation on integers. All bitwise operations are performed on **signed 32‑bit integers** (two's complement).

```glad
LET a = 5  # Binary 101
LET b = 3  # Binary 011

PRINTLN a & b   # 1 (AND)
PRINTLN a | b   # 7 (OR)
PRINTLN a ^ b   # 6 (XOR)
PRINTLN ~a      # -6 (bitwise NOT)
PRINTLN 1 << 2  # 4 (Left Shift)
PRINTLN 8 >> 2  # 2 (Right Shift)

# Compound Assignment
LET x = 1
x <<= 2       # x is now 4

```

#### Comparisons, Logic & Type Checking

You can compare values, chain comparisons for ranges, check object identity, and perform runtime type-checking.

```glad
# Equality & Inequality
PRINTLN 1 == 1      # True
PRINTLN 1 != 2      # True

# Chained Comparisons (Ranges)
LET age = 25
IF 18 <= age < 30 THEN
  PRINTLN "Young Adult"
ENDIF

PRINTLN (10 < 20) AND (10 != 5) # 1 (True)

# Identity ('IS' checks if variables refer to the same object)
LET a = [1, 2]
LET b = a
PRINTLN b IS a      # True

# Type Checking ('INSTANCEOF' checks the entire inheritance chain)
CLASS Animal ENDCLASS
CLASS Dog INHERITS Animal ENDCLASS
LET d = NEW Dog()
PRINTLN d INSTANCEOF Dog    # 1 (True)
PRINTLN d INSTANCEOF Animal # 1 (True)

# Boolean Operators
IF a AND b THEN
  PRINTLN "Both exist"
ENDIF
```

#### Conditional (Ternary) Operator

A concise way to write `IF...ELSE` statements in a single line. It supports nesting and arbitrary expressions.

```glad
LET age = 20
LET type = age >= 18 ? "Adult" : "Minor"
PRINTLN type # "Adult"

# Nested Ternary
LET score = 85
LET grade = score > 90 ? "A" : score > 80 ? "B" : "C"
PRINTLN grade # "B"

```

#### Increment / Decrement

Supports C-style pre- and post-increment/decrement operators on variables and list elements.

```glad
LET i = 5
PRINTLN i++ # 5
PRINTLN i   # 6
PRINTLN ++i # 7
PRINTLN i   # 7

LET my_list = [10, 20]
PRINTLN my_list[1]++ # 20
PRINTLN my_list[1]   # 21

```

-----

### 4\. Control Flow

#### IF Statements

Uses `IF...THEN...ENDIF` syntax.

```glad
IF x > 10 THEN
    PRINTLN "Large"
ELSE IF x > 5 THEN
    PRINTLN "Medium"
ELSE
    PRINTLN "Small"
ENDIF

```

#### Switch Statements

Use `SWITCH` to match a value against multiple possibilities. It supports single values, comma-separated lists for multiple matches, and expressions.

```glad
LET status = 200

SWITCH status
    CASE 200:
        PRINTLN "OK"
    CASE 404, 500:
        PRINTLN "Error"
    DEFAULT:
        PRINTLN "Unknown Status"
ENDSWITCH

```

#### WHILE Loops

Loops while a condition is `TRUE`.

```glad
LET i = 3
WHILE i > 0
  PRINTLN "i = " + i
  i = i - 1
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
  PRINTLN "Item: " + item
ENDFOR

# Iterate over Strings (Characters)
FOR letter IN "Hi"
  PRINTLN letter
ENDFOR

# Iterate over Dictionaries (Keys)
LET data = {"x": 10, "y": 20}
FOR key IN data
  PRINTLN key + ": " + data[key]
ENDFOR

# Loop Destructuring (Unpacking)
LET points = [[1, 2], [3, 4]]
FOR [x, y] IN points
  PRINTLN "x: " + STR(x) + ", y: " + STR(y)
ENDFOR

# --- 2. C-Style FOR Loops ---
# FOR (initialization; condition; increment)
FOR (LET i = 0; i < 5; i++)
  PRINTLN "Count: " + STR(i)
ENDFOR

```

**`BREAK` and `CONTINUE`** are supported in both `WHILE` and `FOR` loops.

---

### 5. Functions

#### Named Functions

Defined with `DEF...ENDDEF`. Arguments are passed by value. `RETURN` sends a value back.

```glad
DEF add(a, b)
  RETURN a + b
ENDDEF

LET sum = add(10, 5)
PRINTLN sum # 15

```

#### Anonymous Functions

Functions can be defined without a name, perfect for assigning to variables.

```glad
LET double = DEF(x)
  RETURN x * 2
ENDDEF

PRINTLN double(5) # 10

```

#### Closures

Functions capture variables from their parent scope.

```glad
DEF create_greeter(greeting)
  DEF greeter_func(name)
    # 'greeting' is "closed over" from the parent
    RETURN greeting + ", " + name + "!"
  ENDDEF
  RETURN greeter_func
ENDDEF

LET say_hello = create_greeter("Hello")
PRINTLN say_hello("Alex") # "Hello, Alex!"

```

#### Recursion

Functions can call themselves.

```glad
DEF fib(n)
  IF n <= 1 THEN
    RETURN n
  ENDIF
  RETURN fib(n - 1) + fib(n - 2)
ENDDEF

PRINTLN fib(7) # 13

```

#### Function Overloading

You can define multiple functions with the same name, as long as they accept a different number of arguments (arity).

```glad
DEF add(a, b)
  RETURN a + b
ENDDEF

DEF add(a, b, c)
  RETURN a + b + c
ENDDEF

PRINTLN add(10, 20)     # Calls 2-arg version: 30
PRINTLN add(10, 20, 30) # Calls 3-arg version: 60

```

-----

### 6\. Object-Oriented Programming (OOP)

#### Classes and Instantiation

Use `CLASS...ENDCLASS` to define classes and `NEW` to create instances. The constructor is a method named exactly after the class.

```glad
CLASS Counter
  DEF Counter()
    THIS.count = 0 # 'THIS' is the instance
  ENDDEF
  
  DEF increment()
    THIS.count = THIS.count + 1
  ENDDEF
  
  DEF get_count()
    RETURN THIS.count
  ENDDEF
ENDCLASS

LET c = NEW Counter()
c.increment()
PRINTLN c.get_count() # 1

```

#### The `THIS` Keyword

`THIS` is used to access instance attributes and methods. It is automatically available inside all non-static methods; you do not need to pass it as an argument.

#### Inheritance & The SUPER Keyword

Use the `INHERITS` keyword to inherit from parent classes. You can use the `SUPER` keyword to seamlessly call parent constructors and overridden methods. GladLang enforces strict visibility rules (LSP) and prevents circular inheritance loops.

```glad
CLASS Pet
  DEF Pet(name)
    THIS.name = name
  ENDDEF
  
  DEF speak()
    RETURN "makes a generic pet sound."
  ENDDEF
ENDCLASS

CLASS Dog INHERITS Pet
  DEF Dog(name)
    # Automatically delegates to the parent constructor
    SUPER(name)
  ENDDEF

  # Override the 'speak' method and extend parent functionality
  DEF speak()
    PRINTLN THIS.name + " says: Woof, and " + SUPER.speak()
  ENDDEF
ENDCLASS

LET my_dog = NEW Dog("Buddy")
my_dog.speak() # "Buddy says: Woof, and makes a generic pet sound."

```

#### Multiple Inheritance & MRO

GladLang supports multiple and hybrid inheritance (solving the Diamond Problem). When inheriting from multiple classes, GladLang establishes a **Method Resolution Order (MRO)** that prioritizes parents from left to right.

If you want to bypass the default `SUPER()` MRO (for example, to initialize multiple parent classes explicitly), you can call parent constructors or methods directly using the Class name.

```glad
CLASS Animal
    DEF Animal()
        PRINTLN("Animal Constructor")
    ENDDEF

    DEF speak()
        RETURN "Generic Sound"
    ENDDEF
ENDCLASS

CLASS Human
    DEF Human()
        PRINTLN("Human Constructor")
    ENDDEF

    DEF speak()
        RETURN "Hello"
    ENDDEF
ENDCLASS

CLASS Dog INHERITS Animal, Human
    DEF Dog()
        PRINTLN("--- Initializing Dog ---")
        
        # STYLE 1: Explicit Calls (Great for Multiple Inheritance)
        Animal.Animal()
        Human.Human()
        
        # STYLE 2: SUPER Call (Great for Single Inheritance / MRO)
        # This will call 'Animal' again because it's first in MRO
        PRINTLN("--- Calling SUPER() ---")
        SUPER() 
    ENDDEF

    DEF speak()
        # Mix both styles in methods too
        RETURN "Woof! " + SUPER.speak() + " " + Human.speak()
    ENDDEF
ENDCLASS

LET d = NEW Dog()
# Expected:
# --- Initializing Dog ---
# Animal Constructor
# Human Constructor
# --- Calling SUPER() ---
# Animal Constructor

PRINTLN("\n[Speaking]")
PRINTLN(d.speak())
# Expected: Woof! Generic Sound Hello
```

#### Method & Constructor Overloading

Classes support overloading for both regular methods and constructors. This allows for flexible object creation (e.g., Copy Constructors).

```glad
CLASS Vector
  # Default Constructor
  DEF Vector()
    THIS.x = 0
    THIS.y = 0
  ENDDEF

  # Overloaded Constructor
  DEF Vector(x, y)
    THIS.x = x
    THIS.y = y
  ENDDEF
  
  # Copy Constructor
  DEF Vector(other)
    THIS.x = other.x
    THIS.y = other.y
  ENDDEF
ENDCLASS

LET v1 = NEW Vector()       # [0, 0]
LET v2 = NEW Vector(10, 20) # [10, 20]
LET v3 = NEW Vector(v2)     # [10, 20] (Copy of v2)

```

#### Polymorphism

When a base class method calls another method on `THIS`, it will correctly use the **child's overridden version**.

```glad
CLASS Pet
  DEF introduce()
    PRINTLN "I am a pet and I say:"
    THIS.speak() # This will call the child's 'speak'
  ENDDEF
  
  DEF speak()
    PRINTLN "(Generic pet sound)"
  ENDDEF
ENDCLASS

CLASS Cat INHERITS Pet
  DEF speak()
    PRINTLN "Meow!"
  ENDDEF
ENDCLASS

LET my_cat = NEW Cat("Whiskers")
my_cat.introduce()
# Prints:
# I am a pet and I say:
# Meow!

```

#### Access Modifiers

You can control the visibility of methods and attributes using `PUBLIC`, `PRIVATE`, and `PROTECTED`.

* **Encapsulation:** Private attributes are name-mangled to prevent collisions.
* **Singleton Support:** Constructors can be private to force factory usage.

```glad
CLASS SecureData
  DEF SecureData(data)
    PRIVATE THIS.data = data
  ENDDEF

  PUBLIC DEF get_data()
    RETURN THIS.data
  ENDDEF
ENDCLASS

# External access to 'data' will raise a Runtime Error.

```

#### Static Members

GladLang supports Java-style static fields and methods. These belong to the class itself rather than instances.

* **Static Fields:** Shared across all instances.
* **Static Constants:** `STATIC FINAL` creates class-level constants.
* **Static Privacy:** `STATIC PRIVATE` fields are only visible within the class.

```glad
CLASS Config
  # A constant shared by everyone
  STATIC FINAL MAX_USERS = 100

  # A private static variable
  STATIC PRIVATE LET internal_count = 0

  STATIC PUBLIC DEF increment()
    Config.internal_count = Config.internal_count + 1
    RETURN Config.internal_count
  ENDDEF
ENDCLASS

# Access directly via the Class name
PRINTLN Config.MAX_USERS      # 100
PRINTLN Config.increment()    # 1

```

-----

### 7\. Built-in Functions

  * `PRINTLN(value)`: Prints a value to the console **with** a new line.
  * `PRINT(value)`: Prints a value **without** a new line.
  * `INPUT()`: Reads a line of text from the user as a String.
  * `STR(value)`: Casts a value to a String.
  * `INT(value)`: Casts a String or Float to an Integer.
  * `FLOAT(value)`: Casts a String or Integer to a Float.
  * `BOOL(value)`: Casts a value to its Boolean representation (`TRUE` or `FALSE`).
  * `LEN(value)`: Returns the length of a String, List, or Dict. Alias: `LENGTH()`.
  * `PRINTF(format, ...)`: Prints formatted text. Supports `%s` (string), `%d` (integer), `%f` (float), and `%%` (literal percent). Extra arguments are ignored.
  * `TIME()`: Returns the current time as a float (seconds since epoch).
  * `TIME_SECONDS()`: Returns the current time as an integer (seconds since epoch).
  * `TIME_MILLIS()`: Returns the current time as an integer (milliseconds since epoch).
  * `TIME_NANOS()`: Returns the current time as an integer (nanoseconds since epoch).
  * `RANDOM()`: Returns a cryptographically secure random 32‑bit integer.
  * `RANDOM_FLOAT()`: Returns a cryptographically secure float in the range `[0.0, 1.0)`.
  * `RANDOM_RANGE(start, stop)`: Returns a cryptographically secure integer in `[start, stop)` (stop excluded). Requires `start < stop`.
  * `DELAY(seconds)`: Pauses execution for the given number of seconds (capped at 60 seconds for safety). Only finite, non‑negative numbers are accepted.

-----

## Error Handling

You can handle runtime errors gracefully or throw your own exceptions.

```glad
TRY
    # Attempt dangerous code
    LET result = 10 / 0
    PRINTLN result
CATCH error
    # Handle the error
    PRINTLN "Caught an error: " + error
FINALLY
    # Always runs
    PRINTLN "Cleanup complete."
ENDTRY

# Manually throwing errors
TRY
    LET age = -1
    IF age < 0 THEN
        THROW "Age cannot be negative"
    ENDIF
CATCH e
    PRINTLN e   # prints only "Age cannot be negative"
ENDTRY

```

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
gladlang "test_closures.glad"
gladlang "test_lists.glad"
gladlang "test_polymorphism.glad"

```

## License

You can use this under the MIT License. See [LICENSE](LICENSE) for more details.