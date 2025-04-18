def prepare_key(key):
    key = key.upper().replace("J", "I")
    key_matrix = []
    for char in key:
        if char not in key_matrix and char.isalpha():
            key_matrix.append(char)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in key_matrix:
            key_matrix.append(char)
    return [key_matrix[i:i+5] for i in range(0, 25, 5)]

def prepare_text(plaintext):
    plaintext = plaintext.upper().replace("J", "I")
    plaintext = ''.join(filter(str.isalpha, plaintext))
    i = 0
    while i < len(plaintext) - 1:
        if plaintext[i] == plaintext[i+1]:
            plaintext = plaintext[:i+1] + 'X' + plaintext[i+1:]
        i += 2
    if len(plaintext) % 2 != 0:
        plaintext += 'X'
    return plaintext

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
            ciphertext += matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            ciphertext += matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            ciphertext += matrix[row_a][col_b] + matrix[row_b][col_a]
    return ciphertext

def decrypt(ciphertext, key):
    matrix = prepare_key(key)
    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        
        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b] + matrix[row_b][col_a]
    return plaintext