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
