# Helper script to install PARI for github workflows

# Exit on error
set -e

if [ "$PARI_VERSION" = "" ]; then
    PARI_VERSION=2.17.2
fi

if [ "$URLDIR" = "" ]; then
    PURE_VERSION=${PARI_VERSION/pari-}
    URLDIR=OLD/${PURE_VERSION%.*}
fi

PARI_URL="https://pari.math.u-bordeaux.fr/pub/pari/$URLDIR"
PARI_URL1="https://pari.math.u-bordeaux.fr/pub/pari/unix"
PARI_URL2="https://pari.math.u-bordeaux.fr/pub/pari/unstable"

if [ -d build/pari-$PURE_VERSION ] ; then
    echo "Using existing pari-$PURE_VERSION build directory"
    cd "build/pari-$PURE_VERSION"
else
    echo "Download PARI sources"
    wget --no-verbose "$PARI_URL/$PARI_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz" || wget --no-verbose "$PARI_URL1/pari-$PARI_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz" || wget --no-verbose "$PARI_URL2/pari-$PARI_VERSION.tar.gz" -O "pari-$PURE_VERSION.tgz"
    if [ ! -d build ] ; then
        mkdir build
    fi
    tar xzf "pari-$PURE_VERSION.tgz" -C build
    cd "build/pari-$PURE_VERSION"
fi

echo "Building Pari ..."
./Configure --prefix=/usr
make gp
sudo make install
