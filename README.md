# FeMaNomNom
#### Video Demo:  <https://youtu.be/-MT5M3EoRMc>

#### Problem:
My Girlfriend and I, we love to cook. However, there often is pulled the same question: What do we want to cook today.
There are so many recipes we have already cooked, but do not remember. Or even if we do remember, we can't find them back.
We tried do create an MS Word based recipe book, but that wasn't quite effective. When I tended to finish the CS50X course I thought this is the ideal opportunity to solve our Problem. I going to create a web app to run it locally and use it in our network.

#### Description:
FeMaNomNom is a web application to manage cooking recipies in.
Therefore you can view, add and edit recipies in an SQLite Database via a web based frontend.

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
