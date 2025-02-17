document.getElementById('register-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    if (username && password) {
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        users.push({ username, password });
        localStorage.setItem('users', JSON.stringify(users));
        document.getElementById('message').textContent = 'Usuario registrado exitosamente';
    }
});

document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const user = users.find(u => u.username === username && u.password === password);

    if (user) {
        document.getElementById('message').textContent = 'Login exitoso';
    } else {
        document.getElementById('message').textContent = 'Usuario o contraseña incorrectos';
    }
});