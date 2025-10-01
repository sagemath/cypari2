#!/bin/bash

# Helper script to install PARI (e.g. for CI builds).
# On macOS: the default system fake gcc (clang) is used
# On Linux: the default system gcc is used
# On Windows: uses the ucrt64 toolchain in Msys2
# On *BSD: should be clang; also make should be gmake

# Exit on error
set -e

# Detect platform
PLATFORM="unknown"
case "$(uname -s)" in
    MSYS_NT*|MINGW*)
        PLATFORM="msys"
        ;;
    Linux)
        PLATFORM="linux"
        ;;
    Darwin)
        PLATFORM="macos"
        ;;
    FreeBSD)
        PLATFORM="freebsd"
        ;;
    OpenBSD)
        PLATFORM="openbsd"
        ;;
    *)
        echo "Unknown platform"
        exit 1
        ;;
esac

# Run the script again in UCRT64 system for msys
if [ "$ucrt" != "0" ] && [ "$PLATFORM" = "msys" ]; then
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
    
    # install wget if not present
    if ! command -v wget &> /dev/null
    then
        if [ "$PLATFORM" = "msys" ]; then
            pacman -S --noconfirm mingw-w64-ucrt-x86_64-wget
        elif [ "$PLATFORM" = "linux" ]; then
            dnf install -y wget
        elif [ "$PLATFORM" = "macos" ]; then
            brew install wget
        fi
    fi

    wget --no-verbose "$PARI_URL/$PURE_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz" \
        || wget --no-verbose "$PARI_URL1/pari-$PURE_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz" \
        || wget --no-verbose "$PARI_URL2/pari-$PURE_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz" \
        || wget --no-verbose "$PARI_URL/pari-$PURE_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz"
    tar xzf "pari-$PURE_VERSION.tgz"
    cd "pari-$PURE_VERSION"
fi

echo "Building Pari ..."
if [ "$PLATFORM" = "msys" ]; then
    # Remove "export_file='$(LIBPARI).def';" line from config/Makefile.SH"
    # Otherwise we get a Segmentation Fault during the resulting dlltool call
    sed -i.bak "/export_file='\\\$(LIBPARI).def';/d" config/Makefile.SH
fi
# For debugging:
# export CFLAGS="-g"
if [[ "$PLATFORM" = "msys" ]]; then
  # If one installs in a non-default location, then one needs to call os.add_dll_directory
  # in Python to find the DLLs.
  CONFIG_ARGS="--without-readline --prefix=$MSYSTEM_PREFIX"
else
  CONFIG_ARGS="--prefix=/usr"
fi
chmod -R +x ./Configure ./config
./Configure $CONFIG_ARGS

# On Windows, disable UNIX-specific code in language files
# (not sure why UNIX is defined)
lang_es="src/language/es.c"
if [ -f "$lang_es" ] && [ "$PLATFORM" = "msys" ]; then
    sed -i.bak \
        -e 's/#if[[:space:]]*defined(UNIX)/#if 0/' \
        -e 's/#ifdef[[:space:]]*UNIX/#if 0/' \
        "$lang_es"
fi


if [ "$PLATFORM" = "msys" ]; then
    # Windows
    cd Omingw-x86_64
    make install-lib-dyn
    make install-include
    make install-doc
    make install-cfg

    # Fix location of libpari.dll.a
    if [ -f "$MSYSTEM_PREFIX/bin/libpari.dll.a" ]; then
        cp "$MSYSTEM_PREFIX/bin/libpari.dll.a" "$MSYSTEM_PREFIX/lib/"
    fi
else
    # Linux or macOS
    
    # Remove sudo provided by devtoolset since it doesn't work
    rm -f /opt/rh/gcc-toolset-14/root/usr/bin/sudo
    if ! command -v sudo >/dev/null 2>&1; then
        dnf install sudo
    fi
    make gp
    sudo make install
fi
