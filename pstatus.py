'''
pstatus: Status code helper utility
===================================

pstatus is can be used to extract meaning from process status codes as returned
by ``os.system``, ``os.wait``, ``os.waitpid``, as well as ``subprocess.call``,
``subprocess.CalledProcessError.returncode``, ``subprocess.Popen.call``,
``subprocess.Popen.wait``, and ``subprocess.Popen.returncode``.

It exports one function ``split`` which extracts an exit code, a signal number,
a flag indicating whether or not the process left a core dump behind.
'''
from collections import namedtuple
import os

__version__ = '1.0.0'

__all__ = ['Status', 'split']


class Status(namedtuple('Status', ['exit', 'signal', 'core'])):
    """
    This object may be accessed as either a ``tuple`` of ``(exit, signal,
    core)`` or via the attributes ``exit``, ``signal``, and ``core``.
    Additionally another attribute ``ok`` is defined which indicates whether or
    not the process exited successfully.
    """
    @property
    def ok(self):
        """
        Returns whether or not the process exited successfully
        """
        return (self.exit == 0)


def split(status, subprocess=False):
    """
    Split an exit status code as returned by ``os.system``, ``os.wait``, or
    ``os.waitpid``, returning a ``tuple`` which includes the processes exit
    code, the signal responsible for the processes termination, and whether or
    not the process left a core dump behind. If there was no exit code then the
    first value will be ``None``, and if there was no signal, then the second
    value will be ``None``.

    Optionally, and perhaps with less utility, if a second flag is passed and
    set to ``True``, will ``split`` a ``returncode`` as returned by the
    ``subprocess`` module. In this instance the ``core`` part of the returned
    ``3-tuple`` will always be ``None``, because that information is
    unavailable.

    For example, with ``os.system``:

    >>> split(os.system('true'))
    Status(exit=0, signal=None, core=False)
    >>> split(os.system('false'))
    Status(exit=1, signal=None, core=False)

    Using ``os.spawnlp`` and ``os.kill`` to demonstrate extraction of signals:

    >>> pid = os.spawnlp(os.P_NOWAIT, 'sleep', 'sleep', '100')
    >>> os.kill(pid, 15)
    >>> _, code = os.waitpid(pid, 0)
    >>> split(code)
    Status(exit=None, signal=15, core=False)

    And now with ``subprocess.call``:

    >>> import subprocess
    >>> split(subprocess.call(['true']), subprocess=True)
    Status(exit=0, signal=None, core=None)
    >>> split(subprocess.call(['false']), subprocess=True)
    Status(exit=1, signal=None, core=None)

    Using ``subprocess.Popen`` and ``subprocess.Popen.kill`` to extract
    signals:

    >>> p = subprocess.Popen(['sleep', '100'])
    >>> p.terminate()
    >>> split(p.wait(), subprocess=True)
    Status(exit=None, signal=15, core=None)

    :param status: status code to split
    :type status: ``int``
    :param subprocess: flag indicating supplied status is a ``subprocess``
        returncode
    :type subprocess: ``bool``
    :returns:  ``3-tuple`` (exit, signal, core)
    :rtype: ``3-tuple``
    """
    if subprocess:
        if status >= 0:
            signal, code, core = (None, status, None)
        else:
            signal, code, core = (abs(status), None, None)
    else:
        if os.WIFSIGNALED(status):
            signal = os.WTERMSIG(status)
        else:
            signal = None
        if os.WIFEXITED(status):
            code = os.WEXITSTATUS(status)
        else:
            code = None
        core = os.WCOREDUMP(status)
    return Status(code, signal, core)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
