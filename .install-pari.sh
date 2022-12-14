# Helper script to install PARI for github workflows

# Exit on error
set -e

if [ "$URLDIR" = "" ]; then
    PURE_VERSION=${PARI_VERSION/pari-}
    URLDIR=OLD/${PURE_VERSION%.*}
fi

PARI_URL="http://pari.math.u-bordeaux.fr/pub/pari/$URLDIR"
PARI_URL1="http://pari.math.u-bordeaux.fr/pub/pari/unix"
PARI_URL2="http://pari.math.u-bordeaux.fr/pub/pari/unstable"

# Download PARI sources
wget --no-verbose "$PARI_URL/$PARI_VERSION.tar.gz" || wget --no-verbose "$PARI_URL1/$PARI_VERSION.tar.gz" || wget --no-verbose "$PARI_URL2/$PARI_VERSION.tar.gz" || wget --no-verbose "$PARI_URL3/$PARI_VERSION.tar.gz"

# Install
tar xzf "$PARI_VERSION.tar.gz"
cd "$PARI_VERSION"
./Configure --prefix=/usr
make gp
sudo make install
