#!/bin/bash

# Helper script to install PARI (e.g. for CI builds).
# On macOS: the default system gcc is used
# On Linux: the default system gcc is used
# On Windows: uses the ucrt64 toolchain in Msys2

# Exit on error
set -e

# Run the script again in UCRT64 system for msys
if [ "$ucrt" != "0" ] && [[ "$(uname -s)" == MSYS_NT* ]]; then
    MSYSTEM=UCRT64 MSYS2_PATH_TYPE=inherit bash --login -c "cd $pwd ; $self"
fi

# Windows conda prefix is not added to path automatically
# thus mingw compiler is not found later
if [ -n "$CONDA_PREFIX" ]; then
    export PATH="$(cygpath "$CONDA_PREFIX")/Library/bin:$PATH"
fi

if [ "$PARI_VERSION" = "" ]; then
    PARI_VERSION=2.17.2
fi

PURE_VERSION=${PARI_VERSION/pari-}
URLDIR=OLD/${PURE_VERSION%.*}

PARI_URL="https://pari.math.u-bordeaux.fr/pub/pari/$URLDIR"
PARI_URL1="https://pari.math.u-bordeaux.fr/pub/pari/unix"
PARI_URL2="https://pari.math.u-bordeaux.fr/pub/pari/unstable"

if [ -d build/pari-$PURE_VERSION ] ; then
    echo "Using existing pari-$PURE_VERSION build directory"
    cd "build/pari-$PURE_VERSION"
else
    echo "Download PARI sources"
    if [ ! -d build ] ; then
        mkdir build
    fi
    cd build
    wget --no-verbose "$PARI_URL/$PARI_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz" || wget --no-verbose "$PARI_URL1/pari-$PURE_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz" || wget --no-verbose "$PARI_URL2/pari-$PURE_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz"
    tar xzf "pari-$PURE_VERSION.tgz"
    cd "pari-$PURE_VERSION"
fi

echo "Building Pari ..."
if [ "$(uname -s)" = "Linux" ]; then
    ./Configure  --prefix=/usr
else
    ./Configure
fi

# On Windows, disable UNIX-specific code in language files
# (not sure why UNIX is defined)
lang_es="src/language/es.c"
if [ -f "$lang_es" ] && [[ "$(uname -s)" == MSYS_NT* ]]; then
    sed -i.bak \
        -e 's/#if[[:space:]]*defined(UNIX)/#if 0/' \
        -e 's/#ifdef[[:space:]]*UNIX/#if 0/' \
        "$lang_es"
fi


if [[ "$(uname -s)" == MSYS_NT* ]]; then
    # Windows
    sudo make install-lib-sta
    sudo make install-include
    sudo make install-doc
    sudo make install-cfg
    sudo make install-bin-sta
else
    # Linux or macOS
    make gp
    sudo make install
fi

exit 0
export DESTDIR=
if [ $(uname) = "Darwin" ] ; then
    rm -rf Odarwin*
    export CFLAGS="-arch x86_64 -arch arm64 -mmacosx-version-min=10.9"
# For debugging:
#   export CFLAGS="-g -arch x86_64 -arch arm64 -mmacosx-version-min=10.9"
    ./Configure --host=universal-darwin --prefix=${PARIPREFIX} --with-gmp=${GMPPREFIX}
    cd Odarwin-universal
    make install
    make install-lib-sta
    make clean
elif [ `python -c "import sys; print(sys.platform)"` = 'win32' ] ; then
#Windows
    export PATH=/c/msys64/ucrt64/bin:$PATH
    export MSYSTEM=UCRT64
    export CC=/c/msys64/ucrt64/bin/gcc
    # Disable avx and sse2.
    export CFLAGS="-U HAS_AVX -U HAS_AVX512 -U HAS_SSE2"
    ./Configure --prefix=${PARIPREFIX} --libdir=${PARILIBDIR} --without-readline --with-gmp=${GMPPREFIX}
    cd Omingw-*
    make install-lib-sta
    make install-include
    make install-doc
    make install-cfg
    make install-bin-sta
else
# linux
    ./Configure --prefix=${PARIPREFIX} --libdir=${PARILIBDIR} --with-gmp=${GMPPREFIX}
    make install
    make install-lib-sta
fi
