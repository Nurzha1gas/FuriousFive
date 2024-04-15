document.addEventListener("DOMContentLoaded", function() {
    const signUpButton = document.querySelector('.btn-signup');
    if (signUpButton) {
        signUpButton.addEventListener('click', function() {
            window.location.href = 'signup.html'; // Путь к вашему файлу sign up страницы
        });
    }
});



document.addEventListener("DOMContentLoaded", function() {
    const submitButton = document.querySelector('.btn3-ver');
    if (submitButton) {
        submitButton.addEventListener('click', function() {
            window.location.href = 'login.html'; // Путь к вашему файлу страницы логина
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвратить стандартную отправку формы

        
        console.log(document.getElementById('password')); // Should not be null
        const password = document.getElementById('password').value;

        
        if (password.length < 8) {
            alert("Password must be at least 8 characters long.");
            return;
        }

        if (!isPasswordStrong(password)) {
            alert("Password is too weak. It must contain at least one uppercase letter, one lowercase letter, one number, and one special character.");
            return;
        }

        // Перенаправляем на verif.html, если все проверки пройдены
        window.location.href = 'login.html';
    });

    function isPasswordStrong(password) {
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        const hasSpecialChar = /\W/.test(password);
        return hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChar;
    }
});