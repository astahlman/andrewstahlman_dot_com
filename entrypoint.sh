#!/bin/bash

set -euxo pipefail

emacs --version

readonly ROOTDIR="/root/website"
readonly CASK="/root/.cask/bin/"
export PATH="$PATH:$CASK"

cask install
/root/.cask/bin/cask emacs --batch -l bootstrap-build.el -f "website/build"
