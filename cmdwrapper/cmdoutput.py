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
"""The output (stdout, stderr) of a command."""


class CmdOutput(object):
    """The output of a command (like stdout or stderr)."""

    def __init__(self, output):
        """Store the output internally."""
        self._output = self._to_utf8(output)

    def __str__(self):
        """Return the output."""
        return self._output

    @property
    def output(self):
        """String version of the output."""
        return self.__str__()

    @property
    def lines(self):
        """Return the output as a list (each item is a line of the output)."""
        return self._output.splitlines()

    @property
    def firstline(self):
        """First line of the output."""
        if self._output != '':
            return self.lines[0]

        return ''

    def show(self):
        """Print the output."""
        print(self._output)

    @staticmethod
    def _to_utf8(output):
        """Return an unified version of the output."""
        if output is None:
            output = ''
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='ignore')
        assert isinstance(output, str)
        return output


def main():
    """The program starts here."""
    import logging
    import unittest
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s')

    class Test_CmdOutput(unittest.TestCase):
        """Testing the class CmdOutput."""

        def test_cmdoutput(self):
            """Test: CmdOutput()."""
            first_line = b'First Line'
            second_line = b'Second Line'
            byte_content = first_line + b'\n' + second_line

            for content in [byte_content, str(byte_content)]:
                cmd_output = CmdOutput(content)

                if isinstance(content, bytes):
                    content = content.decode('utf-8')

                # CmdOutput.__str__()
                self.assertEqual(content, str(cmd_output.output))

                # CmdOutput.output
                self.assertEqual(content, cmd_output.output)

                # test CmdOutput.lines
                self.assertEqual(cmd_output.lines[0],
                                 first_line.decode('utf-8'))

                self.assertEqual(cmd_output.lines[1],
                                 second_line.decode('utf-8'))

    tests = unittest.TestLoader().loadTestsFromTestCase(Test_CmdOutput)
    unittest.TextTestRunner(verbosity=5).run(tests)


if __name__ == '__main__':
    main()

# vim:ai:et:sw=4:ts=4:sts=4:tw=78:fenc=utf-8
