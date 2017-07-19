CyPari 2
========

.. image:: https://travis-ci.org/defeo/cypari2.svg?branch=master

A Python interface to the number theory library `libpari <http://pari.math.u-bordeaux.fr/>`_.

This library supports both Python 2 and Python 3.

Installation
------------

We describe here how to install cypari2. Any other kind of installation
is not supported. In particular, ``python setup.py install`` does NOT work.

GNU/Linux
^^^^^^^^^

Check if a package `python-cypari2` or `python2-cypari2` or `python3-cypari2`
is available through your package manager.

Generic install via PyPI
^^^^^^^^^^^^^^^^^^^^^^^^

1. Install libpari, pip, cysignals

2. Install cypari2 via the Python Package Index (PyPI) via::

    $ pip install cypari2 [--user]

(the optional option *--user* allows to install cypari2 for a single user
and avoids using pip with administrator rights)

Development version
^^^^^^^^^^^^^^^^^^^

If you want to try the development version, you can replace step 2
of the "Generic install via PyPI" by

::

    $ pip install git+https://github.com/defeo/cypari2.git [--user]


Usage
-----

Just launch Python and then you can perform some PARI/GP computation

::

    >>> import cypari2
    >>> pari = cypari2.Pari()
    >>> pari(2).zeta()
    1.64493406684823

    >>> K = pari("bnfinit(x^3 - 2)")
    >>> K.bnfunit()
    [x - 1]

The object **pari** above is the object for the interface. It can be called
with basic Python objects like integer or floating point. When called with
a string as in the second example above, the corresponding code is interpreted
by libpari

Any object you get a handle on is of type **Gen** (that is a wrapper around the
**GEN** type from libpari). All PARI/GP functions are then available as *method*
of the object **Gen**.

Issues
------

1) If you change your PARI installation you need to recompile cysignals and cypari2 using
the *--no-cache-dir* option of pip

::

     pip install cysignals --no-cache-dir --force-reinstall [--user]
     pip install cypari2 --no-cache-dir --force-reinstall [--user]

Contributing
------------

Submit pull request or get in contact with `Luca De Feo <http://defeo.lu/>`_.
