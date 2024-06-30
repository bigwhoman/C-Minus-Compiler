#!/bin/bash
for test in testcases-phase3/T*; do
    echo "RUNNING TEST $test"
    cp "$test/input.txt" input.txt
    python3 compiler.py #> /dev/null
    ./tester_linux.out > stdout.txt #2> /dev/null
    diff --strip-trailing-cr <(sed -e '$a\' "$test/expected.txt") <(sed -e '$a\' stdout.txt)
    sed -i '$ d' stdout.txt # remove bytes used
    stdout_exit_code=$?
    diff --strip-trailing-cr <(sed -e '$a\' "$test/semantic_errors.txt") <(sed -e '$a\' semantic_errors.txt)
    semantic_error_exit_code=$?
    echo "=================="
    if [[ $stdout_exit_code -ne 0 || $semantic_error_exit_code -ne 0 ]]; then
        echo "HALTING ON TEST $test: $stdout_exit_code $semantic_error_exit_code"
        exit
    fi
done
rm input.txt expected.txt semantic_errors.txt stdout.txt output.txt