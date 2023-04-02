# myFitnessPet


### Requirements : 

jinja2, flask, sqlite3

### To use : 

run app.py
open in web browser

### Functionalities done

- pet have page
- log food (only kcal each meal)
- log health status
- multiple pets

### Functionalities Later

Main
- account / password
- log food better
    - scan code bar for food
    - photo for each meal (automatically recognised from pool of used meals ?)
- tips / articles
  - add section for that

Online
- database online
- user account online

Optional
- Set picture of animal
- Set BMR for animal
- Set graph for animal


Choices
- Name is assumed to be unique per animal

### Random



    <form onsubmit="submitWeightForm(event, '{pet}')">
        <label for="weight-{pet}">Weight:</label>
        <input type="text" id="weight-{pet}" name="weight"><br>
        <label for="date-{pet}">Date:</label>
        <input type="text" id="date-{pet}" name="date"><br>
        <input type="submit" value="Submit">
    </form>