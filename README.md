# CyPari 2

[![Build Status](https://travis-ci.org/defeo/cypari2.svg?branch=master)](https://travis-ci.org/defeo/cypari2)

A Python interface to the number theory library [libpari](http://pari.math.u-bordeaux.fr/).

This library supports both Python 2 and Python 3

## Installation

1) Install libpari

2) Clone the cypari2 project

3) Install with pip:
```
$ cd where_I_cloned_cypari2
$ pip install .
```
Note that any other kind of installation program is not supported.
In particular, ``python setup.py install`` does NOT work.

## Usage

Just launch Python and then you can perform some PARI/GP computation inside python
```
>>> import cypari2
>>> pari = cypari2.Pari()
>>> pari(2).zeta()
1.64493406684823
>>> K = pari("bnfinit(x^3 - 2)")
>>> K.bnfunit()
[x - 1]
```

## Issues

1) If you change your PARI installation you need to recompile cysignals and cypari2 using
the `--no-cache-dir` option of pip

     pip install cysignals --no-cache-dir --force-reinstall [--user]
     pip install cypari2 --no-cache-dir --force-reinstall [--user]

## Contributing

Submit pull request or get in contact with [Luca De Feo](http://defeo.lu/).
