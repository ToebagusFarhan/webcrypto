document.addEventListener('DOMContentLoaded', function() {
    // Toggle between text input and file upload
    const inputTypeRadios = document.querySelectorAll('input[name="input_type"]');
    const textInputDiv = document.getElementById('text_input');
    const fileInputDiv = document.getElementById('file_input');
    
    inputTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'text') {
                textInputDiv.style.display = 'block';
                fileInputDiv.style.display = 'none';
            } else {
                textInputDiv.style.display = 'none';
                fileInputDiv.style.display = 'block';
            }
        });
    });
    
    // Show/hide additional parameters based on cipher type
    const cipherTypeSelect = document.getElementById('cipher_type');
    const affineParams = document.getElementById('affine_params');
    const hillParams = document.getElementById('hill_params');
    
    cipherTypeSelect.addEventListener('change', function() {
        // Hide all parameter sections first
        document.querySelectorAll('.cipher-params').forEach(el => {
            el.style.display = 'none';
        });
        
        // Show relevant parameters
        if (this.value === 'affine') {
            affineParams.style.display = 'block';
        } else if (this.value === 'hill') {
            hillParams.style.display = 'block';
        }
    });
    
    // Trigger change event on page load to set initial state
    cipherTypeSelect.dispatchEvent(new Event('change'));
    document.querySelector('input[name="input_type"][value="text"]').dispatchEvent(new Event('change'));
});

function copyToClipboard(selector) {
    const text = document.querySelector(selector).innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}