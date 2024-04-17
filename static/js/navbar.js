document.addEventListener('DOMContentLoaded', function() {
    // Get the user profile button and the dropdown menu
    const userProfileButton = document.getElementById('user-menu-button');
    // const userProfileMenu = document.getElementById('menu');
    const userProfileMenu = decument.getElementById('menu');
  
    // Add click event listener to the user profile button
    userProfileButton.addEventListener('click', function() {
      // Toggle the visibility of the dropdown menu
      userProfileMenu.classList.toggle('hidden');
    });
  
    // Close the dropdown menu when clicking outside of it
    document.addEventListener('click', function(event) {
      if (!userProfileButton.contains(event.target) && !userProfileMenu.contains(event.target)) {
        userProfileMenu.classList.add('hidden');
      }
    });
  });
  