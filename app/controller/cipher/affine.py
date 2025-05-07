def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1,
            u2 - q * v2,
            u3 - q * v3,
            v1,
            v2,
            v3,
        )
    return u1 % m

def encrypt(plaintext, a, b):
    plaintext = ''.join(filter(str.isalpha, plaintext.upper()))
    ciphertext = ''
    for char in plaintext:
        x = ord(char) - ord('A')
        encrypted = (a * x + b) % 26
        ciphertext += chr(encrypted + ord('A'))
    return ciphertext

def decrypt(ciphertext, a, b):
    ciphertext = ciphertext.upper()
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise ValueError("a and 26 must be coprime.")
    plaintext = ''
    for char in ciphertext:
        y = ord(char) - ord('A')
        decrypted = (a_inv * (y - b)) % 26
        plaintext += chr(decrypted + ord('A'))
    return plaintext

# --- BYTE SUPPORT ---

def encrypt_bytes(data: bytes, a: int, b: int) -> bytes:
    """Encrypt raw bytes (0-255) using Affine cipher with mod 256."""
    encrypted = bytearray()
    for byte in data:
        encrypted.append((a * byte + b) % 256)
    return bytes(encrypted)

def decrypt_bytes(data: bytes, a: int, b: int) -> bytes:
    """Decrypt raw bytes (0-255) using Affine cipher with mod 256."""
    a_inv = mod_inverse(a, 256)
    if a_inv is None:
        raise ValueError("a and 256 must be coprime.")
    decrypted = bytearray()
    for byte in data:
        decrypted.append((a_inv * (byte - b)) % 256)
    return bytes(decrypted)
