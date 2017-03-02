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

test_with() {
  local exit_code=0
  echo "+ $*"
  "$@" || exit_code="$?"

  if [[ "$exit_code" -ne 0 ]]; then
    echo "ERROR: $*" >&2
  fi

  return "$exit_code"
}

main() {
  local filename

  for filename in cmdwrapper/*; do
    test_with pep257 "$filename"
    test_with flake8 "$filename"
    test_with pylint "$filename"

    continue

    test_with coverage run "$filename"

    if ! test_with coverage report "--fail-under=$COVERAGE_MIN" "$filename"; then
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
