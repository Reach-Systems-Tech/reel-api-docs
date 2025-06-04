# Project Style Guide

This document outlines the style standards for the project, broken down by language.

## Python

### General Conventions

#### Code Layout

- Use 4 spaces per indentation level.
- Limit all lines to a maximum of 79 characters.
- Separate top-level function and class definitions with two blank lines.
- Use a single blank line to separate methods within a class.
- Surround top-level function and class definitions with two blank lines.

#### Imports

- Imports should usually be on separate lines.
- Imports should be grouped in the following order:
    1. Standard library imports.
    2. Related third-party imports.
    3. Local application/library-specific imports- .
- Each group of imports should be separated by a blank line.

```python
# Correct import grouping
import os
import sys

import requests

from mymodule import myfunction
```

#### Naming Conventions

There are several different types of conventions used:

- **Snake Case**: Use lowercase words separated by underscores (e.g., `my_variable`).
- **Screaming Snake Case**: Use uppercase words separated by underscores (e.g., `MY_CONSTANT`).
- **CapWords**: Capitalized words (e.g., `BestClassEver`).
-- **Kebab Case**: lowercase words separated by hypens (e.g., `my-api-endpoint`)

##### When To Use Which Convention

- **Variables**: Use snake case.
- **Constants**: Use screaming snake case.
- **Functions**: Use snake case.
- **Classes**: Use CapWords.
- **API Endpoint URLS**: Use Kebab Case.

#### Docstrings

Use Google style for docstrings. Here’s how to write docstrings for different constructs:

##### Function and Method Docstrings

```python
def function_with_types_in_docstring(param1, param2):
    """Summary of the function.

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    Raises:
        ValueError: If `param2` is empty.
    """
    if not param2:
        raise ValueError('param2 cannot be empty')
    return True
```

##### Class Docstrings

```python
class SampleClass:
    """Summary of the class.

    Attributes:
        attr1 (int): Description of `attr1`.
        attr2 (str): Description of `attr2`.
    """

    def __init__(self, attr1, attr2):
        """Inits SampleClass with attr1 and attr2.

        Args:
            attr1 (int): Description of `attr1`.
            attr2 (str): Description of `attr2`.
        """
        self.attr1 = attr1
        self.attr2 = attr2

    def method(self):
        """Summary of the method.

        Returns:
            bool: Description of return value.
        """
        return True
```

##### Module Docstrings

```python
"""
File: module_filename.py
Title: What Is This Module For
Company: Reach Systems
Author: Steven Universe
Date: August 2, 2024 (The date the file was created)

Description: This module demonstrates proper usage of module-level docstrings.

Usage: This is an example of how to use this module:
    
        python example.py
Notes: Anything important that should be known
"""

import sys

def main():
    """Entry point for the application script."""
    print('Hello, world!')

if __name__ == "__main__":
    main()
```

The `Usage:` and `Notes:` sections are added as needed.

#### Inline Comments

- Use inline comments sparingly.
- Inline comments should be separated by at least two spaces from the statement.
- Inline comments should start with a # and a single space.

```python
x = x + 1  # Increment x
```

#### Block Comments

- Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code.
- Each line of a block comment starts with a # and a single space (unless it is indented text inside the comment).

```python
# This is a block comment.
# It explains the following code.
y = x * 2
```

## Conclusion

By following these conventions, your code will be more readable, maintainable, and consistent. Happy coding!
