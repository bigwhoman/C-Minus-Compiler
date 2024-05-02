#!/bin/bash
for test in testcases-phase2/T*; do
    echo "RUNNING TEST $test"
    cp "$test/input.txt" input.txt
    python3 compiler.py
    diff --strip-trailing-cr "$test/parse_tree.txt" parse_tree.txt
    diff --strip-trailing-cr "$test/syntax_errors.txt" syntax_errors.txt
    echo "=================="
done
rm input.txt parse_tree.txt syntax_errors.txt