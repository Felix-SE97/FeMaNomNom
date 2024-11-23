# FeMaNomNom
#### Video Demo:  <https://youtu.be/-MT5M3EoRMc>

#### Problem:
My girlfriend and I love to cook. However, the same question often arises: What do we want to cook today? 
There are so many recipes we have already cooked but don't remember. Even if we do remember, we can't find 
them. We tried to create an MS Word-based recipe book, but that wasn't very effective. When I was finishing 
the CS50X course, I thought this was the ideal opportunity to solve our problem. I decided to create a web 
app to run locally and use in our network.

#### Description:
FeMaNomNom is a web application for managing cooking recipes. You can view, add, and edit recipes in an 
SQLite database via a web-based frontend.

### What I have done, but is not that obvious:
- All pictures are selfmade:
- Logo: gimp + dutyfree vectors from pixabay
- icons: inkscape + dutyfree vectors from pixabay
- foodpictures: All foodpictures are taken with my smartphone camera.

#### How to use:
* create virtual environment
* activate the environment
* pip install flask
* pip install cs50
* copy following folders into the folder where you created the environment:
* flask_session, __pycache__, static, template
* Also copy following file in the same fodler:
* app.py, helpers.py, Nutzdaten.db
* You now can start the app.

#### Future ideas:
[ ] Edit uploaded recipes
[ ] delete recipes
[ ] choose random recipe button
[ ] ranking system based on the amount of added to the favourites

#### file structure:
-**/static**
    - images: This is the folder where the pictures are uploaded to.
    - src: This is the folder where all this logos/icons are in.
    - style.css: This is the css file describing the layout for the whole project.

-**templates**
    - vorlagen: folder with backup-files of preveous versions
    - layout.html: HTML-core. This file is the "mother" of all other HTML-documents
    - index.html: HTML-Block for the "Home"-page.
    - index_ohne.html: HTML-Block used for the "My Recipies"-Page. Compared to index.html there is no filter function on this page
    - rezept.html: HTML-Block used for the "Show Recipe"-Pages.
    - addRecipe.html: HTML-Block used for the "Add Recipe"-Page. It includes the form to describe the recipe
    - addRecipe_editIngri.html: HTML-Block used for the "edit ingredient"-function. "Same" as the addRecipe.html, but with two div set to absolute to set them in the foreground
    - addRecipe_editPrep.html: HTML-Block used for the "edit preparation"-function. "Same" as the addRecipe.html, but with two div set to absolute to set them in the foreground
    - login.html: HTML-Block used for "Login"-Page
    - register.html: HTML-Block used for the Registration which is accessed through the "Login"-Page
    - apology.html: HTML-Block used to show Errors (e.g.: "No username was submitted",  "No password was submitted", "invalid username and/or password", "Confirmation doesn't match password...", "Username is already taken!" )

#### Language, frameworks and other components used:
- Python / flask / cs50
- Jinja
- SQLite3
- JavaScript
- HTML
- CSS
- Bootstrap (but only to use their icons)
- font-awesome
- Google Fonts

#### Contact:
In case you would like to contact me, please use the enbedded social media links inside the project.
