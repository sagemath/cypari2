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

# CI builds can use an isolated PARI, independent of Homebrew's PARI
# version and of any libraries already installed on the runner.
if [ -n "${PARI_PREFIX:-}" ]; then
    if [ "$PLATFORM" != linux ] && [ "$PLATFORM" != macos ]; then
        echo "PARI_PREFIX is supported only on Linux and macOS" >&2
        exit 1
    fi
    PARI_VERSION=${PARI_VERSION:-2.19.1}
    if [ "$PARI_VERSION" != 2.19.1 ]; then
        echo "No verified source checksum for PARI $PARI_VERSION" >&2
        exit 1
    fi
    PARI_SHA256=419553b11ff8c3ecb8e9031b7d91d7cee003a5d721e685fcb499565c96fe2943
    case "$PARI_PREFIX" in
        /*) ;;
        *) echo "PARI_PREFIX must be an absolute path" >&2; exit 1 ;;
    esac
    if [ -e "$PARI_PREFIX" ]; then
        echo "PARI_PREFIX must be a new directory: $PARI_PREFIX" >&2
        exit 1
    fi
    prefix_parent=$(dirname "$PARI_PREFIX")
    available_kib=$(df -Pk "$prefix_parent" | awk 'END {print $4}')
    if [ "$available_kib" -lt 8388608 ]; then
        echo "PARI build requires at least 8 GiB free in $prefix_parent; available: $available_kib KiB" >&2
        exit 1
    fi

    elevate=()
    if [ "$(id -u)" != 0 ]; then
        elevate=(sudo)
    fi
    gmp_args=()
    if [ "$PLATFORM" = macos ]; then
        if ! brew list --versions gmp >/dev/null; then
            if [ "${PARI_INSTALL_DEPENDENCIES:-0}" != 1 ]; then
                echo "GMP must already be installed; dependency installation is disabled" >&2
                exit 1
            fi
            brew install gmp
        fi
        gmp_args=("--with-gmp=$(brew --prefix gmp)")
        SDKROOT=${SDKROOT:-$(xcrun --sdk macosx --show-sdk-path)}
        export SDKROOT
        # Retain Homebrew's workaround for the macOS Clang miscompilation.
        # https://pari.math.u-bordeaux.fr/cgi-bin/bugreport.cgi?bug=2608
        CFLAGS="${CFLAGS:+$CFLAGS }-O1"
        export CFLAGS
        jobs=$(sysctl -n hw.logicalcpu)
    else
        # manylinux/musllinux containers and hosted Ubuntu use different tools.
        if ! printf '#include <gmp.h>\n' | "${CC:-cc}" -E - >/dev/null 2>&1; then
            if [ "${PARI_INSTALL_DEPENDENCIES:-0}" != 1 ]; then
                echo "GMP headers must already be installed; dependency installation is disabled" >&2
                exit 1
            fi
            if command -v dnf >/dev/null; then
                "${elevate[@]}" dnf install -y gmp-devel
            elif command -v yum >/dev/null; then
                "${elevate[@]}" yum install -y gmp-devel
            elif command -v apk >/dev/null; then
                "${elevate[@]}" apk add gmp-dev
            else
                "${elevate[@]}" apt-get update
                "${elevate[@]}" apt-get install -y libgmp-dev
            fi
        fi
        jobs=$(getconf _NPROCESSORS_ONLN)
    fi
    build_root=$(mktemp -d "$prefix_parent/pari-build.XXXXXX")
    echo "Building verified PARI $PARI_VERSION in $build_root for $PARI_PREFIX"
    cd "$build_root"
    curl --fail --location --retry 3 \
        "https://pari.math.u-bordeaux.fr/pub/pari/unix/pari-$PARI_VERSION.tar.gz" \
        --output pari.tar.gz
    if [ "$PLATFORM" = macos ]; then
        printf '%s  pari.tar.gz\n' "$PARI_SHA256" | shasum -a 256 --check
    else
        printf '%s  pari.tar.gz\n' "$PARI_SHA256" | sha256sum -c
    fi
    tar xzf pari.tar.gz
    cd "pari-$PARI_VERSION"
    ./Configure "--prefix=$PARI_PREFIX" --mt=pthread --without-readline "${gmp_args[@]}"
    make -j"$jobs" gp
    make install
    "$PARI_PREFIX/bin/gp" --version
    # A stack resize in a startup file must not corrupt later input/history.
    printf 'default(parisize,16000000);\n' > "$build_root/startup-check.gp"
    gp_output=$(printf '1+2\n%%\nquit\n' | "$PARI_PREFIX/bin/gp" -f -q -s 8000000 \
        "$build_root/startup-check.gp" 2> "$build_root/startup-check.stderr")
    if [ "$gp_output" != $'3\n3' ]; then
        printf 'PARI startup/history regression: expected 3 twice; got:\n%s\n' "$gp_output" >&2
        cat "$build_root/startup-check.stderr" >&2
        exit 1
    fi
    echo "PARI startup/history regression passed"
    exit 0
fi

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
    PARI_VERSION=2.17.4
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

# Install gmp if not present
if ! ldconfig -p | grep libgmp >/dev/null 2>&1; then
    echo "Installing GMP ..."
    if [ "$PLATFORM" = "msys" ]; then
        pacman -S --noconfirm mingw-w64-ucrt-x86_64-gmp
        MSYSTEM_PREFIX="/ucrt64"
    elif [ "$PLATFORM" = "linux" ]; then
        if command -v dnf >/dev/null 2>&1; then
            dnf install -y gmp-devel
        fi
    elif [ "$PLATFORM" = "macos" ]; then
        brew install gmp
    elif [ "$PLATFORM" = "freebsd" ]; then
        pkg install -y gmp
    elif [ "$PLATFORM" = "openbsd" ]; then
        pkg_add gmp
    fi
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
        if command -v dnf >/dev/null 2>&1; then
            dnf install -y sudo
        elif command -v apt-get >/dev/null 2>&1; then
            apt-get update
            apt-get install -y sudo
        elif command -v apk >/dev/null 2>&1; then
            apk add sudo
        fi
    fi
    make gp
    sudo make install

    # Copy libpari to usr/lib64 (needed on RHEL/CentOS/Fedora)
    if [ -d /usr/lib64 ] && [ -f /usr/lib/libpari.so ]; then
        sudo cp /usr/lib/libpari.so* /usr/lib64/
        sudo ldconfig
    fi

    # Diagnostic output
    ls -l /usr/lib | grep libpari || true
    ls -L /usr/lib | grep libpari || true
    ls -l /usr/local/lib | grep libpari || true
    ldconfig -p | grep libpari || true
fi
