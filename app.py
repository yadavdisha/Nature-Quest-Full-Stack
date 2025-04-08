from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import sqlite3
import base64
import requests
import secrets
from werkzeug.security import generate_password_hash
import random
import string
from flask import session
import json
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'ui_secret_2024'  # Set a secret key for flash messages


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# Your Gmail email address
app.config['MAIL_USERNAME'] = 'uiproject2024@gmail.com'
# Your Gmail password or App Password
app.config['MAIL_PASSWORD'] = 'ofdh pkvc tonk slco'

mail = Mail(app)

# Absolute path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'uiflasknew2.db')


def create_table_user():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        fullName TEXT, 
                        username TEXT UNIQUE, 
                        email TEXT UNIQUE, 
                        phoneNumber TEXT,
                        password TEXT,
                        trip TEXT,
                        trip_date TEXT,
                        contribution TEXT,
                        wishlist TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS password_reset (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                otp TEXT)''')

        print("Database connected successfully.")

# Function to create database table if it doesn't exist


def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, 
                    email TEXT, 
                    datetime TEXT, 
                    location TEXT, 
                    story TEXT, 
                    image BLOB)''')
    c.execute('''CREATE TABLE IF NOT EXISTS notify (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    recipient  TEXT, 
                    body  TEXT, 
                    username TEXT)''')
    conn.commit()
    conn.close()
    print("Database connected successfully.")

# Route for the homepage


@app.route('/')
def index():
    return render_template('index.html')

# Route for the about page


@app.route('/about')
def about():
    return render_template('about.html', login_success=True)

@app.route('/faq')
def faq():
    return render_template('faq.html', login_success=True)


@app.route('/home')
def home():
    return render_template('index.html', login_success=True)


@app.route('/loginpage')
def loginpage():
    return render_template('login.html', login_success=True)

# Route for the booking page


@app.route('/trippage2')
def trippage2():
    return render_template('trippage2.html',login_success=True)


@app.route('/trippage3')
def trippage3():
    return render_template('trippage3.html',login_success=True)


@app.route('/trippage4')
def trippage4():
    return render_template('trippage4.html',login_success=True)


@app.route('/trippage5')
def trippage5():
    return render_template('tripnextpage.html', login_success=True)

# Route for the contact page


@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the destination page


@app.route('/destination')
def destination():
    return render_template('destination.html')

# Route for the package page


@app.route('/package')
def package():
    return render_template('package.html',login_success=True)

# Route for the service page

@app.route('/hiking')
def hiking():
    return render_template('hiking.html',login_success=True)

@app.route('/beachclean')
def beach():
    return render_template('beachclean.html',login_success=True)

@app.route('/join')
def join():
    return render_template('join.html',login_success=True)


@app.route('/join2')
def join2():
    return render_template('join2.html',login_success=True)


@app.route('/service')
def service():
    return render_template('service.html')


@app.route('/full-story')
def fullstory():
    return render_template('full-story.html', login_success=True)


@app.route('/sample-story')
def samplestory():
    return render_template('sample-story1.html', login_success=True)


@app.route('/sample-story1')
def samplestory1():
    return render_template('sample-story2.html', login_success=True)


@app.route('/sample-story2')
def samplestory2():
    return render_template('sample-story3.html', login_success=True)


@app.route('/bot')
def chatbot():
    return render_template('bot.html')


@app.get("/bot1")
def index_get():
    return render_template("bot1.html")

@app.get("/marketplace")
def marketplace():
    return render_template("marketplace.html",  login_success=True)

@app.route('/noti')
def noti():
    category = request.args.get('category')  # Get the category parameter from the URL
    return render_template('noti.html', login_success=True)


@app.get("/product")

def product():
    if 'username' in session:
        return render_template("product.html", username=session['username'], email=session['email'], login_success=True)
    else:
        return render_template("product.html", login_success=False)


def date_function():
    current_datetime = datetime.now()
    return current_datetime

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    sender = data['sender']
    recipient = data['recipient']
    message_body = data['message']

    datetime  = date_function()

    if 'username' in session:
        # Fetch user details from the database based on the logged-in user
        username = session['username']

        subject = f"Naturequest: {username} sent a message"

        msg = Message(subject, sender=sender, recipients=[recipient])
        msg.body = message_body
        mail.send(msg)

    

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO notify (recipient, body, username) VALUES (?, ?, ?)",
                        (recipient, message_body, username))
        conn.commit()
    
        conn.close()
        try:
            mail.send(msg)
            return jsonify({'message': 'Email sent successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    else:
      
        return jsonify({'message': 'kindly login '}), 200



@app.route('/get-notifications', methods=['GET'])

def getnotifications():

        if 'username' in session:
            # Fetch user details from the database based on the logged-in user
        
            email = session['email']

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id, username, body FROM notify WHERE recipient = ? ORDER BY id DESC", (email,))

            entries = c.fetchall()
            conn.close()

            if entries:
                    # story, name, datetime,image_base64 = story_data
                return jsonify(entries)
            else:
                return jsonify([])
        else:
            return jsonify([])

    




# Route for the stories page
@app.route('/stories', methods=['GET', 'POST'])
def stories():
    if request.method == 'POST':
        try:
            # Retrieve form data
            name = request.form['name']
            email = request.form['email']
            datetime = request.form['datetime']
            location = request.form['location']
            story = request.form['story']

            # Check if the request contains the file part
            if 'image' in request.files:
                file = request.files['image'].read()

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO stories (name, email, datetime, location, story, image) VALUES (?, ?, ?, ?, ?, ?)",
                      (name, email, datetime, location, story, (sqlite3.Binary(file))))
            conn.commit()

            print('Data inserted into the database successfully.')

            c.execute(
                "SELECT id,name,email,datetime,location,story,image FROM stories ORDER BY id DESC ")
            entries = c.fetchall()
            conn.close()

            entries_dict = []
            for entry in entries:
                entry_dict = {
                    'id': entry[0],
                    'name': entry[1] if len(entry) > 0 else None,
                    'email': entry[2] if len(entry) > 0 else None,
                    'datetime': entry[3] if len(entry) > 0 else None,
                    'location': entry[4] if len(entry) > 0 else None,
                    'story': entry[5] if len(entry) > 0 else None,
                    'image': base64.b64encode(entry[6]).decode('utf-8') if entry[6] else None
                }
                entries_dict.append(entry_dict)

            if entries:
                # story, name, datetime,image_base64 = story_data
                return render_template('stories.html',  entries=entries_dict, login_success=True)
            else:
                return render_template('stories.html', story_text=None, author_name=None, datetime=None,login_success=True)

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            print(f'Database Error: {str(e)}')
            return redirect(url_for('stories'))
    else:

        return render_template('stories.html', login_success=True)


@app.route('/full-story/<int:story_id>')
def view_story(story_id):

    story = get_story_by_id(story_id)
    if story:
        return render_template('full-story.html', story=story)
    else:
        return render_template('story-not-found.html')
    
def get_story_by_id(story_id):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM stories WHERE id = ?", (story_id,))
    fullstory = c.fetchone()
    conn.close()

    if fullstory:
         
            story_data = {
                'id': fullstory[0],
                'name': fullstory[1],
                'email': fullstory[2],
                'datetime': fullstory[3],
                'location': fullstory[4],
                'story': fullstory[5],
                'image_base64': base64.b64encode(fullstory[6]).decode('utf-8') if fullstory[6] else None
            }
    return story_data





@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_message = data['message']


    url = "https://api.openai.com/v1/chat/completions"
    max_tokens = 50
  

    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_message}],
             "max_tokens": max_tokens
          
        }

    try:
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                completion_text = result['choices'][0]['message']['content']
                return jsonify({'answer': completion_text})
            else:
                return jsonify({'error': str(e)})
    except Exception as e:
            return jsonify({'error': str(e)})

    


# Route for the team page
@app.route('/team')
def team():
    return render_template('team.html')

# Route for the testimonial page


@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

# Route for handling 404 errors


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/loginfail')
def loginfail():
    return render_template('loginfail.html')

@app.route('/signupfail')
def signupfail():
    return render_template('signupfail.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['loginusername']
        password = request.form['loginpassword']

        # Query the database for the user with the provided email
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            Q1 = "SELECT username, password, email FROM users WHERE username=?"
            c.execute(Q1, (username,))
            user = c.fetchone()

            if user and user[1] == password:
                # If user exists and password matches, set the session email and redirect to dashboard
                session['username'] = username
                session['email'] = user[2]
                flash('Login successful!', 'success')
                return render_template('index.html', login_success=True)
            else:
                # If user does not exist or password does not match, display error message
                return render_template('loginfail.html', login_success=False)

    # If method is not POST or login was unsuccessful, render the login page
    return render_template('index.html', login_success=False)


def get_user_details(username, email):
    # Establish a connection to your database
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user_details = c.fetchone()

        # Assuming 'user_id' links the tables
        c.execute("SELECT * FROM stories WHERE email=?", (email,))
        story_table_details = c.fetchone()

    # Close the database connection
    conn.close()

    return user_details, story_table_details


@app.route('/profile')
def profile():
    # Check if user is logged in
    if 'username' in session:
        # Fetch user details from the database based on the logged-in user
        username = session['username']
        email = session['email']
        # Perform database query to fetch user details based on username
        # Replace this with your actual database query
        user_details, story_table_details = get_user_details(
            username, email)  # Implement this function

        if story_table_details is not None:
            # Assuming story_table_details[6] contains the image data
            image_data = story_table_details[6]

            # Convert the image data to base64 encoding
            base64_encoded_image = base64.b64encode(image_data).decode('utf-8')

        if user_details and story_table_details:
            # Render the profile.html template and pass the user details to it
            return render_template('profile.html', user=user_details, story=base64_encoded_image, login_success=True)
        else:
            # Handle case where user details are not found
            return render_template('profile.html', user=user_details, login_success=True)
    else:
        # Redirect to login page if user is not logged in
        return redirect(url_for('login'))

# Route for the dashboard page


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        # Get the logged-in user's email as username
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        # Redirect to login if not logged in
        return render_template('dashboard.html', login_success=False)


# Route for the forgot password page
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Generate a unique token
        otp = ''.join(random.choices(string.digits, k=6))

        # Store the token in the database
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO password_reset (email, otp) VALUES (?, ?)", (email, otp))

        # Send email with password reset instructions
        msg = Message('Password Reset OTP',
                      sender='uiproject2024@gmail.com', recipients=[email])
        msg.body = f'Your OTP for password reset is: {otp}'
        mail.send(msg)

        flash('OTP for password reset sent to your email!', 'success')
        return jsonify({'success': True, 'email': email})

    return render_template('forgot_password.html')


@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        email = request.form['email']
        otp_entered = request.form['otp']

        # Retrieve OTP from the database for the given email
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT otp FROM password_reset WHERE email = ?", (email,))
            otp_stored = c.fetchone()

        if otp_stored and otp_stored[0] == otp_entered:
            # Delete the OTP from the database
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("DELETE FROM password_reset WHERE email = ?", (email,))

            return jsonify({'success': True, 'message': 'OTP verification successful!', 'email': email})
        else:
            return jsonify({'success': False, 'error_message': 'Invalid OTP. Please try again.'})


@app.route('/reset-password', methods=['POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['newPassword']
        email = request.form['newPassPopupemail']

        # Update the password for the user with the provided email
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            # Update the password in the users table
            c.execute("UPDATE users SET password=? WHERE email=?",
                      (new_password, email))
            # Commit changes to the database
            conn.commit()

        return render_template('login.html', login_success=False)


# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            # Retrieve form data
            username = request.form['username']
            email = request.form['email']
            password = request.form['password1']

            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE email=?", (email,))
                existing_user = c.fetchone()
                if existing_user:
                      return render_template('signupfail.html',  login_success=True)
                else:
                    # Insert user data into database
                    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                              (username, email, password))
                    conn.commit()  # Commit the transaction
                    flash('User registered successfully!', 'success')
                    print('User registered successfully.')
                    return render_template('index.html', username=username, login_success=True, first_time_user=True)

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            print(f'Database Error: {str(e)}')

    return render_template('index.html', login_success=False)


@app.route('/tripnextpage')
def tripnextpage():
    return render_template('tripnextpage.html', login_success=True)


@app.route('/save-trip-details', methods=['POST'])
def save_trip_details():
    # Fetch the user's email from the session
    username = session.get('username')

    if username:
        # Retrieve trip details from the request
        trip_name = request.values.get('tripName')
        trip_date = request.values.get('date')

        # Update trip name and trip date in the users table
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''UPDATE users 
                         SET trip = ?, trip_date = ?
                         WHERE username = ?''', (trip_name, trip_date, username))
            conn.commit()

    

        return render_template('tripnextpage.html', success=True)
    else:
        # Return a 400 status code for bad request
       
       return render_template('tripnextpage.html', success=False)


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page
    return render_template('index.html')


if __name__ == '__main__':
    create_table()
    create_table_user()
    app.run(debug=True)
