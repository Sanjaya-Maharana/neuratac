from flask import Flask, render_template, request, redirect, url_for
import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Configure your email settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'apirequest2000@gmail.com'
sender_password = 'rcfyvrzrugdlfmup'

# Initialize SQLite database
db_path = 'myapp.db'

def create_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriber (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS form_submission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phno TEXT,
            message TEXT,
            visitor_ip TEXT,
            location_info TEXT,
            time_stamp TEXT
        )
    ''')
    conn.commit()
    conn.close()



create_database()



# def send_email(receiver_email, subject, message):
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(message, 'plain'))
#
#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())
#         server.quit()
#         return True
#     except Exception as e:
#         print('Error sending email:', str(e))
#         return False

# def get_location_info(ip):
#     try:
#         url = f"https://ipinfo.io/{ip}/json"
#         response = requests.get(url)
#         data = response.json()
#         location_info = f"{data['city']}, {data['region']}, {data['country']}"
#         return location_info
#     except Exception as e:
#         print('Error fetching location:', str(e))
#         return 'Location information not available'

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about-us")
def about():
    return render_template('about-us.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/gallery")
def gallery():
    return render_template('gallery.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    receiver_email = request.form.get('email')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the email is not already in the database
    cursor.execute("SELECT * FROM subscriber WHERE email=?", (receiver_email,))
    existing_email = cursor.fetchone()

    if not existing_email:
        cursor.execute("INSERT INTO subscriber (email) VALUES (?)", (receiver_email,))
        conn.commit()
        conn.close()

        email_content = '''Dear Subscriber,

        Thank you for subscribing to our newsletter! We are thrilled to have you as part of our community. You will now receive regular updates, news, and special offers delivered directly to your inbox.

        Here's what you can expect from our newsletter:

        1. Latest Updates: Stay up-to-date with the latest news, trends, and developments in our industry.
        2. Exclusive Offers: Get access to exclusive discounts and promotions that are only available to our subscribers.
        3. Helpful Tips: Receive valuable tips, insights, and resources to help you make the most of our products/services.

        If you ever have any questions or feedback, please don't hesitate to reach out to us. We value your input and are here to assist you.

        Once again, thank you for subscribing. We look forward to sharing exciting content with you!

        Best regards,
        Neuratac - Innovation AI Solution
        SanjayaMaharana145@gmail.com
        '''
        subject = 'Thank you for subscribing to our newsletter'

        # if send_email(receiver_email, subject, email_content):
        #     message = "Subscribed successfully"
        # else:
        #     message = "Error sending Subscription"
        message = "Subscribed successfully"
    else:
        message = "Email already subscribed"

    return render_template('index.html', message=message)

@app.route("/subscribers")
def subscriber_list():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM subscriber")
    subscribers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template('subscribers.html', subscribers=subscribers)

@app.route('/form_data')
def form_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM form_submission")
    form_submissions = cursor.fetchall()
    conn.close()
    return render_template('form_data.html', form_submissions=form_submissions)

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phno = request.form['phno']
        message = request.form['message']

        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO form_submission (name, email, phno, message, time_stamp) VALUES (?, ?, ?, ?, ?)",
                       (name, email, phno, message, time_stamp))
        conn.commit()
        conn.close()

        return render_template('contact.html', message="Form submitted and data saved to the database")

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
