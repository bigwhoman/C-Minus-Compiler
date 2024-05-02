#!/bin/bash
for test in testcases-phase2/T*; do
    echo "RUNNING TEST $test"
    cp "$test/input.txt" input.txt
    python3 compiler.py
    diff --strip-trailing-cr <(sed -e '$a\' "$test/parse_tree.txt") <(sed -e '$a\' parse_tree.txt)
    parse_tree_exit_code=$?
    #diff --strip-trailing-cr <(sed -e '$a\' "$test/syntax_errors.txt") <(sed -e '$a\' syntax_errors.txt)
    snytax_error_exit_code=$?
    echo "=================="
    if [[ $parse_tree_exit_code -ne 0 || $snytax_error_exit_code -ne 0 ]]; then
        echo "HALTING ON TEST $test"
        exit
    fi
done
rm input.txt parse_tree.txt syntax_errors.txt