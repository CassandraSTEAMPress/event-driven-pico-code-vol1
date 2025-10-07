''' Quickly check hello_world, palindrome, \
    and convert_temperature modules '''

# hello_world 
from hello_world_HOST import say_hello
say_hello()
say_hello("again")
say_hello("Young Rustwalker")

# palindrome 
from palindrome import is_palindrome
is_palindrome("Was it a car or a cat I saw?")
is_palindrome("A man, a plan, a canal, Panama!")
is_palindrome("Are we not drawn onward, "
              "drawn onward to new era?")

is_palindrome("rotated")
is_palindrome("Mr. Robin ate my metal worm.")
is_palindrome("Anne, I vote more cars race Rome to Paris.")

# convert_temperature 
from convert_temperature import CtoF, FtoC
print(f"\nCtoF(0.0) = {CtoF(0.0)}")
print(f"CtoF(100.0) = {CtoF(100.0)}")
print(f"\nFtoC(32.0) = {FtoC(32.0)}")
print(f"FtoC(212.0) = {FtoC(212.0)}")
