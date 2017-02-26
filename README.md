[![Build Status](https://travis-ci.org/Asher256/python-cmdwrapper.svg?branch=master)](https://travis-ci.org/Asher256/python-cmdwrapper)

# Wrap any Linux command and use it as a Python method

This library can be useful for DevOps/Linux engineers.

## Author

Achraf Cherti (aka Asher256) <asher256@gmail.com>

## Info

CmdWrapper is a set of object oriented classes that can help DevOps/Linux
engineers to wrap any Linux command and use it as a Python 3 method.

We are following some good practices of sofware engineering and design patterns
to offer a Python module that is easy to use, extensible and fully compatible
with the Python 3 standards (PEP8, pylint recommendations...).

## Example
```
from CmdWrapper import CmdWrapper

find = CmdWrapper('find')

result = find('/etc', '-maxdepth', '1', '-name', 'e*')
print('proc stdout:', result.stdout)

```

## Code Quality
The code quality is tested and validated with Travis CI and:
- pylint (Python checker)
- flake8 (Python checker)
- pep257 (docstrings)
- coverage.py (coverage of the unit-tests)

The goal is to have a source code that is 100% covered with unit-tests and
following Python's standards (PEP8) and best practices (pylint recommendations).

