
document.addEventListener('DOMContentLoaded', function() {
    var recipe_button = document.getElementById('add-recipe-button');
    recipe_button.addEventListener('click', function() {
        var form = document.getElementById('recipe-form');
        if (form.style.display === 'none') {
            form.style.display = 'block';  // Show the form
            recipe_button.textContent = 'Close Menu'

        } else {
            form.style.display = 'none';   // Hide the form
            recipe_button.textContent = 'Add Recipe'
        }
    });
});

