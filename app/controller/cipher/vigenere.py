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