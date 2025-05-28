
def prepare_key(key):
    key = key.upper().replace("J", "I")
    key_matrix = []
    for char in key:
        if char.isalpha() and char not in key_matrix:
            key_matrix.append(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in key_matrix:
            key_matrix.append(char)
    return [key_matrix[i:i+5] for i in range(0, 25, 5)]

def prepare_text(plaintext):
    plaintext = plaintext.upper().replace("J", "I")
    plaintext = ''.join(filter(str.isalpha, plaintext))
    i = 0
    result = ''
    while i < len(plaintext):
        a = plaintext[i]
        b = plaintext[i+1] if i+1 < len(plaintext) else 'X'
        if a == b:
            result += a + 'X'
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += 'X'
    return result

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return -1, -1

def encrypt(plaintext, key):
    matrix = prepare_key(key)
    plaintext = prepare_text(plaintext)
    ciphertext = ''
    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        if row_a == row_b:
            ciphertext += matrix[row_a][(col_a + 1) % 5]
            ciphertext += matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            ciphertext += matrix[(row_a + 1) % 5][col_a]
            ciphertext += matrix[(row_b + 1) % 5][col_b]
        else:
            ciphertext += matrix[row_a][col_b]
            ciphertext += matrix[row_b][col_a]
    return ciphertext

def decrypt(ciphertext, key):
    matrix = prepare_key(key)
    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5]
            plaintext += matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a]
            plaintext += matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b]
            plaintext += matrix[row_b][col_a]
    return plaintext

def get_playfair_square(key):
    """Returns the Playfair square as a 5x5 matrix for visualization"""
    return prepare_key(key)


def prepare_key_bytes(key: str) -> list:
    key_bytes = []
    seen = set()
    for char in key.encode('latin-1'):
        if char not in seen:
            seen.add(char)
            key_bytes.append(char)
    for i in range(256):
        if i not in seen:
            key_bytes.append(i)
    matrix = [key_bytes[i:i+16] for i in range(0, 256, 16)]  # 16x16 grid for byte values
    return matrix

def find_position_bytes(matrix, byte_val):
    for row in range(16):
        for col in range(16):
            if matrix[row][col] == byte_val:
                return row, col
    return -1, -1

def encrypt_bytes(data: bytes, key: str) -> bytes:
    matrix = prepare_key_bytes(key)
    if len(data) % 2 != 0:
        data += b'\x00'
    result = bytearray()
    for i in range(0, len(data), 2):
        a, b = data[i], data[i+1]
        row_a, col_a = find_position_bytes(matrix, a)
        row_b, col_b = find_position_bytes(matrix, b)
        if row_a == row_b:
            result.append(matrix[row_a][(col_a + 1) % 16])
            result.append(matrix[row_b][(col_b + 1) % 16])
        elif col_a == col_b:
            result.append(matrix[(row_a + 1) % 16][col_a])
            result.append(matrix[(row_b + 1) % 16][col_b])
        else:
            result.append(matrix[row_a][col_b])
            result.append(matrix[row_b][col_a])
    return bytes(result)

def decrypt_bytes(data: bytes, key: str) -> bytes:
    matrix = prepare_key_bytes(key)
    result = bytearray()
    for i in range(0, len(data), 2):
        a, b = data[i], data[i+1]
        row_a, col_a = find_position_bytes(matrix, a)
        row_b, col_b = find_position_bytes(matrix, b)
        if row_a == row_b:
            result.append(matrix[row_a][(col_a - 1) % 16])
            result.append(matrix[row_b][(col_b - 1) % 16])
        elif col_a == col_b:
            result.append(matrix[(row_a - 1) % 16][col_a])
            result.append(matrix[(row_b - 1) % 16][col_b])
        else:
            result.append(matrix[row_a][col_b])
            result.append(matrix[row_b][col_a])
    return bytes(result)
