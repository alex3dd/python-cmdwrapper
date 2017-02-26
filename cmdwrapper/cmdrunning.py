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
"""A running command."""

import sys
import platform
import subprocess
from cmdoutput import CmdOutput
from cmdresult import CmdResult
from cmdproc import CmdProc


assert platform.system() == 'Linux'
assert sys.version_info >= (3, 2), "The Python version need to be >= 3.2"


# Used by CmdRunning in the constructor arguments stdout/stderr
PIPE = subprocess.PIPE
DEVNULL = subprocess.DEVNULL
STDOUT = subprocess.STDOUT


class CmdRunning(object):
    """A running process."""

    def __init__(self, cmd_proc):
        """Init the process."""
        assert isinstance(cmd_proc, CmdProc)
        self.proc = cmd_proc
        self.proc.run()  # run the process automatically

    def wait(self):
        """Wait until the process is terminated."""
        self.proc.wait()
        return self

    @property
    def returncode(self):
        """Return the exit code of the command."""
        return self.proc.returncode

    @property
    def stdout(self):
        """Return stdout."""
        self.wait()
        return CmdOutput(self.proc.stdout)

    @property
    def stderr(self):
        """Return stderr."""
        self.wait()
        return CmdOutput(self.proc.stderr)

    @property
    def result(self):
        """Return a CmdResult() instance (stdout, stderr and returncode)."""
        self.wait()
        return CmdResult(stdout=self.proc.stdout,
                         stderr=self.proc.stderr,
                         returncode=self.proc.returncode)


def main():
    """Main function."""
    pass


if __name__ == '__main__':
    main()

# vim:ai:et:sw=4:ts=4:sts=4:tw=78:fenc=utf-8
