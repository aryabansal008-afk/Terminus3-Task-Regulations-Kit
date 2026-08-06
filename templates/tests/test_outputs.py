"""
Terminus 3 verifier template (pytest-driven).
REGULATIONS.md §8.

Requirements for real tests here:
- Validate semantics, not superficial formatting (Strong Task Principle B).
- Cover every requirement stated in instruction.md.
- Cover edge cases.
- Must NOT be satisfiable by a hardcoded/special-cased solution
  (Strong Task Principle F: anti-hardcoding protections).
- Must NOT depend on any oracle-only artifact (no oracle leakage).
- Fully deterministic: no time.time(), no unseeded random, no network calls.
"""

import pytest


def test_placeholder():
    """Replace with real semantic assertions against /app (or wherever the
    task's artifacts live, per task.toml `artifacts`)."""
    raise NotImplementedError("Write real verifier tests before submission.")
