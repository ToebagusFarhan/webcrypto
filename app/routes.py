from flask import render_template, request, redirect, url_for, flash, send_file, jsonify
from app import app
from app.controller.main_controller import (
    allowed_file, 
    process_text_cipher, 
    process_file_cipher,
    UPLOAD_FOLDER
)
import os
from io import BytesIO
import tempfile

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        cipher_type = request.form.get('cipher_type')
        key = request.form.get('key')
        text = request.form.get('text')
        file = request.files.get('file')
        
        # Additional parameters
        a = request.form.get('a')
        b = request.form.get('b')
        size = request.form.get('size')
        
        if not all([action, cipher_type, key]):
            flash('Missing required fields', 'error')
            return redirect(url_for('index'))

        try:
            # Handle file operations
            if file and file.filename and allowed_file(file.filename):
                result = process_file_cipher(action, cipher_type, file, key)
                if 'error' in result:
                    flash(result['error'], 'error')
                    return redirect(url_for('index'))

                # Create in-memory file
                file_stream = BytesIO(result['file_data'])
                file_stream.seek(0)
                
                # Determine filename
                original_name = os.path.splitext(result['filename'])[0]
                ext = os.path.splitext(result['filename'])[1]
                new_filename = f"{original_name}_{action}ed{ext}"
                
                return send_file(
                    file_stream,
                    as_attachment=True,
                    download_name=new_filename,
                    mimetype='application/octet-stream'
                )

            # Handle text operations
            elif text:
                result = process_text_cipher(action, cipher_type, text, key, a, b, size)
                if 'error' in result:
                    flash(result['error'], 'error')
                    return redirect(url_for('index'))
                
                return render_template('result.html', 
                                    action=action,
                                    cipher_type=cipher_type,
                                    original_text=text,
                                    result=result)

            else:
                flash('Either text or a valid file must be provided', 'error')
                return redirect(url_for('index'))

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/download')
def download():
    text = request.args.get('text', '')
    file = BytesIO(text.encode('utf-8'))
    file.seek(0)
    return send_file(
        file,
        as_attachment=True,
        download_name='ciphertext.txt',
        mimetype='text/plain'
    )