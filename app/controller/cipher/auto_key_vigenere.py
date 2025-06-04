def track_spaces(text):
    space_positions = []
    for i, char in enumerate(text):
        if char.isspace():
            space_positions.append(i)
    return ''.join(c for c in text if not c.isspace()), space_positions

def restore_spaces(text, space_positions):
    result = list(text)
    for pos in space_positions:
        result.insert(pos, ' ')
    return ''.join(result)

def encrypt(plaintext, key):
    text_no_spaces, space_positions = track_spaces(plaintext)
    key = key.upper()
    plain_alpha = ''.join(filter(str.isalpha, text_no_spaces.upper()))
    key_stream = key + plain_alpha[:-len(key)]
    
    result = ''
    j = 0  # Index for key_stream
    for char in text_no_spaces:
        if char.isalpha():
            p = char.upper()
            k = key_stream[j]
            shift = ord(k) - ord('A')
            encrypted_char = chr(((ord(p) - ord('A') + shift) % 26 + ord('A')))
            result += encrypted_char
            j += 1
        else:
            result += char
            
    return result

def decrypt(ciphertext, key):
    text_no_spaces = ciphertext.replace(' ', '')
    key = key.upper()
    result = ''
    plain_so_far = ''
    
    j = 0
    for char in text_no_spaces:
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
