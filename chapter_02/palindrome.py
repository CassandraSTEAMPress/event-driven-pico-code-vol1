def is_palindrome(s):
    ''' Determine whether s is a palindrome or not '''
    r1="".join(list([c for c in s.upper() if c.isalpha()]))
    r2="".join(reversed(r1))
    print(f'PALINDROME: {s}') if r1 == r2 else print(\
                                 f'NOT a PALINDROME: {s}')