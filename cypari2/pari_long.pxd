# On 64-bit Windows, the PARI library’s header file parigen.h includes the
# following preprocessor definition:
#   #define long long long
# Since the long type in Windows compilers remains 32 bits wide 
# (unlike on many Unix-like systems where it is 64 bits), this macro substitution
# creates problems.  We work around this by defining our own types
# pari_longword and pari_ulongword, which are guaranteed to be 64 bits wide.

IF UNAME_SYSNAME == "Windows":
    ctypedef long long pari_longword
    ctypedef unsigned long long pari_ulongword
ELSE:
    ctypedef long pari_longword
    ctypedef unsigned long pari_ulongword
