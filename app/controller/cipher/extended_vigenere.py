def encrypt(data, key):
    """Handle both text and binary data"""
    if isinstance(data, str):
        data = data.encode('latin-1')
    key_bytes = key.encode('latin-1')
    encrypted_data = bytearray()
    for i, byte in enumerate(data):
        key_byte = key_bytes[i % len(key_bytes)]
        encrypted_byte = (byte + key_byte) % 256
        encrypted_data.append(encrypted_byte)
    return bytes(encrypted_data)

def decrypt(data, key):
    """Handle both text and binary data"""
    if isinstance(data, str):
        data = data.encode('latin-1')
    key_bytes = key.encode('latin-1')
    decrypted_data = bytearray()
    for i, byte in enumerate(data):
        key_byte = key_bytes[i % len(key_bytes)]
        decrypted_byte = (byte - key_byte) % 256
        decrypted_data.append(decrypted_byte)
    return bytes(decrypted_data)

def encrypt_text(text, key):
    """Encrypt text and return hex string for display"""
    encrypted_bytes = encrypt(text.encode('latin-1'), key)
    return encrypted_bytes.hex(' ')

def decrypt_hex(hex_str, key):
    """Decrypt hex string back to original text"""
    hex_str = hex_str.replace(' ', '')  # Remove spaces if present
    encrypted_bytes = bytes.fromhex(hex_str)
    decrypted_bytes = decrypt(encrypted_bytes, key)
    return decrypted_bytes.decode('latin-1')