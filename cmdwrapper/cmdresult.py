#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Achraf Cherti (Asher256) <asher256@gmail.com>
# Github: https://github.com/Asher256/python-cmdwrapper
# License: LGPL 2.1
#
# This source code follows the PEP-8 style guide:
# https://www.python.org/dev/peps/pep-0008/
#
"""The result of a command."""

import sys
import platform
from cmdoutput import CmdOutput


assert platform.system() == 'Linux'
assert sys.version_info >= (3, 2), "The Python version need to be >= 3.2"


# pylint: disable=too-few-public-methods
class CmdResult(object):
    """The result of a command (stdout, stderr and return code)."""

    def __init__(self, stdout, stderr, returncode):
        """Init the CmdResult with stdout, stderr and returncode."""
        assert isinstance(stdout, (bytes, str))
        assert isinstance(stderr, (bytes, str))
        assert isinstance(returncode, int)
        self.stdout = CmdOutput(stdout)
        self.stderr = CmdOutput(stderr)
        self.returncode = returncode

    def __str__(self):
        """Return stdout."""
        output = str(self.stdout).rstrip('\r\n').strip() + \
            str(self.stderr).rstrip('\r\n').strip() + '\n'
        return output


def main():
    """Test the class CmdResult."""
    import unittest

    class TestCmdOutput(unittest.TestCase):
        """Testing the class CmdOutput."""

        def test_cmdoutput(self):
            """Test: CmdOutput()."""
            stdout = 'stdout content'
            stderr = 'stderr content'
            returncode = 101

            cmd_result = CmdResult(stdout=stdout, stderr=stderr,
                                   returncode=returncode)
            self.assertEqual(cmd_result.stdout.output, stdout)
            self.assertEqual(cmd_result.stderr.output, stderr)
            self.assertEqual(cmd_result.returncode, returncode)

            to_str = str(cmd_result)
            self.assertIn(stdout, to_str)
            self.assertIn(stderr, to_str)

    tests = unittest.TestLoader().loadTestsFromTestCase(TestCmdOutput)
    unittest.TextTestRunner(verbosity=5).run(tests)


if __name__ == '__main__':
    main()

# vim:ai:et:sw=4:ts=4:sts=4:tw=78:fenc=utf-8
