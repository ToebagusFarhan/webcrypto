import numpy as np

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
    det = int(np.round(np.linalg.det(matrix)))
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