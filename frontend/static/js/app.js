function previewImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var preview = document.getElementById('image-preview');
            preview.src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function togglePasswordVisibility(passwordField) {
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
}

function toggleGeneratePasswordButton(button, passwordGroup, passwordField, passwordChanged) {
    console.log(passwordChanged)
    passwordChanged.value = true
    passwordGroup.style.display = 'block';
    passwordField.style.display = 'block';
    passwordField.value = generateRandomPassword()
}

function generateRandomPassword() {
    var length = 10; // Длина пароля
    var password = "";

    for (var i = 0; i < length; i++) {
        var randomCode = Math.floor(Math.random() * (0x7e - 0x21 + 1)) + 0x21;
        var randomChar = String.fromCharCode(randomCode);
        password += randomChar;
    }

    return password;
}


function openModal() {
    $('#selectEmployeeModal').modal('show');
}