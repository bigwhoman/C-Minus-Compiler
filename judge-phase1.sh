#!/bin/bash
for test in testcases-phase1/T*; do
    echo "RUNNING TEST $test"
    cp "$test/input.txt" input.txt
    python3 compiler.py
    diff --strip-trailing-cr "$test/lexical_errors.txt" lexical_errors.txt
    diff --strip-trailing-cr "$test/tokens.txt" tokens.txt
    echo "=================="
done
rm input.txt lexical_errors.txt tokens.txt symbol_table.txt