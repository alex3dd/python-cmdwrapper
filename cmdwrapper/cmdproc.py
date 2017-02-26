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
import shlex
import logging
import subprocess


assert platform.system() == 'Linux'
assert sys.version_info >= (3, 2), "The Python version need to be >= 3.2"


# Used by CmdRunning in the constructor arguments stdout/stderr
PIPE = subprocess.PIPE
DEVNULL = subprocess.DEVNULL
STDOUT = subprocess.STDOUT


class CmdProcError(Exception):
    """Exception raised when a command fails (returncode != 0)."""

    def __init__(self, error_msg, cmd_proc=None):
        """Store the cmd_proc (which contains stdout, stderr, returncode).

        error_msg: the Python exception's error message (string)
        cmd_proc: the cmd_proc instance

        """
        assert isinstance(error_msg, str)
        if cmd_proc is not None:
            assert isinstance(cmd_proc, CmdProc)

        self._error_msg = error_msg
        self._cmd_proc = cmd_proc
        super().__init__(self._error_msg)


class CmdProc(object):
    """Low level process management (run process, wait until completed...)."""

    # pylint: disable=redefined-builtin
    def __init__(self, cmd, cwd=None, env=None, stdout=PIPE, stderr=PIPE,
                 input=None, timeout=None):
        """Init the process.

        :cmd: the command line arguments. Example: ['ls', '/'] or 'ls /'

        :cwd: the directory where the command is going to be executed
              (None = current directory)

        :env: rewrite the environment variables (key/value)

        :stdout: could contain PIPE, DEVNULL and STDOUT. Behaves exactly like
                 Popen's argument stdout.

        :stderr: could contain PIPE, DEVNULL and STDOUT. Behaves exactly like
                 Popen's argument stderr.

        :input: the input content. Equivalent to 'input' in Popen.communicate.

        :timeout: SIGTERM will be sent to the process after 'timeout' seconds.
        To disable this feature: 'timeout=None'.

        """
        if cmd:
            assert isinstance(cmd, (list, str))

        if cwd:
            assert isinstance(cwd, str)

        if env:
            assert isinstance(env, dict)

        assert stdout in (PIPE, DEVNULL, STDOUT, None)
        assert stderr in (PIPE, DEVNULL, STDOUT, None)

        if input:
            assert isinstance(input, bytes)

        if timeout:
            assert isinstance(timeout, int)

        self._cmd_list, self._cmd_str = self._cmd_split_types(cmd)

        # used by process opener
        self._opts = {'cwd': cwd,
                      'env': env,
                      'stdout': stdout,
                      'stderr': stderr,
                      'input': input,
                      'timeout': timeout}

        self._proc = None

        self.returncode = None
        self.stdout = b''
        self.stderr = b''

    def run(self):
        """Run the command."""
        # Avoid running the process 2 times
        if self._proc is not None:
            return False

        if self._opts['cwd'] or self._opts['timeout']:
            logging.debug('[RUN-OPTIONS] CWD:%s TIMEOUT:%s',
                          str(self._opts['cwd']), str(self._opts['timeout']))

        logging.debug('[RUN-CMD] %s', self._cmd_str)

        # Run the process
        self._proc = subprocess.Popen(args=self._cmd_list,
                                      stdout=self._opts['stdout'],
                                      stderr=self._opts['stderr'],
                                      cwd=self._opts['cwd'],
                                      env=self._opts['env'])

        return True

    def wait(self):
        """Wait until the process is terminated."""
        if self._proc is None:
            self.run()

        if self._proc.poll() is not None:
            # The process is stopped
            return False

        self.returncode = None
        self.stdout = b''
        self.stderr = b''
        try:
            self.stdout, self.stderr = \
                self._proc.communicate(input=self._opts['input'],
                                       timeout=self._opts['timeout'])
            self.returncode = self._proc.returncode

            if self.returncode != 0:
                raise CmdProcError('exit-code {} return by: {}'
                                   .format(self.returncode,
                                           self._cmd_str), self)
        except (subprocess.CalledProcessError, CmdProcError) as err:
            raise CmdProcError(self._cmd_error_msg(str(err)), self)

        return True

    def _cmd_error_msg(self, err_msg):
        """Return a string you can use for the command's exception."""
        error_msg = '{}\n\nCOMMAND: {}\n\nCOMMAND OUTPUT: {}{}\n' \
                    .format(err_msg,
                            self._cmd_str,
                            self.stdout,
                            self.stderr)
        return error_msg

    @staticmethod
    def _cmd_split_types(cmd):
        """Convert a command 'cmd' to list + str."""
        assert isinstance(cmd, (list, str))

        if isinstance(cmd, str):
            cmd_list = shlex.split(cmd)
            cmd_str = cmd
        elif isinstance(cmd, list):
            cmd_list = cmd

            # just for the output. Don't use cmd_str to execute.
            cmd_str = ' '.join(cmd)
        else:
            raise TypeError

        assert isinstance(cmd_list, list)
        assert isinstance(cmd_str, str)

        return cmd_list, cmd_str


def main():
    """Main function."""
    pass


if __name__ == '__main__':
    main()

# vim:ai:et:sw=4:ts=4:sts=4:tw=78:fenc=utf-8
