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
"""The output of a command (stdout or stderr)."""

import sys
import platform


assert platform.system() == 'Linux'
assert sys.version_info >= (3, 3), "The Python version need to be >= 3.3"


class CmdOutput(object):
    """The output of a command (stdout or stderr)."""

    def __init__(self, output):
        """Store the output internally."""
        self._output = None
        self.output = output

    @property
    def lines(self):
        """Return the output as a list (each item is a line)."""
        return self.output.splitlines()

    @property
    def firstline(self):
        """Return the first line of the output."""
        if self.output != '':
            return self.lines[0]

        return ''

    def __str__(self):
        """Return the output."""
        return self.output

    def __iter__(self):
        """Iter through stdout."""
        for line in self.lines:
            yield line

    @property
    def output(self):
        """Return the output's content (string)."""
        return self._output

    @output.setter
    def output(self, output):
        """Return an unified version of the output."""
        if output is None:
            output = ''
        else:
            assert isinstance(output, (bytes, str))

        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='ignore')

        self._output = output


def main():
    """The program starts here."""
    import unittest

    class TestCmdOutput(unittest.TestCase):
        """Testing the class CmdOutput."""

        def test_cmdoutput(self):
            """Test: CmdOutput()."""
            first_line = b'First Line'
            second_line = b'Second Line'
            byte_content = first_line + b'\n' + second_line

            utf8_byte_content = byte_content.decode('utf-8', errors='ignore')
            for content in [byte_content, utf8_byte_content]:
                cmd_output = CmdOutput(content)

                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='ignore')

                # CmdOutput.__str__()
                self.assertEqual(content, str(cmd_output))

                # CmdOutput.output
                self.assertEqual(content, cmd_output.output)

                # CmdOutput.firstline
                self.assertEqual(cmd_output.firstline,
                                 first_line.decode('utf-8', errors='ignore'))

                # test CmdOutput.lines
                self.assertEqual(cmd_output.lines[0],
                                 first_line.decode('utf-8', errors='ignore'))

                self.assertEqual(cmd_output.lines[1],
                                 second_line.decode('utf-8', errors='ignore'))

            # test the case of an empty content
            cmd_output = CmdOutput('')
            cmd_output = CmdOutput(None)
            self.assertEqual(cmd_output.firstline, '')

    tests = unittest.TestLoader().loadTestsFromTestCase(TestCmdOutput)
    ret = unittest.TextTestRunner(verbosity=5).run(tests).wasSuccessful()
    sys.exit(int(not ret))


if __name__ == '__main__':
    main()

# vim:ai:et:sw=4:ts=4:sts=4:tw=78:fenc=utf-8
