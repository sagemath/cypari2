# -*- coding: utf-8 -*-
"""
Handle PARI documentation
"""

from __future__ import unicode_literals
import re
import subprocess


leading_ws = re.compile("^( +)", re.MULTILINE)
trailing_ws = re.compile("( +)$", re.MULTILINE)
double_space = re.compile("  +")

end_space = re.compile(r"(@\[end[a-z]*\])([A-Za-z])")
end_paren = re.compile(r"(@\[end[a-z]*\])([(])")

begin_verb = re.compile(r"@1")
end_verb = re.compile(r"@[23] *@\[endcode\]")
verb_loop = re.compile("^(    .*)@\[[a-z]*\]", re.MULTILINE)

dollars = re.compile(r"@\[dollar\]\s*(.*?)\s*@\[dollar\]", re.DOTALL)
doubledollars = re.compile(r"@\[doubledollar\]\s*(.*?)\s*@\[doubledollar\] *", re.DOTALL)

math_loop = re.compile(r"(@\[start[A-Z]*MATH\][^@]*)@\[[a-z]*\]")
math_backslash = re.compile(r"(@\[start[A-Z]*MATH\][^@]*)=BACKSLASH=")

prototype = re.compile("^[^\n]*\n\n")
library_syntax = re.compile("The library syntax is.*", re.DOTALL)

newlines = re.compile("\n\n\n\n*")

bullet_loop = re.compile("(@BULLET(  [^\n]*\n)*)([^ \n])")
indent_math = re.compile("(@\\[startDISPLAYMATH\\].*\n(.+\n)*)(\\S)")

escape_backslash = re.compile(r"^(\S.*)[\\]", re.MULTILINE)
escape_mid = re.compile(r"^(\S.*)[|]", re.MULTILINE)
escape_percent = re.compile(r"^(\S.*)[%]", re.MULTILINE)
escape_hash = re.compile(r"^(\S.*)[#]", re.MULTILINE)

label_define = re.compile(r"@\[label [a-zA-Z0-9:]*\]")
label_ref = re.compile(r"(Section *)?@\[startref\](se:)?([^@]*)@\[endref\]")


def sub_loop(regex, repl, text):
    """
    In ``text``, substitute ``regex`` by ``repl`` recursively. As long
    as substitution is possible, ``regex`` is substituted.

    INPUT:

    - ``regex`` -- a compiled regular expression

    - ``repl`` -- replacement text

    - ``text`` -- input text

    OUTPUT: substituted text

    EXAMPLES:

    Ensure there a space between any 2 letters ``x``::

        >>> from autogen.doc import sub_loop
        >>> import re
        >>> print(sub_loop(re.compile("xx"), "x x", "xxx_xx"))
        x x x_x x
    """
    while True:
        text, n = regex.subn(repl, text)
        if not n:
            return text


def raw_to_rest(doc):
    r"""
    Convert raw PARI documentation (with ``@``-codes) to reST syntax.

    INPUT:

    - ``doc`` -- the raw PARI documentation

    OUTPUT: a unicode string

    EXAMPLES::

        >>> from autogen.doc import raw_to_rest
        >>> print(raw_to_rest(b"@[startbold]hello world@[endbold]"))
        :strong:`hello world`

    TESTS::

        >>> raw_to_rest(b"@[invalid]")
        Traceback (most recent call last):
        ...
        SyntaxError: @ found: @[invalid]

        >>> s = b'@3@[startbold]*@[endbold] snip @[dollar]0@[dollar]\ndividing @[dollar]#E@[dollar].'
        >>> print(raw_to_rest(s))
        - snip :math:`0`
          dividing :math:`\#E`.
    """
    doc = doc.decode("utf-8")

    # Work around a specific problem with doc of "component"
    doc = doc.replace("[@[dollar]@[dollar]]", "[]")

    # Work around a specific problem with doc of "algdivl"
    doc = doc.replace(r"\y@", r"\backslash y@")

    # Special characters
    doc = doc.replace("@[lt]", "<")
    doc = doc.replace("@[gt]", ">")
    doc = doc.replace("@[pm]", "±")
    doc = doc.replace("@[nbrk]", "\xa0")
    doc = doc.replace("@[agrave]", "à")
    doc = doc.replace("@[aacute]", "á")
    doc = doc.replace("@[eacute]", "é")
    doc = doc.replace("@[ouml]", "ö")
    doc = doc.replace("@[uuml]", "ü")
    doc = doc.replace("\\'{a}", "á")

    # Remove leading and trailing whitespace from every line
    doc = leading_ws.sub("", doc)
    doc = trailing_ws.sub("", doc)

    # Remove multiple spaces
    doc = double_space.sub(" ", doc)

    # Sphinx dislikes inline markup immediately followed by a letter:
    # insert a non-breaking space
    doc = end_space.sub("\\1\xa0\\2", doc)

    # Similarly, for inline markup immediately followed by an open
    # parenthesis, insert a space
    doc = end_paren.sub("\\1 \\2", doc)

    # Fix labels and references
    doc = label_define.sub("", doc)
    doc = label_ref.sub("``\\3`` (in the PARI manual)", doc)

    # Bullet items
    doc = doc.replace("@3@[startbold]*@[endbold] ", "@BULLET  ")
    doc = sub_loop(bullet_loop, "\\1  \\3", doc)
    doc = doc.replace("@BULLET  ", "- ")

    # Add =VOID= in front of all leading whitespace (which was
    # intentionally added) to avoid confusion with verbatim blocks.
    doc = leading_ws.sub(r"=VOID=\1", doc)

    # Verbatim blocks
    doc = begin_verb.sub("::\n\n@0", doc)
    doc = end_verb.sub("", doc)
    doc = doc.replace("@0", "    ")
    doc = doc.replace("@3", "")

    # Remove all further markup from within verbatim blocks
    doc = sub_loop(verb_loop, "\\1", doc)

    # Pair dollars -> beginmath/endmath
    doc = doc.replace("@[dollar]@[dollar]", "@[doubledollar]")
    doc = dollars.sub(r"@[startMATH]\1@[endMATH]", doc)
    doc = doubledollars.sub(r"@[startDISPLAYMATH]\1@[endDISPLAYMATH]", doc)

    # Replace special characters (except in verbatim blocks)
    # \ -> =BACKSLASH=
    # | -> =MID=
    # % -> =PERCENT=
    # # -> =HASH=
    doc = sub_loop(escape_backslash, "\\1=BACKSLASH=", doc)
    doc = sub_loop(escape_mid, "\\1=MID=", doc)
    doc = sub_loop(escape_percent, "\\1=PERCENT=", doc)
    doc = sub_loop(escape_hash, "\\1=HASH=", doc)

    # Math markup
    doc = doc.replace("@[obr]", "{")
    doc = doc.replace("@[cbr]", "}")
    doc = doc.replace("@[startword]", "\\")
    doc = doc.replace("@[endword]", "")
    # (special rules for Hom and Frob, see trac ticket 21005)
    doc = doc.replace("@[startlword]Hom@[endlword]", "\\text{Hom}")
    doc = doc.replace("@[startlword]Frob@[endlword]", "\\text{Frob}")
    doc = doc.replace("@[startlword]", "\\")
    doc = doc.replace("@[endlword]", "")
    doc = doc.replace("@[startbi]", "\\mathbb{")
    doc = doc.replace("@[endbi]", "}")

    # PARI TeX macros
    doc = doc.replace(r"\Cl", r"\mathrm{Cl}")
    doc = doc.replace(r"\Id", r"\mathrm{Id}")
    doc = doc.replace(r"\Norm", r"\mathrm{Norm}")
    doc = doc.replace(r"\disc", r"\mathrm{disc}")
    doc = doc.replace(r"\gcd", r"\mathrm{gcd}")
    doc = doc.replace(r"\lcm", r"\mathrm{lcm}")

    # Remove extra markup inside math blocks
    doc = sub_loop(math_loop, "\\1", doc)

    # Replace special characters by escape sequences
    # Note that =BACKSLASH= becomes an unescaped backslash in math mode
    # but an escaped backslash otherwise.
    doc = sub_loop(math_backslash, r"\1\\", doc)
    doc = doc.replace("=BACKSLASH=", r"\\")
    doc = doc.replace("=MID=", r"\|")
    doc = doc.replace("=PERCENT=", r"\%")
    doc = doc.replace("=HASH=", r"\#")
    doc = doc.replace("=VOID=", "")

    # Handle DISPLAYMATH
    doc = doc.replace("@[endDISPLAYMATH]", "\n\n")
    doc = sub_loop(indent_math, "\\1    \\3", doc)
    doc = doc.replace("@[startDISPLAYMATH]", "\n\n.. MATH::\n\n    ")

    # Inline markup. We do use the more verbose :foo:`text` style since
    # those nest more easily.
    doc = doc.replace("@[startMATH]", ":math:`")
    doc = doc.replace("@[endMATH]", "`")
    doc = doc.replace("@[startpodcode]", "``")
    doc = doc.replace("@[endpodcode]", "``")
    doc = doc.replace("@[startcode]", ":literal:`")
    doc = doc.replace("@[endcode]", "`")
    doc = doc.replace("@[startit]", ":emphasis:`")
    doc = doc.replace("@[endit]", "`")
    doc = doc.replace("@[startbold]", ":strong:`")
    doc = doc.replace("@[endbold]", "`")

    # Remove prototype
    doc = prototype.sub("", doc)

    # Remove everything starting with "The library syntax is"
    # (this is not relevant for Python)
    doc = library_syntax.sub("", doc)

    # Allow at most 2 consecutive newlines
    doc = newlines.sub("\n\n", doc)

    # Strip result
    doc = doc.strip()

    # Ensure no more @ remains
    try:
        i = doc.index("@")
    except ValueError:
        return doc
    ilow = max(0, i-30)
    ihigh = min(len(doc), i+30)
    raise SyntaxError("@ found: " + doc[ilow:ihigh])


def get_raw_doc(function):
    r"""
    Get the raw documentation of PARI function ``function``.

    INPUT:

    - ``function`` -- name of a PARI function

    EXAMPLES::

        >>> from autogen.doc import get_raw_doc
        >>> print(get_raw_doc("cos").decode())
        @[startbold]cos@[dollar](x)@[dollar]:@[endbold]
        <BLANKLINE>
        @[label se:cos]
        Cosine of @[dollar]x@[dollar].
        ...
        >>> get_raw_doc("abcde")
        Traceback (most recent call last):
        ...
        RuntimeError: no help found for 'abcde'
    """
    doc = subprocess.check_output(["gphelp", "-raw", function])
    if doc.endswith(b"""' not found !\n"""):
        raise RuntimeError("no help found for '{}'".format(function))
    return doc


def get_rest_doc(function):
    r"""
    Get the documentation of the PARI function ``function`` in reST
    syntax.

    INPUT:

    - ``function`` -- name of a PARI function

    EXAMPLES::

        >>> from autogen.doc import get_rest_doc
        >>> print(get_rest_doc("teichmuller"))
        Teichmüller character of the :math:`p`-adic number :math:`x`, i.e. the unique
        :math:`(p-1)`-th root of unity congruent to :math:`x / p^{v_...(x)}` modulo :math:`p`...

    ::

        >>> print(get_rest_doc("weber"))
        One of Weber's three :math:`f` functions.
        If :math:`flag = 0`, returns
        <BLANKLINE>
        .. MATH::
        <BLANKLINE>
            f(x) = \exp (-i\pi/24).\eta ((x+1)/2)/\eta (x) {such that}
            j = (f^{24}-16)^.../f^{24},
        <BLANKLINE>
        where :math:`j` is the elliptic :math:`j`-invariant (see the function :literal:`ellj`).
        If :math:`flag = 1`, returns
        <BLANKLINE>
        .. MATH::
        <BLANKLINE>
            f_...(x) = \eta (x/2)/\eta (x) {such that}
            j = (f_...^{24}+16)^.../f_...^{24}.
        <BLANKLINE>
        Finally, if :math:`flag = 2`, returns
        <BLANKLINE>
        .. MATH::
        <BLANKLINE>
            f_...(x) = \sqrt{2}\eta (2x)/\eta (x) {such that}
            j = (f_...^{24}+16)^.../f_...^{24}.
        <BLANKLINE>
        Note the identities :math:`f^... = f_...^...+f_...^...` and :math:`ff_...f_... = \sqrt2`.


    ::

        >>> doc = get_rest_doc("ellap")  # doc depends on PARI version

    ::

        >>> print(get_rest_doc("bitor"))
        bitwise (inclusive)
        :literal:`or` of two integers :math:`x` and :math:`y`, that is the integer 
        <BLANKLINE>
        .. MATH::
        <BLANKLINE>
            \sum
            (x_... or y_...) 2^...
        <BLANKLINE>
        See ``bitand`` (in the PARI manual) for the behavior for negative arguments.
    """
    raw = get_raw_doc(function)
    return raw_to_rest(raw)
