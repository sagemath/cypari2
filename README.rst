CyPari 2
========

.. image:: https://readthedocs.org/projects/cypari2/badge/?version=latest
    :target: https://cypari2.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

A Python interface to the number theory library `PARI/GP <http://pari.math.u-bordeaux.fr/>`_.

Installation
------------

From a distribution package (GNU/Linux, conda-forge)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A package might be available in your package manager, see
https://repology.org/project/python:cypari2/versions or
https://doc.sagemath.org/html/en/reference/spkg/cypari for
installation instructions.


From a pre-built wheel from PyPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Requirements:

- Python >= 3.9
- pip

Install cypari2 via the Python Package Index (PyPI) via

::

    $ pip install cypari2 [--user]

(the optional option *--user* allows to install cypari2 for a single user
and avoids using pip with administrator rights).


From source with pip
^^^^^^^^^^^^^^^^^^^^

Requirements:

- PARI/GP >= 2.9.4 (header files and library); see
  https://doc.sagemath.org/html/en/reference/spkg/pari#spkg-pari
  for availability in distributions (GNU/Linux, conda-forge, Homebrew, FreeBSD),
  or install from source.
- Python >= 3.9
- pip
- `cysignals <https://pypi.python.org/pypi/cysignals/>`_ >= 1.11.3
- Cython >= 3.0

Install cypari2 via the Python Package Index (PyPI) via

::

    $ pip install --no-binary cypari2 cypari2 [--user]

(the optional option *--user* allows to install cypari2 for a single user
and avoids using pip with administrator rights).

`pip` builds the package using build isolation.  All Python build dependencies
of the package, declared in pyproject.toml, are automatically installed in
a temporary virtual environment.

If you want to try the development version, use

::

    $ pip install git+https://github.com/sagemath/cypari2.git [--user]


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

CyPari 2 is maintained by the SageMath community.

Open issues or submit pull requests at https://github.com/sagemath/cypari2
and join https://groups.google.com/group/sage-devel to discuss.
