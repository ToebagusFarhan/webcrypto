def track_spaces(text):
    """Track positions of spaces in text"""
    space_positions = []
    for i, char in enumerate(text):
        if char.isspace():
            space_positions.append(i)
    return ''.join(c for c in text if not c.isspace()), space_positions

def restore_spaces(text, space_positions):
    """Restore spaces to their original positions"""
    result = list(text)
    for pos in space_positions:
        result.insert(pos, ' ')
    return ''.join(result)

def encrypt(plaintext, key):
    # Track spaces before encryption
    plaintext_no_spaces, space_positions = track_spaces(plaintext)
    plaintext_no_spaces = ''.join(filter(str.isalpha, plaintext_no_spaces.upper()))
    key = key.upper()
    key_repeated = (key * (len(plaintext_no_spaces) // len(key) + 1))[:len(plaintext_no_spaces)]
    ciphertext = ''
    for p, k in zip(plaintext_no_spaces, key_repeated):
        shift = ord(k) - ord('A')
        encrypted_char = chr(((ord(p) - ord('A') + shift) % 26 + ord('A')))
        ciphertext += encrypted_char
    return ciphertext

def decrypt(ciphertext, key):
    # Remove formatting spaces (5-letter groups)
    ciphertext = ciphertext.replace(' ', '')
    ciphertext = ciphertext.upper()
    key = key.upper()
    key_repeated = (key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]
    plaintext = ''
    for c, k in zip(ciphertext, key_repeated):
        shift = ord(k) - ord('A')
        decrypted_char = chr(((ord(c) - ord('A') - shift) % 26 + ord('A')))
        plaintext += decrypted_char
    return plaintext

def encrypt_bytes(data: bytes, key: str) -> bytes:
    text = data.decode('utf-8', errors='ignore')  
    encrypted_text = encrypt(text, key)
    return encrypted_text.encode('utf-8')


def decrypt_bytes(data: bytes, key: str) -> bytes:
    text = data.decode('utf-8', errors='ignore')
    decrypted_text = decrypt(text, key)
    return decrypted_text.encode('utf-8')