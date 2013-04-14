pstatus: Status code helper utility
===================================

pstatus is can be used to extract meaning from process status codes as returned
by ``os.system``, ``os.wait``, ``os.waitpid``, as well as ``subprocess.call``,
``subprocess.CalledProcessError.returncode``, ``subprocess.Popen.call``,
``subprocess.Popen.wait``, and ``subprocess.Popen.returncode``.

It exports one function ``split`` which extracts an exit code, a signal number,
a flag indicating whether or not the process left a core dump behind.

``API`` documentation is available at ReadTheDocs_.


Usage
-----

With ``os.system``:

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

With ``subprocess.call``:

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


.. _ReadTheDocs: https://pstatus.readthedocs.org/en/latest/
