#!/bin/bash

if1=$(mktemp) || exit 1
if2=$(mktemp) || exit 1
of=$(mktemp) || exit 1
args='-k1 -k2 -k4 -k8 -k16 -k32 -k64 -d:'

python3 tests/gentest.py -n1000 -m100 $args $if1 $if2 $of || exit 1

# diff <(sort $of) <(python3 src/kvdiff/kvdiff.py -l $args $if1 $if2 | sort) || (echo TEST FAILED; exit 1)
diff <(sort $of) <(kvdiff -l $args $if1 $if2 | sort) || (echo TEST FAILED; exit 1)
echo TEST PASSED
