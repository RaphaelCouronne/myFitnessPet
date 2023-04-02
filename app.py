import sqlite3
from flask import Flask, jsonify, request
from flask import url_for
from flask import render_template
from datetime import datetime

app = Flask(__name__)
DATABASE = 'pet_database.db'



def get_all_pets():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("SELECT DISTINCT name FROM pets")
    pet_names = [row[0] for row in c.fetchall()]

    conn.close()

    return pet_names


@app.route('/')
def home():


    pets = get_all_pets()  # Fetch pet names from the database

    pet_cards = ""
    for pet in pets:
        pet_card = f'''
            <div style="border: 1px solid black; padding: 10px; margin-bottom: 10px;">
                <h3>{pet}</h3>
                
                
                <a href="{ url_for('pet_page', name=pet) }">
                    <img src={ url_for('static', filename='data/dog.jpeg') }>
                </a>
                

                
                
            </div>
            
            
            
            


            
        '''
        pet_cards += pet_card

    # Rest of the home function remains the same


    return f'''
        <html>
        <head>
            <title>Pet Nutrition and Weight Tracker</title>
            <script>
                function submitWeightForm(event, petName) {{
                    event.preventDefault();
                    var weight = document.getElementById("weight-" + petName).value;
                    var date = document.getElementById("date-" + petName).value;

                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/api/pet/" + petName + "/weight", true);
                    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                    xhr.send(JSON.stringify({{ weight: weight, date: date }}));

                    xhr.onload = function () {{
                        if (xhr.status == 200) {{
                            alert("Weight log added successfully for " + petName);
                        }} else {{
                            alert("Error adding weight log for " + petName);
                        }}
                    }};
                }}
            </script>
        </head>
        <body>
            <h1>Pet Nutrition and Weight Tracker</h1>
            {pet_cards}
            

            <form action="/api/pet" method="POST">
                <label for="pet-name">Pet Name:</label>
                <input type="text" id="pet-name" name="pet_name">
                <input type="submit" value="Add new Pet">
            </form>
            
        </body>
        </html>
    '''



@app.route('/pet/<name>')
def pet_page(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Retrieve nutrition and weight logs from database
    c.execute("SELECT * FROM nutrition_log WHERE pet_name=?", (name,))
    nutrition_logs = c.fetchall()
    c.execute("SELECT * FROM weight_log WHERE pet_name=?", (name,))
    weight_logs = c.fetchall()

    # Format weight data for the chart
    weight_data = [log[2] for log in weight_logs]
    weight_dates = [log[1] for log in weight_logs]

    # Extract nutrition data and corresponding dates
    nutrition_data = [log[2] for log in nutrition_logs]
    nutrition_dates = [log[1] for log in nutrition_logs]

    # Close database connection
    conn.close()

    # Render the pet page template with the retrieved data
    return render_template('pet_page.html', pet_name=name, nutrition_logs=nutrition_logs, weight_logs=weight_logs,
                           weight_data=weight_data, weight_dates=weight_dates,
                           nutrition_data=nutrition_data, nutrition_dates=nutrition_dates)



@app.route('/api/pet', methods=['POST'])
def add_pet():
    pet_name = request.form.get("pet_name")

    if pet_name:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # Check if the pet already exists
        c.execute("SELECT * FROM pets WHERE name=?", (pet_name,))
        existing_pet = c.fetchone()

        if existing_pet is None:
            # Add the pet to the database
            c.execute("INSERT INTO pets (name) VALUES (?)", (pet_name,))
            conn.commit()
            conn.close()

            return jsonify({'message': f'Pet {pet_name} added successfully'})
        else:
            conn.close()
            return jsonify({'message': f'Pet {pet_name} already exists'}), 400
    else:
        return jsonify({'message': 'Pet name is required'}), 400



@app.route('/api/pet/<name>')
def get_pet_data(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Retrieve pet data from database
    # c.execute("SELECT * FROM pets WHERE name=?", (name,))
    # pet_data = c.fetchone()

    # Retrieve nutrition and weight logs from database
    c.execute("SELECT * FROM nutrition_log WHERE pet_name=?", (name,))
    nutrition_logs = c.fetchall()
    c.execute("SELECT * FROM weight_log WHERE pet_name=?", (name,))
    weight_logs = c.fetchall()

    # Close database connection
    conn.close()

    # Return data as JSON
    return jsonify({
        # 'pet_data': pet_data,
        'nutrition_logs': nutrition_logs,
        'weight_logs': weight_logs
    })

@app.route('/api/pet/<name>/nutrition', methods=['POST'])
def log_nutrition(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Add new nutrition log to database
    if 'nutrition' in request.json and 'date' in request.json:
        nutrition = request.json['nutrition']
        date = request.json['date']
        c.execute("INSERT INTO nutrition_log VALUES (?, ?, ?)", (name, date, nutrition))
        conn.commit()

    # Close database connection
    conn.close()

    # Return success message as JSON
    return jsonify({'message': 'Nutrition log added successfully'})

@app.route('/api/pet/<name>/weight', methods=['POST'])
def log_weight(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Add new weight log to database
    if 'weight' in request.json and 'date' in request.json:
        weight = request.json['weight']
        date = request.json['date']
        c.execute("INSERT INTO weight_log VALUES (?, ?, ?)", (name, date, weight))
        conn.commit()

    # Close database connection
    conn.close()

    # Return success message as JSON
    return jsonify({'message': 'Weight log added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
