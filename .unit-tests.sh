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

run_unit_tests() {
  local filename="$1"

  # run the unit-tests first
  python3 "$filename"

  test_with pep257 "$filename"
  test_with flake8 "$filename"
  test_with pylint "$filename"

  test_with coverage run "$filename"
  test_with coverage html "$filename"

  if ! test_with coverage report "--fail-under=$COVERAGE_MIN" "$filename"; then
    echo "ERROR: The coverage of $filename is less then ${COVERAGE_MIN}%"
    exit 1
  fi
}

main() {
  local filename

  if ! [[ -f cmdwrapper/cmdwrapper.py ]]; then
    echo "ERROR: the directory $(pwd) where you started the script $0 is invalid." >&2
    exit 1
  fi

  # clean-up
  rm -fr .coverage htmlcov

  if [[ "$#" -gt 0 ]]; then
    run_unit_tests "$1"
  else
    for filename in cmdwrapper/*; do
      run_unit_tests "$filename"
    done
  fi

  echo
  echo "SUCCESS!"

  exit 0
}

# MAIN
main "$@"

# vim:ai:et:sw=2:ts=2:sts=2:tw=0:fenc=utf-8
