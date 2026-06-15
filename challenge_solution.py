"""
CodeToAGI — Episode 26 Challenge Solution
Context Managers Challenge
"""

import time
import os
from contextlib import contextmanager, ExitStack


# ==================== STEP 1 & 2: Suppressor ====================

class Suppressor:
    """Class-based context manager that suppresses specified exceptions."""
    def __init__(self, *exc_types):
        self.exc_types = exc_types

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, self.exc_types):
            print(f"✅ Suppressed: {exc_type.__name__} - {exc_val}")
            return True  # Suppress the exception
        return False  # Let other exceptions propagate


@contextmanager
def suppressor(*exc_types):
    """Generator-based version using @contextmanager decorator."""
    try:
        yield
    except exc_types as e:
        print(f"✅ Suppressed (generator): {type(e).__name__} - {e}")
    else:
        pass  # No exception occurred


# ==================== STEP 3: Timer Context Manager ====================

@contextmanager
def timer(label=""):
    """Context manager that times a block of code."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"⏱  {label} completed in {elapsed:.4f} seconds")


# ==================== STEP 4 & 5: Combined Usage ====================

def main():
    print("=== CodeToAGI EP26 Challenge Solution ===\n")

    # Step 3: Timer example
    with timer("Sum 1 Million Numbers"):
        total = sum(range(1_000_000))
        print(f"Sum = {total:,}")

    print("\n" + "="*50 + "\n")

    # Step 4: ExitStack with multiple files
    filenames = ["file1.txt", "file2.txt", "file3.txt"]

    # Create sample files
    for name in filenames:
        with open(name, "w") as f:
            f.write(f"Content of {name}\n")

    with ExitStack() as stack:
        files = [stack.enter_context(open(name)) for name in filenames]
        print(f"✅ Successfully opened {len(files)} files using ExitStack:")
        for f in files:
            print(f"   - {f.name} is open")

    print("\n" + "="*50 + "\n")

    # Step 5: Combine Timer + Suppressor
    print("Testing combined Timer + Suppressor:")
    try:
        with timer("Dangerous Operation"), Suppressor(ValueError, ZeroDivisionError):
            print("Inside combined context manager...")
            # Deliberately raise an exception
            x = 1 / 0
    except Exception as e:
        print(f"Exception propagated outside: {type(e).__name__}")

    # Cleanup sample files
    for name in filenames:
        if os.path.exists(name):
            os.remove(name)

    print("\n🎉 Challenge Complete! All context managers worked as expected.")


if __name__ == "__main__":
    main()
