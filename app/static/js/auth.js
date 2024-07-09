document.addEventListener('DOMContentLoaded', function() {
    const accountForm = document.getElementById('accountForm');
    const accountMessage = document.getElementById('accountMessage');

    if (accountForm) {
        fetch('/auth/account/data', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                accountForm.style.display = 'block';
            }
            document.getElementById('accUsername').value = data.username || '';
            document.getElementById('accEmail').value = data.email || '';
        })
        .catch(error => {
            accountMessage.textContent = 'Error fetching account information.';
        });

        accountForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            const newUsername = document.getElementById('accUsername').value;
            const newEmail = document.getElementById('accEmail').value;
            const currentPassword = document.getElementById('currentPassword').value;
            const newPassword = document.getElementById('newPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            fetch('/auth/account', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken  // Include the CSRF token in the headers
                },
                body: JSON.stringify({
                    username: newUsername,
                    email: newEmail,
                    current_password: currentPassword,
                    new_password: newPassword,
                    confirm_password: confirmPassword
                })
            })
            .then(response => response.json())
            .then(data => {
                accountMessage.textContent = data.message || 'Account updated successfully.';
            })
            .catch(error => {
                accountMessage.textContent = 'Error updating account information.';
            });
        });
    }
});
