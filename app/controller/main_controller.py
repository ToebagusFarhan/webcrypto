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

# rubah jadi 5 letter
def format_ciphertext(ciphertext):
    # Remove spaces and format into 5-letter groups
    ciphertext = ciphertext.replace(" ", "")
    return ' '.join([ciphertext[i:i+5] for i in range(0, len(ciphertext), 5)])

def format_extended_ciphertext(ciphertext):
    """Return Readable format"""
    return ' '.join(f'{ord(c):02x}' for c in ciphertext)

def process_text_cipher(action, cipher_type, text, key, a=None, b=None, size=None):
    result = {}
    
    if cipher_type == 'vigenere':
        if action == 'encrypt':
            ciphertext = vigenere.encrypt(text, key)
            result['ciphertext'] = format_ciphertext(ciphertext)
            result['raw_cipher'] = ciphertext.replace(' ', '')  
        else:
            result['plaintext'] = vigenere.decrypt(text, key)
    
    elif cipher_type == 'auto_key_vigenere':
        if action == 'encrypt':
            ciphertext = auto_key_vigenere.encrypt(text, key)
            result['ciphertext'] = format_ciphertext(ciphertext)
            result['raw_cipher'] = ciphertext.replace(' ', '')  
        else:
            result['plaintext'] = auto_key_vigenere.decrypt(text, key)
    
    elif cipher_type == 'extended_vigenere':
        if action == 'encrypt':
            ciphertext = extended_vigenere.encrypt_text(text, key)
            result['ciphertext'] = ciphertext  # This is now hex string
            result['raw_cipher'] = ciphertext.replace(' ', '')  # Store without spaces for decryption
        else:
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
                result['raw_cipher'] = ciphertext.replace(' ', '')  
            else:
                result['plaintext'] = affine.decrypt(text, a, b)
        except ValueError as e:
            result['error'] = str(e)
    
    elif cipher_type == 'playfair':
        if action == 'encrypt':
            ciphertext = playfair.encrypt(text, key)
            result['ciphertext'] = format_ciphertext(ciphertext)
            result['raw_cipher'] = ciphertext.replace(' ', '')
            result['playfair_square'] = playfair.get_playfair_square(key)
        else:
            result['plaintext'] = playfair.decrypt(text, key)
            result['playfair_square'] = playfair.get_playfair_square(key)
    
    elif cipher_type == 'hill':
        try:
            size = int(size) if size else 2
            if action == 'encrypt':
                ciphertext = hill.encrypt(text, key, size)
                result['ciphertext'] = format_ciphertext(ciphertext)
                result['raw_cipher'] = ciphertext.replace(' ', '')  
            else:
                result['plaintext'] = hill.decrypt(text, key, size)
        except ValueError as e:
            result['error'] = str(e)
    
    return result


def process_file_cipher(action, cipher_type, file, key, a=None, b=None, size=None):
    result = {}

    try:
        file_content = file.read()
        processed_data = None

        if cipher_type == 'vigenere':
            if action == 'encrypt':
                processed_data = vigenere.encrypt_bytes(file_content, key)
            else:
                processed_data = vigenere.decrypt_bytes(file_content, key)

        elif cipher_type == 'auto_key_vigenere':
            if action == 'encrypt':
                processed_data = auto_key_vigenere.encrypt_bytes(file_content, key)
            else:
                processed_data = auto_key_vigenere.decrypt_bytes(file_content, key)

        elif cipher_type == 'extended_vigenere':
            if action == 'encrypt':
                processed_data = extended_vigenere.encrypt(file_content, key)
            else:
                processed_data = extended_vigenere.decrypt(file_content, key)

        elif cipher_type == 'affine':
            a = int(a)
            b = int(b)
            if action == 'encrypt':
                processed_data = affine.encrypt_bytes(file_content, a, b)
            else:
                processed_data = affine.decrypt_bytes(file_content, a, b)

        elif cipher_type == 'playfair':
            if action == 'encrypt':
                processed_data = playfair.encrypt_bytes(file_content, key)
            else:
                processed_data = playfair.decrypt_bytes(file_content, key)

        elif cipher_type == 'hill':
            size = int(size) if size else 2
            if action == 'encrypt':
                processed_data = hill.encrypt_bytes(file_content, key, size)
            else:
                processed_data = hill.decrypt_bytes(file_content, key, size)

        else:
            result['error'] = f"Cipher '{cipher_type}' does not support file processing."
            return result

        result['file_data'] = processed_data
        result['filename'] = secure_filename(file.filename)

    except Exception as e:
        result['error'] = str(e)

    return result