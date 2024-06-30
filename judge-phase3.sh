#!/bin/bash
for test in testcases-phase3/T*; do
    rm input.txt expected.txt semantic_errors.txt stdout.txt output.txt
    echo "RUNNING TEST $test"
    cp "$test/input.txt" input.txt
    python3 compiler.py > /dev/null
    if [ "The input program is semantically correct." == "$(cat semantic_errors.txt | xargs)" ]; then
        echo "Running tester..."
        ./tester_linux.out > stdout.txt 2> /dev/null
    fi
    sed -i '$ d' stdout.txt # remove bytes used
    diff --strip-trailing-cr <(sed -e '$a\' "$test/expected.txt") <(sed -e '$a\' stdout.txt)
    stdout_exit_code=$?
    diff --strip-trailing-cr <(sed -e '$a\' "$test/semantic_errors.txt") <(sed -e '$a\' semantic_errors.txt)
    semantic_error_exit_code=$?
    echo "=================="
    if [[ $stdout_exit_code -ne 0 || $semantic_error_exit_code -ne 0 ]]; then
        echo "HALTING ON TEST $test: $stdout_exit_code $semantic_error_exit_code"
        exit
    fi
    echo "TEST $test DONE"
done
rm input.txt expected.txt semantic_errors.txt stdout.txt output.txt