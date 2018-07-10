CyPari 2
========

.. image:: https://travis-ci.org/defeo/cypari2.svg?branch=master

A Python interface to the number theory library `libpari <http://pari.math.u-bordeaux.fr/>`_.

This library supports both Python 2 and Python 3.

Installation
------------

GNU/Linux
^^^^^^^^^

A package `python-cypari2` or `python2-cypari2` or `python3-cypari2` might be
available in your package manager.

Using pip
^^^^^^^^^

Requirements:

- PARI/GP >= 2.9.0 (header files and library)
- Python >= 2.7
- pip
- `cysignals <https://pypi.python.org/pypi/cysignals/>`_
- Cython >= 0.28

Install cypari2 via the Python Package Index (PyPI) via

::

    $ pip install cypari2 [--user]

(the optional option *--user* allows to install cypari2 for a single user
and avoids using pip with administrator rights). Depending on your operating
system the pip command might also be called pip2 or pip3.

If you want to try the development version use

::

    $ pip install git+https://github.com/defeo/cypari2.git [--user]

If you have an error saying libpari-gmp*.so* is missing and have all requirements
already installed, try to reinstall cysignals and cypari2

::

    $ pip install cysignals --upgrade [--user]
    $ pip install cypari2 --upgrade [--user]

Other
^^^^^

Any other way to install cypari2 is not supported. In particular, ``python
setup.py install`` will produce an error.

Usage
-----

The interface as been kept as close as possible from PARI/GP. The following
computation in GP

::

    ? zeta(2)
    %1 = 1.6449340668482264364724151666460251892

    ? p = x^3 + x^2 + x - 1;
    ? modulus = t^3 + t^2 + t - 1;
    ? fq = factorff(p, 3, modulus);
    ? centerlift(lift(fq))
    %5 =
    [            x - t 1]

    [x + (t^2 + t - 1) 1]

    [   x + (-t^2 - 1) 1]

translates into

::

    >>> import cypari2
    >>> pari = cypari2.Pari()

    >>> pari(2).zeta()
    1.64493406684823

    >>> p = pari("x^3 + x^2 + x - 1")
    >>> modulus = pari("t^3 + t^2 + t - 1")
    >>> fq = p.factorff(3, modulus)
    >>> fq.lift().centerlift()
    [x - t, 1; x + (t^2 + t - 1), 1; x + (-t^2 - 1), 1]

The object **pari** above is the object for the interface and acts as a
constructor. It can be called with basic Python objects like integer
or floating point. When called with a string as in the last example
the corresponding string is interpreted as if it was executed in a GP shell.

Beyond the interface object **pari** of type **Pari**, any object you get a
handle on is of type **Gen** (that is a wrapper around the **GEN** type from
libpari). All PARI/GP functions are then available in their original names as
*methods* like **zeta**, **factorff**, **lift** or **centerlift** above.

Alternatively, the pari functions are accessible as methods of **pari**. The
same computations be done via

::

    >>> import cypari2
    >>> pari = cypari2.Pari()

    >>> pari.zeta(2)
    1.64493406684823

    >>> p = pari("x^3 + x^2 + x - 1")
    >>> modulus = pari("t^3 + t^2 + t - 1")
    >>> fq = pari.factorff(p, 3, modulus)
    >>> pari.centerlift(pari.lift(fq))
    [x - t, 1; x + (t^2 + t - 1), 1; x + (-t^2 - 1), 1]

The complete documentation of cypari2 is available at http://cypari2.readthedocs.io and
the PARI/GP documentation at http://pari.math.u-bordeaux.fr/doc.html

Contributing
------------

Submit pull request or get in contact with `Luca De Feo <http://defeo.lu/>`_.
