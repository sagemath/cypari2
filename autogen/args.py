"""
Arguments for PARI calls
"""

#*****************************************************************************
#       Copyright (C) 2015 Jeroen Demeyer <jdemeyer@cage.ugent.be>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from __future__ import unicode_literals

# Some replacements for reserved words
replacements = {'char': 'character', 'return': 'return_value'}

class PariArgument(object):
    """
    This class represents one argument in a PARI call.
    """
    def __init__(self, namesiter, default, index):
        """
        Create a new argument for a PARI call.

        INPUT:

        - ``namesiter`` -- iterator over all names of the arguments.
          Usually, the next name from this iterator is used as argument
          name.

        - ``default`` -- default value for this argument (``None``
          means that the argument is not optional).

        - ``index`` -- (integer >= 0). Index of this argument in the
          list of arguments. Index 0 means a ``"self"`` argument which
          is treated specially. For a function which is not a method,
          start counting at 1.
        """
        self.index = index
        try:
            self.name = self.get_argument_name(namesiter)
        except StopIteration:
            # No more names available, use something default.
            # This is used in listcreate() and polsturm() for example
            # which have deprecated arguments which are not listed in
            # the help.
            self.name = "_arg%s" % index
            self.undocumented = True
        else:
            self.undocumented = False

        if self.index == 0:  # "self" argument can never have a default
            self.default = None
        elif default is None:
            self.default = self.always_default()
        elif default == "":
            self.default = self.default_default()
        else:
            self.default = default

        # Name for a temporary variable. Only a few classes actually use this.
        self.tmpname = "_" + self.name

    def __repr__(self):
        s = self._typerepr() + " " + self.name
        if self.default is not None:
            s += "=" + self.default
        return s

    def _typerepr(self):
        """
        Return a string representing the type of this argument.
        """
        return "(generic)"

    def ctype(self):
        """
        The corresponding C type. This is used for auto-generating
        the declarations of the C function. In some cases, this is also
        used for passing the argument from Python to Cython.
        """
        raise NotImplementedError

    def always_default(self):
        """
        If this returns not ``None``, it is a value which is always
        the default for this argument, which is then automatically
        optional.
        """
        return None

    def default_default(self):
        """
        The default value for an optional argument if no other default
        was specified in the prototype.
        """
        return "NULL"

    def get_argument_name(self, namesiter):
        """
        Return the name for this argument, given ``namesiter`` which is
        an iterator over the argument names given by the help string.
        """
        n = next(namesiter)
        try:
            return replacements[n]
        except KeyError:
            return n

    def prototype_code(self):
        """
        Return code to appear in the prototype of the Cython wrapper.
        """
        raise NotImplementedError

    def deprecation_warning_code(self, function):
        """
        Return code to appear in the function body to give a
        deprecation warning for this argument, if applicable.
        ``function`` is the function name to appear in the message.
        """
        if not self.undocumented:
            return ""
        s  = "        if {name} is not None:\n"
        s += "            from warnings import warn\n"
        s += "            warn('argument {index} of the PARI/GP function {function} is undocumented and deprecated', DeprecationWarning)\n"
        return s.format(name=self.name, index=self.index, function=function)

    def convert_code(self):
        """
        Return code to appear in the function body to convert this
        argument to something that PARI understand. This code can also
        contain extra checks. It will run outside of ``sig_on()``.
        """
        return ""

    def c_convert_code(self):
        """
        Return additional conversion code which will be run after
        ``convert_code`` and inside the ``sig_on()`` block. This must
        not involve any Python code (in particular, it should not raise
        exceptions).
        """
        return ""

    def call_code(self):
        """
        Return code to put this argument in a PARI function call.
        """
        return self.name


class PariArgumentObject(PariArgument):
    """
    Class for arguments which are passed as generic Python ``object``.
    """
    def prototype_code(self):
        """
        Return code to appear in the prototype of the Cython wrapper.
        """
        s = self.name
        if self.default is not None:
            # Default corresponds to None, actual default value should
            # be handled in convert_code()
            s += "=None"
        return s

class PariArgumentClass(PariArgument):
    """
    Class for arguments which are passed as a specific C/Cython class.

    The C/Cython type is given by ``self.ctype()``.
    """
    def prototype_code(self):
        """
        Return code to appear in the prototype of the Cython wrapper.
        """
        s = self.ctype() + " " + self.name
        if self.default is not None:
            s += "=" + self.default
        return s


class PariInstanceArgument(PariArgumentObject):
    """
    ``self`` argument for ``Pari`` object.

    This argument is never actually used.
    """
    def __init__(self):
        PariArgument.__init__(self, iter(["self"]), None, 0)
    def _typerepr(self):
        return "Pari"
    def ctype(self):
        return "GEN"


class PariArgumentGEN(PariArgumentObject):
    def _typerepr(self):
        return "GEN"
    def ctype(self):
        return "GEN"
    def convert_code(self):
        """
        Conversion to Gen
        """
        if self.index == 0:
            # self argument
            s  = ""
        elif self.default is None:
            s  = "        {name} = objtogen({name})\n"
        elif self.default is False:
            # This is actually a required argument
            # See parse_prototype() in parser.py why we need this
            s  = "        if {name} is None:\n"
            s += "            raise TypeError(\"missing required argument: '{name}'\")\n"
            s += "        {name} = objtogen({name})\n"
        else:
            s  = "        cdef bint _have_{name} = ({name} is not None)\n"
            s += "        if _have_{name}:\n"
            s += "            {name} = objtogen({name})\n"
        return s.format(name=self.name)
    def c_convert_code(self):
        """
        Conversion Gen -> GEN
        """
        if not self.default:
            # required argument
            s  = "        cdef GEN {tmp} = (<Gen>{name}).g\n"
        elif self.default == "NULL":
            s  = "        cdef GEN {tmp} = NULL\n"
            s += "        if _have_{name}:\n"
            s += "            {tmp} = (<Gen>{name}).g\n"
        elif self.default == "0":
            s  = "        cdef GEN {tmp} = gen_0\n"
            s += "        if _have_{name}:\n"
            s += "            {tmp} = (<Gen>{name}).g\n"
        else:
            raise ValueError("default value %r for GEN argument %r is not supported" % (self.default, self.name))
        return s.format(name=self.name, tmp=self.tmpname)
    def call_code(self):
        return self.tmpname

class PariArgumentString(PariArgumentObject):
    def _typerepr(self):
        return "str"
    def ctype(self):
        return "char *"
    def convert_code(self):
        if self.default is None:
            s  = "        {name} = to_bytes({name})\n"
            s += "        cdef char* {tmp} = <bytes>{name}\n"
        else:
            s  = "        cdef char* {tmp}\n"
            s += "        if {name} is None:\n"
            s += "            {tmp} = {default}\n"
            s += "        else:\n"
            s += "            {name} = to_bytes({name})\n"
            s += "            {tmp} = <bytes>{name}\n"
        return s.format(name=self.name, tmp=self.tmpname, default=self.default)
    def call_code(self):
        return self.tmpname

class PariArgumentVariable(PariArgumentObject):
    def _typerepr(self):
        return "var"
    def ctype(self):
        return "long"
    def default_default(self):
        return "-1"
    def convert_code(self):
        if self.default is None:
            s  = "        cdef long {tmp} = get_var({name})\n"
        else:
            s  = "        cdef long {tmp} = {default}\n"
            s += "        if {name} is not None:\n"
            s += "            {tmp} = get_var({name})\n"
        return s.format(name=self.name, tmp=self.tmpname, default=self.default)
    def call_code(self):
        return self.tmpname

class PariArgumentLong(PariArgumentClass):
    def _typerepr(self):
        return "long"
    def ctype(self):
        return "long"
    def default_default(self):
        return "0"

class PariArgumentULong(PariArgumentClass):
    def _typerepr(self):
        return "unsigned long"
    def ctype(self):
        return "unsigned long"
    def default_default(self):
        return "0"

class PariArgumentPrec(PariArgumentClass):
    def _typerepr(self):
        return "prec"
    def ctype(self):
        return "long"
    def always_default(self):
        return "DEFAULT_BITPREC"
    def get_argument_name(self, namesiter):
        return "precision"
    def c_convert_code(self):
        s = "        {name} = nbits2prec({name})\n"
        return s.format(name=self.name)

class PariArgumentBitprec(PariArgumentClass):
    def _typerepr(self):
        return "bitprec"
    def ctype(self):
        return "long"
    def always_default(self):
        return "DEFAULT_BITPREC"
    def get_argument_name(self, namesiter):
        return "precision"

class PariArgumentSeriesPrec(PariArgumentClass):
    def _typerepr(self):
        return "serprec"
    def ctype(self):
        return "long"
    def default_default(self):
        return "-1"
    def get_argument_name(self, namesiter):
        return "serprec"
    def c_convert_code(self):
        s  = "        if {name} < 0:\n"
        s += "            {name} = precdl  # Global PARI series precision\n"
        return s.format(name=self.name)

class PariArgumentGENPointer(PariArgumentObject):
    default = "NULL"
    def _typerepr(self):
        return "GEN*"
    def ctype(self):
        return "GEN*"
    def convert_code(self):
        """
        Conversion to NULL or Gen
        """
        s  = "        cdef bint _have_{name} = ({name} is not None)\n"
        s += "        if _have_{name}:\n"
        s += "            raise NotImplementedError(\"optional argument {name} not available\")\n"
        return s.format(name=self.name)
    def c_convert_code(self):
        """
        Conversion Gen -> GEN
        """
        s  = "        cdef GEN * {tmp} = NULL\n"
        return s.format(name=self.name, tmp=self.tmpname)
    def call_code(self):
        return self.tmpname


pari_arg_types = {
        'G': PariArgumentGEN,
        'W': PariArgumentGEN,
        'r': PariArgumentString,
        's': PariArgumentString,
        'L': PariArgumentLong,
        'U': PariArgumentULong,
        'n': PariArgumentVariable,
        'p': PariArgumentPrec,
        'b': PariArgumentBitprec,
        'P': PariArgumentSeriesPrec,
        '&': PariArgumentGENPointer,

    # Codes which are known but not actually supported yet
        'V': None,
        'I': None,
        'E': None,
        'J': None,
        'C': None,
        '*': None,
        '=': None}
