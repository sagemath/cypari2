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

- PARI/GP (header files and library)
- python >= 2.7
- pip
- `cysignals <https://pypi.python.org/pypi/cysignals/>`_

Install cypari2 via the Python Package Index (PyPI) via

::

    $ pip install cypari2 [--user]

(the optional option *--user* allows to install cypari2 for a single user
and avoids using pip with administrator rights). Depending on your operating
system the pip command might also be called pip2 or pip3.

If you want to try the development version use

::

    $ pip install git+https://github.com/defeo/cypari2.git [--user]

Other
^^^^^

Any other way to install cypari2 is not supported. In particular, ``python
setup.py install`` will produce an error.

Usage
-----

Here is an example of some PARI/GP computations in Python

::

    >>> import cypari2
    >>> pari = cypari2.Pari()

    >>> pari(2).zeta()
    1.64493406684823

    >>> pari(2197).ispower(3)
    (3, 13)

    >>> K = pari("bnfinit(x^3 - 2)")
    >>> K.bnfunit()
    [x - 1]

The object **pari** above is the object for the interface and acts as a
constructor. It can be called with basic Python objects like integer
or floating point. When called with a string as in the last example
the corresponding string is interpreted as if it was executed in a GP shell.

Beyond the interface object **pari** of type **Pari**, any object you get a
handle on is of type **Gen** (that is a wrapper around the **GEN** type from
libpari). All PARI/GP functions are then available in their original names as
*methods* like **zeta**, **ispower** or **bnfunit** above.

The complete documentation is available at http://cypari2.readthedocs.io

Contributing
------------

Submit pull request or get in contact with `Luca De Feo <http://defeo.lu/>`_.
