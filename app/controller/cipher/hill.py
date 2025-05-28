import numpy as np

# --- TEXT-BASED HILL CIPHER ---

def text_to_num(text):
    return [ord(char) - ord('A') for char in text]

def num_to_text(nums):
    return ''.join([chr(int(round(num)) + ord('A')) for num in nums])

def matrix_mod_inverse(matrix, modulus):
    """Calculate the modular multiplicative inverse of a matrix"""
    det = int(round(np.linalg.det(matrix)))
    det_inv = None
    
    # Find modular multiplicative inverse of determinant
    for i in range(modulus):
        if (det * i) % modulus == 1:
            det_inv = i
            break
    
    if det_inv is None:
        raise ValueError("Matrix is not invertible")

    # Calculate adjugate matrix
    adj = np.round(det * np.linalg.inv(matrix)).astype(int)
    
    # Calculate modular multiplicative inverse of matrix
    inv = (det_inv * adj) % modulus
    return inv

def prepare_key(key, size):
    key = key.upper()
    key = ''.join(filter(str.isalnum, key))
    key_nums = []
    
    for char in key:
        if char.isalpha():
            key_nums.append(ord(char) - ord('A'))
        elif char.isdigit():
            key_nums.append(int(char) % 26)  # Ensure numbers are within modulo 26
            
    # Pad with sequential numbers if key is too short
    while len(key_nums) < size * size:
        next_val = len(key_nums) % 26
        key_nums.append(next_val)
        
    key_matrix = np.array(key_nums[:size*size]).reshape(size, size)
    
    # Verify matrix is invertible
    try:
        matrix_mod_inverse(key_matrix, 26)
    except:
        raise ValueError("Key matrix must be invertible modulo 26. Try a different key.")
        
    return key_matrix

def prepare_text(text, size):
    text = text.upper()
    text = ''.join(filter(str.isalpha, text))
    # Pad with 'X' to make length multiple of size
    while len(text) % size != 0:
        text += 'X'
    return text

def encrypt(plaintext, key, size=2):
    key_matrix = prepare_key(key, size)
    plaintext = prepare_text(plaintext, size)
    ciphertext = ''
    
    for i in range(0, len(plaintext), size):
        block = text_to_num(plaintext[i:i+size])
        result = np.dot(key_matrix, block) % 26
        ciphertext += num_to_text(result)
        
    return ciphertext

def decrypt(ciphertext, key, size=2):
    key_matrix = prepare_key(key, size)
    inv_key = matrix_mod_inverse(key_matrix, 26)
    plaintext = ''
    
    for i in range(0, len(ciphertext), size):
        block = text_to_num(ciphertext[i:i+size])
        result = np.dot(inv_key, block) % 26
        plaintext += num_to_text(result)
        
    return plaintext

# --- BYTE-BASED HILL CIPHER FOR FILES ---

def encrypt_bytes(data: bytes, key: str, size: int = 2) -> bytes:
    # For file encryption, use modulo 256 instead of 26
    key_bytes = [ord(c) % 256 for c in key]
    while len(key_bytes) < size * size:
        key_bytes.append(len(key_bytes) % 256)
    key_matrix = np.array(key_bytes[:size*size]).reshape(size, size)
    
    # Pad data to match matrix size
    if len(data) % size != 0:
        data = data + b'\x00' * (size - (len(data) % size))
    
    result = bytearray()
    for i in range(0, len(data), size):
        block = np.array([x for x in data[i:i+size]])
        encrypted = np.dot(key_matrix, block) % 256
        result.extend(encrypted.astype(np.uint8))
    
    return bytes(result)

def decrypt_bytes(data: bytes, key: str, size: int = 2) -> bytes:
    # Similar to encrypt_bytes but with inverse matrix
    key_bytes = [ord(c) % 256 for c in key]
    while len(key_bytes) < size * size:
        key_bytes.append(len(key_bytes) % 256)
    key_matrix = np.array(key_bytes[:size*size]).reshape(size, size)
    
    try:
        inv_matrix = matrix_mod_inverse(key_matrix, 256)
    except:
        raise ValueError("Key matrix is not invertible mod 256. Try a different key.")
    
    result = bytearray()
    for i in range(0, len(data), size):
        block = np.array([x for x in data[i:i+size]])
        decrypted = np.dot(inv_matrix, block) % 256
        result.extend(decrypted.astype(np.uint8))
    
    return bytes(result)
