document.addEventListener('DOMContentLoaded', function() {
  const userProfileButton = document.getElementById('user-menu-button');
  const userProfileMenu = document.getElementById('menu');

  // Set initial state: menu closed
  userProfileButton.setAttribute('aria-expanded', 'false');
  userProfileMenu.classList.add('hidden');

  // Add click event listener to the user profile button
  userProfileButton.addEventListener('click', function(event) {
    // Toggle the aria-expanded attribute
    const expanded = userProfileButton.getAttribute('aria-expanded') === 'true' || false;
    userProfileButton.setAttribute('aria-expanded', !expanded);

    // Toggle the visibility of the dropdown menu
    userProfileMenu.classList.toggle('hidden');
  });

  // Close the dropdown menu when clicking outside of it
  document.addEventListener('click', function(event) {
    if (!userProfileButton.contains(event.target) && !userProfileMenu.contains(event.target)) {
      userProfileButton.setAttribute('aria-expanded', 'false');
      userProfileMenu.classList.add('hidden');
    }
  });
});
