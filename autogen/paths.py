"""
Find out installation paths of PARI/GP
"""

#*****************************************************************************
#       Copyright (C) 2017 Jeroen Demeyer <jdemeyer@cage.ugent.be>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from __future__ import absolute_import, unicode_literals

import os
from glob import glob
from distutils.spawn import find_executable


# find_executable() returns None if nothing was found
gppath = find_executable("gp")
if gppath is None:
    # This almost certainly won't work, but we need to put something here
    prefix = "."
else:
    # Assume gppath is ${prefix}/bin/gp
    prefix = os.path.dirname(os.path.dirname(gppath))


def pari_share():
    r"""
    Return the directory where the PARI data files are stored.

    EXAMPLES::

        >>> import os
        >>> from autogen.parser import pari_share
        >>> os.path.isfile(os.path.join(pari_share(), "pari.desc"))
        True
    """
    sharedir = os.path.join(prefix, "share", "pari")
    if not os.path.isdir(sharedir):
        raise EnvironmentError("PARI share directory {!r} does not exist".format(sharedir))
    return sharedir


def include_dirs():
    """
    Return the directory containing PARI include files.
    """
    dirs = [os.path.join(prefix, "include")]
    return [d for d in dirs if os.path.isdir(os.path.join(d, "pari"))]


def library_dirs():
    """
    Return the directory containing PARI library files.
    """
    dirs = [os.path.join(prefix, s) for s in ("lib", "lib32", "lib64")]
    return [d for d in dirs if glob(os.path.join(d, "libpari*"))]
