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
# set -o xtrace

COVERAGE_MIN=100

main() {
  local filename

  for filename in cmdwrapper/*; do
    echo "pep257 $filename"
    pep257 "$filename"

    echo "flake8 $filename"
    flake8 "$filename"

    echo pylint "$filename"
    pylint "$filename"

    echo coverage run "$filename"
    coverage run "$filename"

    echo coverage report "$filename"
    if ! coverage report "--fail-under=$COVERAGE_MIN" "$filename"; then
      echo "ERROR: The coverage of $filename is less then ${COVERAGE_MIN}%"
      exit 1
    fi
  done

  echo
  echo "SUCCESS!"

  exit 0
}

# MAIN
main "$@"

# vim:ai:et:sw=2:ts=2:sts=2:tw=0:fenc=utf-8
