import sqlite3

class Pet:
    def __init__(self, name, species, age, weight):
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight
        self.nutrition_log = []
        self.weight_log = []
        self.conn = sqlite3.connect('../pet_database.db')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS nutrition_log
                     (pet_name text, date text, nutrition_info text)''')

        # Create weight log table
        self.c.execute('''CREATE TABLE IF NOT EXISTS weight_log
                     (pet_name text, date text, weight integer)''')

        # Create name table
        self.c.execute('''CREATE TABLE IF NOT EXISTS pets
                     (name text)''')



    def __del__(self):
        self.conn.close()

    def log_nutrition(self, nutrition_info):
        self.nutrition_log.append(nutrition_info)
        date = nutrition_info['date']
        nutrition = nutrition_info['nutrition']
        self.c.execute("INSERT INTO nutrition_log VALUES (?, ?, ?)",
                       (self.name, date, nutrition))
        self.conn.commit()

    def log_weight(self, weight_info):
        self.weight_log.append(weight_info)
        date = weight_info['date']
        weight = weight_info['weight']
        self.c.execute("INSERT INTO weight_log VALUES (?, ?, ?)",
                       (self.name, date, weight))
        self.weight = weight
        self.conn.commit()

    def get_nutrition_log(self):
        self.c.execute("SELECT * FROM nutrition_log WHERE pet_name=?",
                       (self.name,))
        return self.c.fetchall()

    def get_weight_log(self):
        self.c.execute("SELECT * FROM weight_log WHERE pet_name=?",
                       (self.name,))
        return self.c.fetchall()

    def get_current_weight(self):
        return self.weight



class Cat(Pet):
    def __init__(self, name, age, weight):
        super.__init__(name, "cat", age, weight)


def compute_daily_calories(pet):
    # Compute base metabolic rate (BMR) using Harris-Benedict equation
    if pet.species == 'dog':
        if pet.weight < 9:
            bmr = (22 * pet.weight) + 95
        elif pet.weight < 23:
            bmr = (30 * pet.weight) + 70
        elif pet.weight < 55:
            bmr = (50 * pet.weight) + 10
        else:
            bmr = (30 * pet.weight) + 80
    elif pet.species == 'cat':
        bmr = (30 * pet.weight) + 70

    # Adjust BMR based on activity level
    if pet.activity_level == 'sedentary':
        calories = bmr * 1.2
    elif pet.activity_level == 'lightly active':
        calories = bmr * 1.375
    elif pet.activity_level == 'moderately active':
        calories = bmr * 1.55
    elif pet.activity_level == 'very active':
        calories = bmr * 1.725
    else:
        calories = bmr * 1.9

    return bmr, calories


class Meal:
    def __init__(self, type, quantity, time):
        self.type = type # produit
        self.quantity = quantity # kcal
        self.time = time # date / heure


pet1 = Pet('Max', 'dog', 5, 20)
pet1.log_weight({"weight": 10, "date": "2023-12-04"})
pet1.log_nutrition({"nutrition": "croquetas", "date": "2023-12-04"})


pet2 = Pet('George', 'cat', 4, 10)
pet2.log_weight({"weight": 5, "date": "2023-12-04"})
pet2.log_nutrition({"nutrition": "patée", "date": "2023-12-04"})



"""
while True:
    action = input('What would you like to do? (log nutrition, log weight, get nutrition log, get weight log, get current weight) ')

    if action == 'log nutrition':
        nutrition_info = input('Please enter the nutrition information: ')
        pet1.log_nutrition(nutrition_info)
        print('Nutrition information logged for ' + pet1.name)

    elif action == 'log weight':
        weight_info = {}
        weight_info['weight'] = int(input('Please enter the weight: '))
        weight_info['date'] = input('Please enter the date (yyyy-mm-dd): ')
        pet1.log_weight(weight_info)
        print('Weight information logged for ' + pet1.name)

    elif action == 'get nutrition log':
        print(pet1.get_nutrition_log())

    elif action == 'get weight log':
        print(pet1.get_weight_log())

    elif action == 'get current weight':
        print(pet1.get_current_weight())

    else:
        print('Invalid input, please try again.')
"""
