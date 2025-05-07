from werkzeug.utils import secure_filename
from .cipher import (
    vigenere, 
    auto_key_vigenere, 
    extended_vigenere, 
    affine, 
    playfair, 
    hill
)

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'bin', 'pdf', 'docx', 'jpg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_ciphertext(ciphertext):
    # Remove spaces and format into 5-letter groups
    ciphertext = ciphertext.replace(" ", "")
    return ' '.join([ciphertext[i:i+5] for i in range(0, len(ciphertext), 5)])

def format_extended_ciphertext(ciphertext):
    """Return Readable format"""
    return ' '.join(f'{ord(c):02x}' for c in ciphertext)

def process_text_cipher(action, cipher_type, text, key, a=None, b=None, size=None):
    """Memproses teks menggunakan berbagai algoritma cipher.
    Fungsi ini menangani berbagai jenis operasi cipher (enkripsi/dekripsi)
    berdasarkan jenis cipher dan parameter yang ditentukan.
    Args:
        action (str): Aksi yang akan dilakukan ('encrypt' atau 'decrypt')
        cipher_type (str): Jenis cipher yang digunakan ('vigenere', 'auto_key_vigenere',
                          'extended_vigenere', 'affine', 'playfair', 'hill')
        text (str): Teks masukan yang akan diproses
        key (str): Kunci enkripsi/dekripsi
        a (int, optional): Parameter 'a' untuk cipher affine. Default: None.
        b (int, optional): Parameter 'b' untuk cipher affine. Default: None.
        size (int, optional): Ukuran matriks untuk cipher hill. Default: None.
    Returns:
        dict: Dictionary yang berisi:
            - {'ciphertext': str} untuk enkripsi
            - {'plaintext': str} untuk dekripsi
            - {'error': str} jika terjadi kesalahan
            - Untuk enkripsi extended_vigenere juga menyertakan {'raw_cipher': str}
    Raises:
        ValueError: Jika parameter yang tidak valid diberikan untuk cipher affine atau hill
    """
    result = {}
    
    if cipher_type == 'vigenere':
        if action == 'encrypt':
            ciphertext = vigenere.encrypt(text, key)
            result['ciphertext'] = format_ciphertext(ciphertext)
        else:
            result['plaintext'] = vigenere.decrypt(text, key)
    
    elif cipher_type == 'auto_key_vigenere':
        if action == 'encrypt':
            ciphertext = auto_key_vigenere.encrypt(text, key)
            result['ciphertext'] = format_ciphertext(ciphertext)
        else:
            result['plaintext'] = auto_key_vigenere.decrypt(text, key)
    
    elif cipher_type == 'extended_vigenere':
        if action == 'encrypt':
            ciphertext = extended_vigenere.encrypt_text(text, key)
            result['ciphertext'] = ciphertext  # This is now hex string
            result['raw_cipher'] = ciphertext.replace(' ', '')  # Store without spaces for decryption
        else:
            # For decryption, we expect the hex string input
            try:
                result['plaintext'] = extended_vigenere.decrypt_hex(text, key)
            except ValueError as e:
                result['error'] = f"Invalid hex input: {str(e)}"
    
    elif cipher_type == 'affine':
        try:
            a = int(a)
            b = int(b)
            if action == 'encrypt':
                ciphertext = affine.encrypt(text, a, b)
                result['ciphertext'] = format_ciphertext(ciphertext)
            else:
                result['plaintext'] = affine.decrypt(text, a, b)
        except ValueError as e:
            result['error'] = str(e)
    
    elif cipher_type == 'playfair':
        if action == 'encrypt':
            ciphertext = playfair.encrypt(text, key)
            result['ciphertext'] = format_ciphertext(ciphertext)
        else:
            result['plaintext'] = playfair.decrypt(text, key)
    
    elif cipher_type == 'hill':
        try:
            size = int(size) if size else 2
            if action == 'encrypt':
                ciphertext = hill.encrypt(text, key, size)
                result['ciphertext'] = format_ciphertext(ciphertext)
            else:
                result['plaintext'] = hill.decrypt(text, key, size)
        except ValueError as e:
            result['error'] = str(e)
    
    return result

def process_file_cipher(action, cipher_type, file, key):
    result = {}
    
    if cipher_type != 'extended_vigenere':
        result['error'] = "Only Extended Vigenere cipher supports file encryption/decryption"
        return result
    
    try:
        file_content = file.read()
        
        if action == 'encrypt':
            processed_data = extended_vigenere.encrypt(file_content, key)
        else:
            processed_data = extended_vigenere.decrypt(file_content, key)
        
        result['file_data'] = processed_data
        result['filename'] = secure_filename(file.filename)
    
    except Exception as e:
        result['error'] = str(e)
    
    return result