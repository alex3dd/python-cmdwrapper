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
"""Wrap any Linux command and run it as a Python method."""

import sys
from copy import deepcopy
from pprint import pformat
from subprocess import PIPE, DEVNULL, STDOUT
from cmdwrapper.cmdoutput import CmdOutput
from cmdwrapper.cmdproc import CmdProc
from cmdwrapper.cmdproc import CmdProcError    # noqa


assert sys.version_info >= (3, 3), "The Python version need to be >= 3.3"


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
        return str(self.stdout) + str(self.stderr)


class CmdRunning(object):
    """A running process."""

    def __init__(self, cmd_proc):
        """Init the process."""
        assert isinstance(cmd_proc, CmdProc)
        self.proc = cmd_proc
        self.proc.run()  # run the process automatically

    def wait(self):
        """Wait until the process is terminated.

        If the returncode != 0 an exception will be raised.

        """
        self.proc.wait()
        return self

    @property
    def returncode(self):
        """Return the exit code of the command."""
        self.wait()
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

    def __iter__(self):
        """Iter through stdout."""
        # TODO: implement an stdout reader that can read from stdout while SSH
        #       is running
        for line in self.stdout.lines:
            yield line


class CmdWrapper(object):
    """Wrap any Linux command and run it as a Python method."""

    def __init__(self, cmd=None, *args):
        """Command + arguments to wrap.

        :cmd: the command.
        :*args: the command's arguments.

        Example:
        >>> ssh = CmdWrapper('ssh', '-vvvv')
        >>> ssh('server', 'ls', '/')

        """
        if cmd is not None:
            assert isinstance(cmd, str)

        self._cmd = None
        self._args = None
        self.cmd(cmd)
        self.args(*args)

        self._cmd_proc_kwargs = {}

    def __call__(self, *args, **cmd_proc_kwargs):
        """Run the command."""
        if self._cmd is None:
            cmd_args = []
        else:
            cmd_args = [self._cmd]

        cmd_args = cmd_args + self._args + list(args)

        kwargs = deepcopy(self._cmd_proc_kwargs)
        kwargs.update(cmd_proc_kwargs)

        cmd_proc = CmdProc(cmd=cmd_args, **kwargs)
        return CmdRunning(cmd_proc)

    def __repr__(self):
        """Return the repr."""
        return pformat({'cmd': self._cmd, 'args': self._args,
                        'cmd_proc_kwargs': self._cmd_proc_kwargs})

    def timeout(self, timeout):
        """The default timeout."""
        assert isinstance(timeout, int)
        self._cmd_proc_kwargs['timeout'] = timeout
        return self

    def get(self, option):
        """Return an option's value (env, cwd, cmd, args, etc.)."""
        try:
            return self._cmd_proc_kwargs[option]
        except KeyError:
            return None

    def env(self, env):
        """A dict with the environment variables."""
        assert isinstance(env, dict)
        self._cmd_proc_kwargs['env'] = env
        return self

    def cwd(self, cwd):
        """The directory from where the command is going to be started."""
        assert isinstance(cwd, str)
        self._cmd_proc_kwargs['cwd'] = cwd
        return self

    def cmd(self, cmd):
        """Change the cmd."""
        if cmd:
            assert isinstance(cmd, (str, list))

        self._cmd = cmd
        return self

    def args(self, *args):
        """Change the command's arguments."""
        args = list(args)
        for arg in args:
            assert isinstance(arg, str)

        self._args = list(args)
        return self

    def copy(self):
        """Copy the object."""
        return deepcopy(self)

    def input(self, content):
        """The stdin's content."""
        assert isinstance(content, bytes)
        self._cmd_proc_kwargs['input'] = content
        return self

    def output(self, stdout=PIPE, stderr=PIPE):
        """Modify the output. Values: PIPE, DEVNULL, STDOUT or None."""
        assert stdout in (PIPE, DEVNULL, STDOUT, None)
        assert stderr in (PIPE, DEVNULL, STDOUT, None)
        self._cmd_proc_kwargs['stdout'] = stdout
        self._cmd_proc_kwargs['stderr'] = stderr
        return self


def main():
    """Test the class CmdResult."""
    import unittest

    class TestCmdResult(unittest.TestCase):
        """Testing the class CmdResult."""

        def test_cmdoutput(self):
            """Test: CmdResult()."""
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

    class TestCmdWrapper(unittest.TestCase):
        """Testing the class CmdWrapper."""

        def test_cmdwrapper(self):
            """Test: CmdWrapper()."""
            cmd_wrapper = CmdWrapper()
            running = cmd_wrapper('bash', '-c', 'echo TEST')
            self.assertEqual(running.stdout.firstline, 'TEST')

            bash = CmdWrapper('bash')
            repr(bash)

            bash.cmd('bash').args('-c').cwd('/').timeout(2).output()
            self.assertEqual(bash.get('cwd'), '/')
            self.assertRaises(KeyError, bash.get('HelloWorld'))
            bash.env({'TEST': 'HIWORLD'})

            bash_copy = bash.copy()
            # pylint: disable=protected-access
            self.assertNotEqual(id(bash_copy._args), id(bash._args))

            running = bash('echo $TEST')
            self.assertEqual(running.stdout.firstline, 'HIWORLD')

            running = bash('pwd')
            self.assertEqual(running.stdout.firstline, '/')

            bash.input(b'HIWORLD')
            running = bash('cat')
            self.assertEqual(running.stdout.firstline, 'HIWORLD')

            cmd_result = running.result
            self.assertEqual(str(running.stdout), str(cmd_result.stdout))
            self.assertEqual(str(running.stderr), str(cmd_result.stderr))
            self.assertEqual(running.returncode, cmd_result.returncode)

    class TestCmdRunning(unittest.TestCase):
        """Testing the class CmdRunning."""

        def test_cmdrunning(self):
            """Test: CmdRunning()."""
            running = CmdRunning(CmdProc('bash -c "echo HIWORLD"'))
            self.assertEqual(running.stdout.firstline, 'HIWORLD')

            running = CmdRunning(CmdProc('bash -c "echo HIWORLD >&2"'))
            self.assertEqual(running.stderr.firstline, 'HIWORLD')

            running = CmdRunning(CmdProc('true'))
            self.assertEqual(running.returncode, 0)

    ret = 0

    tests = unittest.TestLoader().loadTestsFromTestCase(TestCmdResult)
    ret |= unittest.TextTestRunner(verbosity=5).run(tests).wasSuccessful()

    tests = unittest.TestLoader().loadTestsFromTestCase(TestCmdRunning)
    ret |= unittest.TextTestRunner(verbosity=5).run(tests).wasSuccessful()

    tests = unittest.TestLoader().loadTestsFromTestCase(TestCmdWrapper)
    ret |= unittest.TextTestRunner(verbosity=5).run(tests).wasSuccessful()

    sys.exit(int(not ret))


if __name__ == '__main__':
    main()

# vim:ai:et:sw=4:ts=4:sts=4:tw=78:fenc=utf-8
