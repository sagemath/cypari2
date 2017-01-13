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
error). Bill seems to be ok to make it public but we need to make a proper
request on pari-dev mailing list.

2) If you change your pari installation you need to recompile cysignals and cypari2 using
the `--no-cache-dir` option of pip

     pip install cysignals --no-cache-dir --force-reinstall [--user]
     pip install cypari2 --no-cache-dir --force-reinstall [--user]

## Contributing

Good question!
