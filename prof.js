function toggleEdit() {
    var editBtn = document.querySelector('.edit-btn');
    var editables = document.querySelectorAll('.editable');
    var infoTexts = document.querySelectorAll('.info-text');
    var profileImage = document.getElementById('profile-image');
    var profileImageInput = document.getElementById('profile-image-input');
  
    if (editBtn.textContent === 'Edit') {
        // Enable editing
        editables.forEach(function(input) {
            input.style.display = 'inline-block';
            if (input.previousElementSibling) {
                input.previousElementSibling.style.display = 'none';
            }
        });
        profileImage.style.display = 'none';
        profileImageInput.style.display = 'inline-block';
        editBtn.textContent = 'Save';
    } else {
        // Save edits
        editables.forEach(function(input) {
            input.style.display = 'none';
            if (input.id === 'profile-image-input') {
                profileImage.src = input.value || 'https://img.icons8.com/bubbles/100/000000/user.png';
                profileImage.style.display = 'block';
            } else {
                var textSpan = input.previousElementSibling;
                textSpan.textContent = input.value;
                textSpan.style.display = 'block';
            }
        });
        editBtn.textContent = 'Edit';
    }
  }

  
  document.addEventListener('DOMContentLoaded', function() {
    var profilePageLink = document.getElementById('profilePage');
  
    profilePageLink.addEventListener('click', function(e) {
      e.preventDefault(); // Prevent the default anchor behavior
      window.location.href = 'profile.html'; // Change the current page to 'profile.html'
    });
  });




