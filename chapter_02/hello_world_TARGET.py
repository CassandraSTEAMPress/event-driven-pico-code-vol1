import os, sys

def say_hello(name="world"):
    '''Print info about the system and greeting'''
    mySoftwareVersion = "1.0"
    myPlatform = os.uname()
    mySys = sys.implementation

    print(f'SoftwareVersion = {mySoftwareVersion}')
    print(f'myPlatform: {myPlatform}')
    print(f'mySys: {mySys}')
    print(f'Hello, {name}!\n')
