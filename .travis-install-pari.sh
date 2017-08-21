# Helper script to install PARI for Travis CI

# Exit on error
set -e

# Figure out PARI version and download location
# Note that we support giving a list of URLs
if [ "$PARI_VERSION" = snapshot ]; then
    PARI_VERSION=$(wget -qO- "http://pari.math.u-bordeaux.fr/pub/pari/snapshots" | sed -n 's/.*href="\(pari-.*-g.*\)[.]tar[.]gz".*/\1/p')
    URL="http://pari.math.u-bordeaux.fr/pub/pari/snapshots"
else
    URL="http://pari.math.u-bordeaux.fr/pub/pari/unix http://pari.math.u-bordeaux.fr/pub/pari/unstable"
fi

# Download PARI sources
for url in $URL; do
    if wget --no-verbose "$url/$PARI_VERSION.tar.gz"; then
        # Success
        break
    fi
done

# Install
tar xzf "$PARI_VERSION.tar.gz"
cd "$PARI_VERSION"
./Configure --prefix=/usr
make gp
sudo make install
