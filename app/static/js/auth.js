document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const accountForm = document.getElementById('accountForm');
    const logoutButton = document.getElementById('logoutButton');

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('regUsername').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;

            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password })
            });

            const result = await response.json();
            document.getElementById('registerMessage').innerText = result.message || result.error;
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const result = await response.json();
            document.getElementById('loginMessage').innerText = result.message || result.error;
        });
    }

    if (accountForm) {
        fetch('/account', { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('accountMessage').innerText = data.error;
                } else {
                    accountForm.style.display = 'block';
                    document.getElementById('accUsername').value = data.username;
                    document.getElementById('accEmail').value = data.email;
                }
            });

        accountForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('accUsername').value;
            const email = document.getElementById('accEmail').value;
            const currentPassword = document.getElementById('currentPassword').value;
            const newPassword = document.getElementById('newPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            const response = await fetch('/account', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, current_password: currentPassword, new_password: newPassword, confirm_password: confirmPassword })
            });

            const result = await response.json();
            document.getElementById('accountMessage').innerText = result.message || result.error;
        });
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            const response = await fetch('/logout', { method: 'POST' });
            const result = await response.json();
            alert(result.message || result.error);
        });
    }
});
