# -*- coding: utf-8 -*-
r"""
Conversion functions for bytes/unicode
"""

import sys
encoding = sys.getfilesystemencoding()

cpdef bytes to_bytes(s):
    """
    Examples:

    >>> from cypari2.string_utils import to_bytes
    >>> s1 = to_bytes(b'hello')
    >>> s2 = to_bytes('hello')
    >>> s3 = to_bytes(u'hello')
    >>> type(s1) == type(s2) == type(s3) == bytes
    True
    >>> s1 == s2 == s3 == b'hello'
    True
    """
    if isinstance(s, bytes):
        return s
    elif isinstance(s, unicode):
        return (<unicode> s).encode(encoding)
    else:
        raise TypeError

cpdef str to_string(s):
    r"""
    Examples:

    >>> from cypari2.string_utils import to_string
    >>> s1 = to_string(b'hello')
    >>> s2 = to_string('hello')
    >>> s3 = to_string(u'hello')
    >>> type(s1) == type(s2) == type(s3) == str
    True
    >>> s1 == s2 == s3 == 'hello'
    True
    """
    if isinstance(s, bytes):
        IF PY_MAJOR_VERSION == 2:
            return s
        ELSE:
            return (<bytes> s).decode(encoding)
    elif isinstance(s, unicode):
        IF PY_MAJOR_VERSION == 2:
            return (<unicode> s).encode(encoding)
        ELSE:
            return s
    else:
        raise TypeError
