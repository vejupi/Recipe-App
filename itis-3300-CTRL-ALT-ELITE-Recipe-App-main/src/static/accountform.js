document.addEventListener('DOMContentLoaded', () =>{
    const signupButton = document.getElementById('signupButton');
    const signupForm = document.getElementById('signupForm');
    const accountForm = document.getElementById('accountForm');
    const profilePage = document.getElementById('profilePage');
    const profileUsername = document.getElementById('profileUsername');
    const profileEmail = document.getElementById('profileEmail');

    signupButton.addEventListener('click', () => {
        signupForm.style.display = 'block';
        signupButton.style.display = 'none';
        
        
    });

    accountForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;

        profileUsername.textContent = username;
        profileEmail.textContent = email;

        signupForm.style.display = 'none';
        profilePage.style.display = 'block';
        console.log("Signup Form Display Style:", profilePage.style.display);

});
});