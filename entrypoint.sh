#!/bin/bash

set -euxo pipefail

emacs --version

readonly ROOTDIR="/root/website"
readonly CASK="/root/.cask/bin/"
export PATH="$PATH:$CASK"

cask install
/root/.cask/bin/cask emacs --batch -l bootstrap-build.el -f "build-website"

### Diagnostics
stat build/
echo "Github workspace is: ${GITHUB_WORKSPACE}"
stat "${GITHUB_WORKSPACE}"
cp -r build/ "${GITHUB_WORKSPACE}"

