from flask import Flask, render_template, redirect, request, url_for, flash
import sqlite3


#Create the database
conn = sqlite3.connect('sacc_alumni_database.db')

#Create a cursor object to interact with the database 
cursor = conn.cursor()


#Create the alumni table

cursor.execute( '''
CREATE TABLE IF NOT EXISTS alumni(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               firstname TEXT NOT NULL,
               middlename TEXT,
               lastname TEXT NOT NULL,
               gender TEXT,
               phone_number TEXT,
               email TEXT,
               year_of_entry INTEER,
               year_of_completion INTEGER,
               programme TEXT,
               qualification TEXT,
               occupation TEXT,
               institution TEXT,
               residence TEXT,
               sacraments TEXT,
               society TEXT
               )

''')

#commit changes
conn.commit()








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
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        entry = request.form['entry']
        completion = request.form['completion']
        programme = request.form['programme']
        qualification = request.form['qualification']
        occupation = request.form['occupation']
        institution = request.form['institution']
        residence = request.form['residence']
        sacraments = ', '.join(request.form.getlist('sacraments'))
        society = request.form.getlist('society')


        # Add the custom 'Other' input if it's provided
        other_society = request.form.get('other_society')
        if other_society:
            society.append(other_society)

        # Join selected options into a comma-separated string
        society_str = ', '.join(society)

        # Validate form fields
        if not (firstname and lastname and  gender and residence and completion and occupation and phone and sacraments and society):
            flash('Kindly Fill All Fields')
            return redirect(url_for('index'))
        

        #insert data into database

        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alumni (firstname, middlename, lastname, gender, phone_number, email, 
                       year_of_entry, year_of_completion, programme, qualification, occupation,
                       institution, residence, sacraments, society)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
       ''',     (firstname, middlename, lastname, gender, phone, email, entry, completion, 
                 programme, qualification, occupation, institution, residence, sacraments, society_str))
        conn.commit()
        conn.close()

        flash('Details Successfully Submitted\nThank You :)')
        return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)