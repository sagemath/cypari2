# CyPari 2

A Python interface to the number theory library [libpari](http://pari.math.u-bordeaux.fr/).

## Installation

```
pip install cypari2
```

## Usage

TODO 

1) You need to manually copy the (private) pari header anal.h inside some (public) include
directory. The only reason for this is because of the error handler that access to the function
`closure_func_err` (that returns the name of the GP function that triggers the
error). Bill and Karim seems to be ok to make it public but we might need to make a proper
request on pari-dev mailing list.
This request is somehow weird as it only concerns GP functions

    >>> import cypari2
    >>> pari = cypari2.Pari()
    >>> pari(1).zeta()   # closure_func_err returned NULL
    Traceback (most recent call last):
    ...
    PariError: domain error in zeta: argument = 1
    >>> pari('zeta(1)')  # closure_func_err returned 'zeta'
    Traceback (most recent call last):
    ...
    PariError: zeta: domain error in zeta: argument = 1

2) If you change your pari installation you need to recompile cysignals and cypari2 using
the `--no-cache-dir` option of pip

     pip install cysignals --no-cache-dir --force-reinstall [--user]
     pip install cypari2 --no-cache-dir --force-reinstall [--user]

## Contributing

Good question!
