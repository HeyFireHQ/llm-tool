test:
  just test-rust && just test-python

test-rust:
  cargo test

test-python:
  maturin develop && python3 tests/test.py
