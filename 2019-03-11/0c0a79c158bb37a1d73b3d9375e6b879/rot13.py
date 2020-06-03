import string
from codecs import encode as _dont_use_this_

def rot13(message):
    return "".join(chr(((ord(c) - ord('a') + 13) % 26) + ord('a')) if ord(c) in range(ord('a'), ord('z')+1) else chr(((ord(c) - ord('A') + 13) % 26) + ord('A')) if ord(c) in range(ord('A'), ord('Z')+1) else c for c in message)