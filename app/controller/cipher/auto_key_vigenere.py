def encrypt(plaintext, key):
    key = key.upper()
    result = ''
    # Sumber masalah, ngilangin non-alpha tapi spasinya ngikut jirr
    # Fix it, mechanic
    plain_alpha = ''.join(filter(str.isalpha, plaintext.upper()))
    key_stream = key + plain_alpha[:-len(key)]
    
    j = 0  # Indeks untuk key_stream
    for i, char in enumerate(plaintext):
        if char.isalpha():
            # ENKRIPSI HURUF DOANG
            p = char.upper()
            k = key_stream[j]
            shift = ord(k) - ord('A')
            encrypted_char = chr(((ord(p) - ord('A') + shift) % 26 + ord('A')))
            result += encrypted_char
            j += 1
        else:
            # INI BUAT SPASI, JANGAN DIHAPUS WOI
            result += char
    return result

def decrypt(ciphertext, key):
    key = key.upper()
    result = ''
    plain_so_far = ''
    
    j = 0 
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            if j < len(key):
                k = key[j]
            else:
                k = plain_so_far[j - len(key)]
            
            shift = ord(k) - ord('A')
            decrypted_char = chr(((ord(char.upper()) - ord('A') - shift) % 26 + ord('A')))
            result += decrypted_char
            plain_so_far += decrypted_char
            j += 1
        else:
            result += char
    return result

def encrypt_bytes(data: bytes, key: str) -> bytes:
    text = data.decode('utf-8', errors='ignore')  
    encrypted = encrypt(text, key)
    return encrypted.encode('utf-8')


def decrypt_bytes(data: bytes, key: str) -> bytes:
    text = data.decode('utf-8', errors='ignore')
    decrypted = decrypt(text, key)
    return decrypted.encode('utf-8')
