import time
from fibonacci_n import fibonacci_iterative, fibonacci_recursive

# Time iterative Fibonacci algorithm
print("\nElapsed times in ms for iterative Fibonacci algorithm:") 
for n in range(0, 36, 5): 
    start = time.ticks_ms()
    result = fibonacci_iterative(n)
    end = time.ticks_ms()
    elapsed_ms = end - start
    print(f'F_i({n}): {result} = {elapsed_ms} ms')

# Time recursive Fibonacci algorithm
print("\nElapsed times in ms for recursive Fibonacci algorithm:")
for n in range(0, 36, 5): 
    start = time.ticks_ms()
    result = fibonacci_recursive(n)
    end = time.ticks_ms()
    elapsed_ms = end - start
    print(f'F_r({n}): {result} = {elapsed_ms} ms')