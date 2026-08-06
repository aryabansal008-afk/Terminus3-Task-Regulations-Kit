#!/usr/bin/env bash
# Terminus 3 verifier entrypoint template
# REGULATIONS.md §8 — deterministic: no wall-clock dependence, no network
# dependence, no unseeded randomness.
set -euo pipefail

pytest -v /tests/test_outputs.py
