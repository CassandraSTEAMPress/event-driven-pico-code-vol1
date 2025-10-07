# my_uuid4.py - Generate a random UUID compliant to IETF RFC 4122
#
# See: https://datatracker.ietf.org/doc/html/rfc4122
#      https://datatracker.ietf.org/doc/html/rfc9562
#      https://docs.python.org/3/library/uuid.html
# ---------------------------------------------------------------

import os
import uuid

def my_uuid4():
    # Get 16 high-quality, cryptographically secure random bytes
    random_x = bytearray(os.urandom(16))

    # Set the "version" and "variant" bits per RFC 4122
    random_x[6] = (random_x[6] & 0x0F) | 0x40
    random_x[8] = (random_x[8] & 0x3F) | 0x80

    # Generate a 32-character hexadecimal string
    h = random_x.hex()

    # Return the string formatted as a UUID string with hyphens
    return str('-'.join((h[0:8], h[8:12], \
                         h[12:16], h[16:20], h[20:32])))

def is_rfc4122_UUID(test_string):
    # Try creating a valid UUID object from the string;
    #   raise ValueError if the format is invalid
    try:
        parsed_string = uuid.UUID(test_string)
        if parsed_string.variant == uuid.RFC_4122 and \
           parsed_string.version == 4:
            return True
        # The string is not in a valid UUID format
        else:  
            return False
    # The string is not a UUID
    except ValueError:
        return False
  
if __name__ == '__main__':
    for _ in range(5):
        x = my_uuid4()
        print(f"RFC version 4, 4122 compliant? " \
              f"{is_rfc4122_UUID(x)}: '{x}'")

    not_UUID = "not-a-good-uuid-string"
    print(f"\nnot_UUID = '{not_UUID}'")
    print(f"RFC version 4, 4122 compliant? " \
          f"{is_rfc4122_UUID(not_UUID)}")
    
    nil_UUID = "00000000-0000-0000-0000-000000000000"
    print(f"\nnil_UUID = '{nil_UUID}'")
    print(f"RFC version 4, 4122 compliant? " \
          f"{is_rfc4122_UUID(nil_UUID)}")
 
    omni_UUID = "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"
    print(f"\nomni_UUID = '{omni_UUID}'")
    print(f"RFC version 4, 4122 compliant? " \
          f"{is_rfc4122_UUID(omni_UUID)}")