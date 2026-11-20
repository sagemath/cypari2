#!/usr/bin/env bash
# Select the core PARI keg without changing which Python the matrix uses.
set -euo pipefail

if ! command -v brew >/dev/null && [[ -x /home/linuxbrew/.linuxbrew/bin/brew ]]; then
    export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"
fi
expected_version=${PARI_VERSION:-2.19.1}
if [[ ${PARI_INSTALL_DEPENDENCIES:-1} == 1 ]]; then
    # Hosted images can disable automatic updates and ship an older core index.
    available=$(brew info --json=v2 homebrew/core/pari | jq -r '.formulae[0].versions.stable')
    if [[ $available != "$expected_version" ]]; then
        brew update
    fi
    brew install homebrew/core/pari
fi
pari_prefix=$(brew --prefix --installed homebrew/core/pari)
gmp_prefix=$(brew --prefix --installed homebrew/core/gmp)
# A tap can install a keg with the same name and version on a shared runner.
if ! jq -e '.source.tap == "homebrew/core"' "$pari_prefix/INSTALL_RECEIPT.json" >/dev/null; then
    echo "Expected a homebrew/core/pari keg at $pari_prefix" >&2
    exit 1
fi
version=$("$pari_prefix/bin/gp" --version-short)
if [[ $version != "$expected_version" ]]; then
    echo "Expected PARI $expected_version from Homebrew core, found $version in $pari_prefix" >&2
    exit 1
fi
# cibuildwheel also runs this hook outside GitHub Actions.
if [[ -z ${GITHUB_ENV:-} || -z ${GITHUB_PATH:-} ]]; then
    exit 0
fi
echo "$pari_prefix/bin" >> "$GITHUB_PATH"
{
    echo "PARI_PREFIX=$pari_prefix"
    echo "GMP_PREFIX=$gmp_prefix"
    echo "LDFLAGS=-Wl,-rpath,$pari_prefix/lib"
    echo "PKG_CONFIG_PATH=$gmp_prefix/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
    if [[ $(uname -s) == Darwin ]]; then
        echo "SDKROOT=$(xcrun --sdk macosx --show-sdk-path)"
    fi
} >> "$GITHUB_ENV"
