def encrypt(data, key):
    """Encrypt binary or text data using extended Vigenère cipher"""
    if isinstance(data, str):
        data = data.encode('latin-1')
    key_bytes = key.encode('latin-1')
    encrypted_data = bytearray()
    for i, byte in enumerate(data):
        key_byte = key_bytes[i % len(key_bytes)]
        encrypted_data.append((byte + key_byte) % 256)
    return bytes(encrypted_data)

def decrypt(data, key):
    """Decrypt binary or text data using extended Vigenère cipher"""
    if isinstance(data, str):
        data = data.encode('latin-1')
    key_bytes = key.encode('latin-1')
    decrypted_data = bytearray()
    for i, byte in enumerate(data):
        key_byte = key_bytes[i % len(key_bytes)]
        decrypted_data.append((byte - key_byte) % 256)
    return bytes(decrypted_data)

def encrypt_text(text, key):
    """Encrypt plaintext and return a hex string (for display)"""
    encrypted = encrypt(text, key)
    return encrypted.hex(' ')

def decrypt_hex(hex_str, key):
    """Decrypt hex string (from UI) back to text"""
    hex_str = hex_str.replace(' ', '')
    encrypted_bytes = bytes.fromhex(hex_str)
    decrypted_bytes = decrypt(encrypted_bytes, key)
    return decrypted_bytes.decode('latin-1')

def encrypt_bytes(data: bytes, key: str) -> bytes:
    """Encrypt bytes for file processing"""
    return encrypt(data, key)

def decrypt_bytes(data: bytes, key: str) -> bytes:
    """Decrypt bytes for file processing"""
    return decrypt(data, key)
