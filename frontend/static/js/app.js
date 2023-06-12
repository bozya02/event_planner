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

function openModal(modalId) {
    // Устанавливаем текст задачи в содержимое модального окна
    $('#' + modalId).modal('show');
}

function createTaskChart(taskData) {
    let ctx = document.getElementById('taskChart').getContext('2d');
    let chart = new Chart(ctx, {
        type: 'doughnut', data: taskData, options: {
            responsive: true, legend: {
                position: 'right',
            },
        },
    });
}

function changeTaskState(taskId, state) {
    $.ajax({
        url: '/check_task/' + taskId, type: 'POST', data: {
            'state': state,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        }, success: function (response) {
            location.reload();
        }, error: function (xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
}