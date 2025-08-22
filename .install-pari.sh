# Helper script to install PARI for github workflows

# Exit on error
set -e

if [ "$URLDIR" = "" ]; then
    PURE_VERSION=${PARI_VERSION/pari-}
    URLDIR=OLD/${PURE_VERSION%.*}
fi

PARI_URL="https://pari.math.u-bordeaux.fr/pub/pari/$URLDIR"
PARI_URL1="https://pari.math.u-bordeaux.fr/pub/pari/unix"
PARI_URL2="https://pari.math.u-bordeaux.fr/pub/pari/unstable"

# Download PARI sources
wget --no-verbose "$PARI_URL/$PARI_VERSION.tar.gz" -O pari.tgz || wget --no-verbose "$PARI_URL1/pari-$PARI_VERSION.tar.gz" -O pari.tgz || wget --no-verbose "$PARI_URL2/pari-$PARI_VERSION.tar.gz" -O pari.tgz

# Install
mkdir Pari42
tar xzf pari.tgz -C Pari42
cd Pari42/*
./Configure --prefix=/usr
make gp
sudo make install
