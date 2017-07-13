# -*- coding: utf-8 -*-
r"""
Conversion functions for bytes/unicode
"""

import sys
encoding = sys.getfilesystemencoding()

cpdef bytes to_bytes(s):
    """
    Converts bytes and unicode ``s`` to bytes.

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
        return <bytes> s
    elif isinstance(s, unicode):
        return (<unicode> s).encode(encoding)
    else:
        raise TypeError

cpdef unicode to_unicode(s):
    r"""
    Converts bytes and unicode ``s`` to unicode.

    Examples:

    >>> from cypari2.string_utils import to_unicode
    >>> s1 = to_unicode(b'hello')
    >>> s2 = to_unicode('hello')
    >>> s3 = to_unicode(u'hello')
    >>> import sys
    >>> u_type = (unicode if sys.version_info.major <= 2 else str)
    >>> type(s1) == type(s2) == type(s3) == u_type
    True
    >>> s1 == s2 == s3 == u'hello'
    True
    """
    if isinstance(s, bytes):
        return (<bytes> s).decode(encoding)
    elif isinstance(s, unicode):
        return <unicode> s
    else:
        raise TypeError

