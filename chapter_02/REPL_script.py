''' Quick sanity check Python script '''

# Hello, world!
print("Hello, world!")
s1="Hello";s2=", again!"; print(s1+s2)

# Tuple
xTuple =('a','b','c')+('d','e','f')
print(f'\nxTuple = {xTuple}')

# List
yList  =[1,2,3]+[4,5,6]
print(f'\nyList = {yList}')

# Dictionary
D = {'0':0, 'a':1, 'b':2, 'c':3}  
D['b'] = 52
D['d'] = 4  
print(f"""\nDictionary: 
      D = {D},
      len(D) = {len(D)},
      D.keys() = {D.keys()},
      D.values() = {D.values()}
      """)

# Palindrome
test_string='Are we not drawn onward, drawn onward to new era?'
input_string = "".join(c.upper() for c in test_string \
                       if c.isalpha())
reversed_string = ''.join(reversed(input_string))
if input_string == reversed_string: 
    print(f'PALINDROME: {test_string}')
else:
    print(f'NOT a PALINDROME: {test_string}')

# Temperature Conversion
tempCelsius = 100.0
print(f"\nFahrenheit: {(9.0/5.0 * tempCelsius) + 32.0}")
