from flask import Flask, render_template, redirect, request, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'st_augustine_pray_for_us'


# Function to connect to the database
def connect_database():
    return sqlite3.connect('sacc_alumni_database.db')

# Route for the form page
@app.route('/')
def index():
    return render_template('form.html')

#Route to handle form submission
@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        sex = request.form['sex']
        location = request.form['location']
        year = request.form['year']
        occupation = request.form['occupation']
        phone = request.form['phone']
        email = request.form['email']
        society = request.form['society']


        # Validate form fields
        if not (firstname and lastname and age and sex and location and year and occupation and phone and email):
            flash('Kindly Fill All Fields But SOCIETY is Optional')
            return redirect(url_for('index'))
        

        #insert data into database

        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alumni (firstname, lastname, age, sex, location, year_of_completion, occupation, phone_number, email, society)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
       ''',     (firstname, lastname, age, sex, location, year, occupation, phone, email, society))
        conn.commit()
        conn.close()

        flash('Details Successfully Submitted\nThank You :)')
        return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)