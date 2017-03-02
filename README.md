[![Build Status](https://travis-ci.org/Asher256/python-cmdwrapper.svg?branch=master)](https://travis-ci.org/Asher256/python-cmdwrapper)

## CmdWrapper - wrap any Linux command and use it as a Python 3 method

This library is useful for DevOps/Linux engineers.

- Author: Achraf Cherti (aka Asher256) <asher256@gmail.com>
- Github: https://github.com/Asher256/python-cmdwrapper

## Info

Python-CmdWrapper is a set of object oriented classes that can help you wrap any Linux
command and use it as a Python 3 method.

We are following the best practices of sofware engineering to offer a Python
module that is easy to use, object oriented, extensible and fully compatible
with the Python standards (PEP8, pylint recommendations...).

## Example
```
>>> from CmdWrapper import CmdWrapper

>>> find = CmdWrapper('find')

>>> result = find('/etc', '-maxdepth', '1', '-name', 'e*')
>>> print('proc stdout:', result.stdout)
/etc
/etc/ethertypes
/etc/environment

>>> print('proc stdout:', result.stdout.lines)
['/etc', '/etc/ethertypes', '/etc/environment']

>>> print('proc stdout:', result.stdout.firstline)
/etc

>>> print('exit-code:', result.returncode)
0

```

## Code Quality
The code quality is tested and validated with Travis CI and:
- pylint (Python checker)
- flake8 (Python checker)
- pep257 (docstrings)
- coverage.py (coverage of the unit-tests)

The goal is to have a source code that is 100% covered with unit-tests and
following Python's standards (PEP8) and best practices (pylint recommendations).

## Contribution

I encourage you to fork the project and send me your pull requests! I
