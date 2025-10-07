import time
from fibonacci_n import fibonacci_iterative, fibonacci_recursive

# Time iterative Fibonacci algorithm
print("\nElapsed times in ms for iterative Fibonacci algorithm:") 
for n in range(0, 36, 5): 
    start = time.perf_counter()
    result = fibonacci_iterative(n)
    end = time.perf_counter()
    elapsed_ms = (end - start) * 1000  # convert to milliseconds
    print(f'F_i({n}): {result} = {elapsed_ms:.5f} ms')

# Time recursive Fibonacci algorithm
print("\nElapsed times in ms for recursive Fibonacci algorithm:") 
for n in range(0, 36, 5): 
    start = time.perf_counter()
    result = fibonacci_recursive(n)
    end = time.perf_counter()
    elapsed_ms = (end - start) * 1000  # convert to milliseconds
    print(f'F_r({n}): {result} = {elapsed_ms:.5f} ms')