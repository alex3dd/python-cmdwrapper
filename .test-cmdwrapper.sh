#!/usr/bin/env bash
#
# test cmdwrapper
#
# Author: Achraf Cherti (aka Asher256) <asher256@gmail.com>
# Website: http://www.asher256.com/
# License: LGPL2.1
#
# This source code follows the Google style guide for shell scripts:
# https://google.github.io/styleguide/shell.xml
#

set -o errexit
set -o nounset
set -o xtrace

main() {
  local filename

  for filename in cmdwrapper/*; do
    pep257 "$filename"
    flake8 "$filename"
    pylint "$filename"
    coverage report --fail-under=100 "$filename"
  done

  exit 0
}

# MAIN
main "$@"

# vim:ai:et:sw=2:ts=2:sts=2:tw=0:fenc=utf-8
