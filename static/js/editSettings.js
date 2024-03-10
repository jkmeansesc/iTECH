// Get the edit button element
var editButton = document.querySelector('.btn.btn-primary.btn-outline.pull-right.edit-username-btn');

// Add click event listener
editButton.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default behavior, i.e., do not navigate to the href specified in the link

    // Hide the original edit button
    editButton.style.display = 'none';

    // Get the username element
    var usernameElement = document.getElementById('elem-username');
    // Get the form element
    var formElement = document.getElementById('change-username');

    // Show the username input box and set the username as its value
    usernameElement.style.display = 'none';
    formElement.style.display = 'block';
});

// Get the cancel button element
var cancelButton = document.querySelector('button[data-dismiss="form"].edit-username-btn');

// Add click event listener
cancelButton.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default behavior

    // Get the edit button element
    var editButton = document.querySelector('.btn.btn-primary.btn-outline.pull-right.edit-username-btn');
    // Get the username element
    var usernameElement = document.getElementById('elem-username');
    // Get the form element
    var formElement = document.getElementById('change-username');

    // Show the original edit button and hide the username input box
    editButton.style.display = 'inline-block';
    usernameElement.style.display = 'block';
    formElement.style.display = 'none';
});


// Get the edit email button element
var editEmailButton = document.querySelector('.btn.btn-primary.btn-outline.pull-right.edit-email-btn');

// Add click event listener
editEmailButton.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default behavior, i.e., do not navigate to the href specified in the link

    // Hide the original edit button
    editEmailButton.style.display = 'none';

    // Get the email element
    var emailElement = document.getElementById('elem-email');
    // Get the form element
    var formElement = document.getElementById('change-email');

    // Show the email input box and set the email as its value
    emailElement.style.display = 'none';
    formElement.style.display = 'block';
});

// Get the cancel button element
var cancelEmailButton = document.querySelector('button[data-dismiss="form"].edit-email-btn');

// Add click event listener
cancelEmailButton.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default behavior

    // Get the edit button element
    var editEmailButton = document.querySelector('.btn.btn-primary.btn-outline.pull-right.edit-email-btn');
    // Get the username element
    var emailElement = document.getElementById('elem-email');
    // Get the form element
    var formElement = document.getElementById('change-email');

    // Show the original edit button and hide the eamil input box
    editEmailButton.style.display = 'inline-block';
    emailElement.style.display = 'block';
    formElement.style.display = 'none';
});

// Get the edit password button element
var editPwdButton = document.querySelector('.btn.btn-primary.btn-outline.pull-right.edit-pwd-btn');

// Add click event listener
editPwdButton.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default behavior, i.e., do not navigate to the href specified in the link

    // Hide the original edit password button
    editPwdButton.style.display = 'none';

    // Get the password change form element
    var pwdForm = document.getElementById('change-pwd');

    // Show the password change form
    pwdForm.style.display = 'block';
});

// Get the cancel button element
var cancelPwdButton = document.querySelector('button[data-dismiss="form"].edit-pwd-btn');

// Add click event listener
cancelPwdButton.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default behavior

    // Show the original edit password button
    editPwdButton.style.display = 'inline-block';

    // Get the password change form element
    var pwdForm = document.getElementById('change-pwd');

    // Hide the password change form
    pwdForm.style.display = 'none';
});

