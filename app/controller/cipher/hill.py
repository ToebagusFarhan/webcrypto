import numpy as np

# --- TEXT-BASED HILL CIPHER ---

def text_to_num(text):
    return [ord(char) - ord('A') for char in text]

def num_to_text(nums):
    return ''.join([chr(num + ord('A')) for num in nums])

def prepare_key(key, size):
    key = key.upper()
    key = ''.join(filter(str.isalpha, key))
    while len(key) < size * size:
        key += 'A'
    key = key[:size*size]
    key_matrix = text_to_num(key)
    return np.array(key_matrix).reshape(size, size)

def prepare_text(plaintext, size):
    plaintext = plaintext.upper()
    plaintext = ''.join(filter(str.isalpha, plaintext))
    while len(plaintext) % size != 0:
        plaintext += 'X'
    return plaintext

def mod_inverse_matrix(matrix, mod):
    det = int(round(np.linalg.det(matrix)))
    det_inv = pow(det, -1, mod)
    adj = np.round(det * np.linalg.inv(matrix)).astype(int)
    return (det_inv * adj) % mod

def encrypt(plaintext, key, size=2):
    key_matrix = prepare_key(key, size)
    plaintext = prepare_text(plaintext, size)
    ciphertext = ''
    for i in range(0, len(plaintext), size):
        block = plaintext[i:i+size]
        nums = text_to_num(block)
        encrypted_nums = np.dot(key_matrix, nums) % 26
        ciphertext += num_to_text(encrypted_nums)
    return ciphertext

def decrypt(ciphertext, key, size=2):
    key_matrix = prepare_key(key, size)
    try:
        inv_key = mod_inverse_matrix(key_matrix, 26)
    except ValueError:
        raise ValueError("Key matrix is not invertible (determinant has no modular inverse)")
    
    plaintext = ''
    for i in range(0, len(ciphertext), size):
        block = ciphertext[i:i+size]
        nums = text_to_num(block)
        decrypted_nums = np.dot(inv_key, nums) % 26
        plaintext += num_to_text(decrypted_nums)
    return plaintext

# --- BYTE-BASED HILL CIPHER FOR FILES ---

def prepare_key_bytes(key: str, size: int) -> np.ndarray:
    key_bytes = key.encode('latin-1')
    while len(key_bytes) < size * size:
        key_bytes += b'\x00'
    key_bytes = key_bytes[:size * size]
    return np.array(list(key_bytes)).reshape(size, size)

def encrypt_bytes(data: bytes, key: str, size: int = 2) -> bytes:
    key_matrix = prepare_key_bytes(key, size)
    while len(data) % size != 0:
        data += b'\x00'

    result = bytearray()
    for i in range(0, len(data), size):
        block = np.array(list(data[i:i+size]))
        encrypted = np.dot(key_matrix, block) % 256
        result.extend(encrypted.astype(np.uint8))
    return bytes(result)

def decrypt_bytes(data: bytes, key: str, size: int = 2) -> bytes:
    key_matrix = prepare_key_bytes(key, size)
    try:
        inv_matrix = mod_inverse_matrix(key_matrix, 256)
    except Exception:
        raise ValueError("Key matrix is not invertible mod 256.")

    result = bytearray()
    for i in range(0, len(data), size):
        block = np.array(list(data[i:i+size]))
        decrypted = np.dot(inv_matrix, block) % 256
        result.extend(decrypted.astype(np.uint8))
    return bytes(result)
