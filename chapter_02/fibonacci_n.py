# Iteratively find the nth in the Fibonacci Sequence 
def fibonacci_iterative(n): 
    ''' '''
    a, b = 0, 1
    for i in range(n):
        a, b = b, a+b
    return a

# Recursively find the nth in the Fibonacci Sequence 
def fibonacci_recursive(n):
    if n in {0, 1}:  # Base case halting the recursion
        return n
    return fibonacci_recursive(n - 1) \
           + fibonacci_recursive(n - 2)