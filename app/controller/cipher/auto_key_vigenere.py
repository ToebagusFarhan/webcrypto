def encrypt(plaintext, key):
    plaintext = ''.join(filter(str.isalpha, plaintext.upper()))
    key = key.upper()
    key_stream = key + plaintext[:-len(key)]
    ciphertext = ''
    for p, k in zip(plaintext, key_stream):
        shift = ord(k) - ord('A')
        encrypted_char = chr(((ord(p) - ord('A') + shift) % 26 + ord('A')))
        ciphertext += encrypted_char
    return ciphertext

def decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = ''
    key_part = key
    for i in range(len(ciphertext)):
        if i < len(key):
            k = key[i]
        else:
            k = plaintext[i - len(key)]
        shift = ord(k) - ord('A')
        decrypted_char = chr(((ord(ciphertext[i]) - ord('A') - shift) % 26 + ord('A')))
        plaintext += decrypted_char
    return plaintext

def encrypt_bytes(data: bytes, key: str) -> bytes:
    text = data.decode('utf-8', errors='ignore')  # Skip invalid UTF-8 bytes
    encrypted = encrypt(text, key)
    return encrypted.encode('utf-8')


def decrypt_bytes(data: bytes, key: str) -> bytes:
    text = data.decode('utf-8', errors='ignore')
    decrypted = decrypt(text, key)
    return decrypted.encode('utf-8')
