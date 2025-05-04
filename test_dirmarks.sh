#!/bin/bash

set -e

echo "[TEST] Cleaning up any old test marks..."
sed -i.bak '/^testmark:/d' ~/.markrc || true

TEST_DIR=$(pwd)

# Add a mark
echo "[TEST] Adding mark 'testmark' for $TEST_DIR"
dirmarks --add testmark "$TEST_DIR"

# List marks
echo "[TEST] Listing marks (should include 'testmark')"
dirmarks --list

# Get the mark
echo "[TEST] Getting mark 'testmark' (should print $TEST_DIR)"
dirmarks --get testmark

# Update the mark
echo "[TEST] Updating mark 'testmark' to /tmp"
dirmarks --update testmark /tmp

echo "[TEST] Getting mark 'testmark' (should print /tmp)"
dirmarks --get testmark

# Print the mark (simulate -p)
echo "[TEST] Printing mark 'testmark' (should print /tmp)"
dirmarks --get testmark

# Delete the mark
echo "[TEST] Deleting mark 'testmark'"
dirmarks --delete testmark

# List marks again
echo "[TEST] Listing marks (should NOT include 'testmark')"
dirmarks --list

# Test help
echo "[TEST] Printing help"
dirmarks --help

# Test shell function output
echo "[TEST] Printing shell function"
dirmarks --shell

echo "[TEST] All tests completed." 