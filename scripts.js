document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    
    // Debugging the registration form
    const registerForm = document.getElementById('register-form');
    const registerUsername = document.getElementById('register-username');
    const registerPassword = document.getElementById('register-password');

    if (registerForm && registerUsername && registerPassword) {
        console.log('Registration form elements found');
        registerForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const username = registerUsername.value;
            const password = registerPassword.value;

            if (username && password) {
                const users = JSON.parse(localStorage.getItem('users') || '[]');
                users.push({ username, password });
                localStorage.setItem('users', JSON.stringify(users));
                document.getElementById('message').textContent = 'Usuario registrado exitosamente';
                console.log('User registered:', { username, password });
            } else {
                console.log('Username or password is missing');
            }
        });
    } else {
        console.error('Registration form elements not found');
    }

    // Debugging the login form
    const loginForm = document.getElementById('login-form');
    const loginUsername = document.getElementById('login-username');
    const loginPassword = document.getElementById('login-password');

    if (loginForm && loginUsername && loginPassword) {
        console.log('Login form elements found');
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const username = loginUsername.value;
            const password = loginPassword.value;

            const users = JSON.parse(localStorage.getItem('users') || '[]');
            const user = users.find(u => u.username === username && u.password === password);

            if (user) {
                document.getElementById('message').textContent = 'Login exitoso';
                console.log('Login successful for user:', username);
            } else {
                document.getElementById('message').textContent = 'Usuario o contraseña incorrectos';
                console.log('Login failed for user:', username);
            }
        });
    } else {
        console.error('Login form elements not found');
    }
});