def encrypt(plaintext, key):
    plaintext = ''.join(filter(str.isalpha, plaintext.upper()))
    key = key.upper()
    key_repeated = (key * (len(plaintext) // len(key) + 1))[:len(plaintext)]
    ciphertext = ''
    for p, k in zip(plaintext, key_repeated):
        shift = ord(k) - ord('A')
        encrypted_char = chr(((ord(p) - ord('A') + shift) % 26 + ord('A')))
        ciphertext += encrypted_char
    return ciphertext

def decrypt(ciphertext, key):
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