document.addEventListener('DOMContentLoaded', function() {
    // Toggle between text input and file upload
    const inputTypeRadios = document.querySelectorAll('input[name="input_type"]');
    const textInputDiv = document.getElementById('text_input');
    const fileInputDiv = document.getElementById('file_input');
    const fileRadioInput = document.querySelector('input[name="input_type"][value="file"]');
    
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
            // Disable file input and switch to text input
            fileRadioInput.disabled = false;
            document.querySelector('input[name="input_type"][value="text"]').checked = true;
            textInputDiv.style.display = 'block';
            fileInputDiv.style.display = 'none';
        } else if (this.value === 'hill') {
            hillParams.style.display = 'block';
            // Disable file input and switch to text input
            fileRadioInput.disabled = false;
            document.querySelector('input[name="input_type"][value="text"]').checked = true;
            textInputDiv.style.display = 'block';
            fileInputDiv.style.display = 'none';
        } else if (this.value === 'extended_vigenere') {
            // Enable file input for extended vigenere
            fileRadioInput.disabled = false;
        } else {
            // Disable file input for other ciphers
            fileRadioInput.disabled = false;
            document.querySelector('input[name="input_type"][value="text"]').checked = true;
            textInputDiv.style.display = 'block';
            fileInputDiv.style.display = 'none';
        }
    });
    
    // Trigger change event on page load to set initial state
    cipherTypeSelect.dispatchEvent(new Event('change'));
    document.querySelector('input[name="input_type"][value="text"]').dispatchEvent(new Event('change'));

    // Mode slider functionality
    const slider = document.getElementById('action-slider');
    const hiddenInput = document.getElementById('action');
    const labels = document.querySelectorAll('.slider-labels span');

    function updateSlider() {
        const value = slider.value;
        hiddenInput.value = value === '0' ? 'encrypt' : 'decrypt';
        
        // Update labels
        labels.forEach((label, index) => {
            if (index.toString() === value) {
                label.classList.add('active');
            } else {
                label.classList.remove('active');
            }
        });
    }

    slider.addEventListener('input', updateSlider);
    
    // Handle label clicks
    labels.forEach((label, index) => {
        label.addEventListener('click', () => {
            slider.value = index;
            updateSlider();
        });
    });
    
    // Theme switching functionality
    const themeToggle = document.getElementById('theme-toggle');
    const themeLabel = themeToggle.querySelector('.theme-label');
    const sunIcon = themeToggle.querySelector('.sun-icon');
    
    // Check if user has a saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeToggle(savedTheme);
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeToggle(newTheme);
    });
    
    function updateThemeToggle(theme) {
        if (theme === 'light') {
            themeLabel.textContent = 'Dark';
            sunIcon.style.transform = 'rotate(180deg)';
        } else {
            themeLabel.textContent = 'Light';
            sunIcon.style.transform = 'rotate(0)';
        }
    }
});

function copyToClipboard(selector) {
    const text = document.querySelector(selector).innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert('SUDAH DI KOPI KANG!');
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}