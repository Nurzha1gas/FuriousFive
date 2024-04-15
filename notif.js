  
document.addEventListener('DOMContentLoaded', function() {
    var profilePageLink = document.getElementById('profilePage');
  
    profilePageLink.addEventListener('click', function(e) {
      e.preventDefault(); // Prevent the default anchor behavior
      window.location.href = 'profile.html'; // Change the current page to 'profile.html'
    });
  });



  document.addEventListener('DOMContentLoaded', function() {
    var notifPageBtn = document.getElementById('notifPageBTN');
  
    notifPageBtn.addEventListener('click', function(e) {
      e.preventDefault(); // Предотвращает стандартное поведение элемента
      window.location.href = 'notifPage.html'; // Переход на страницу уведомлений
    });
  });
// Предполагаем, что у вас есть какой-то способ определить, находится ли пользователь на странице "Profile".
// Например, по URL страницы или на основе данных, доступных на странице.

if (window.location.pathname === 'profile.html') {
  document.getElementById('profilePage').classList.add('profile-active');
}