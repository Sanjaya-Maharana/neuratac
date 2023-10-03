from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime



app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# Configure your email settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'apirequest2000@gmail.com'
sender_password = 'rcfyvrzrugdlfmup'

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscribers.db'
db = SQLAlchemy(app)

# Define a Subscriber model for the database
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_submissions.db'  # Use SQLite as an example
db = SQLAlchemy(app)

class FormSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(25))
    phno = db.Column(db.String(15))
    message = db.Column(db.Text)
    visitor_ip = db.Column(db.String(45))
    location_info = db.Column(db.String(50))
    time_stamp = db.Column(db.String(25))

    def __init__(self, name, email, phno, message, visitor_ip, location_info, time_stamp):
        self.name = name
        self.email = email
        self.phno = phno
        self.message = message
        self.visitor_ip = visitor_ip
        self.location_info = location_info
        self.time_stamp = time_stamp


def send_email(receiver_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print('Error sending email:', str(e))
        return False


def get_location_info(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url)
        data = response.json()  # Parse the JSON response
        print(data)  # Print the entire JSON response (for debugging)
        location_info = f"{data['city']}, {data['region']}, {data['country']}"
        return location_info
    except Exception as e:
        print('Error fetching location:', str(e))
        return 'Location information not available'


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

    # Check if the email is not already in the database
    if not Subscriber.query.filter_by(email=receiver_email).first():
        new_subscriber = Subscriber(email=receiver_email)
        db.session.add(new_subscriber)
        db.session.commit()

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

        if send_email(receiver_email, subject, email_content):
            message = "Subscribed successfully"
        else:
            message = "Error sending Subscription"
    else:
        message = "Email already subscribed"

    return render_template('index.html', message=message)

@app.route("/subscribers")
def subscriber_list():
    # Retrieve the list of subscribers from the database
    subscribers = Subscriber.query.all()

    return render_template('subscribers.html', subscribers=subscribers)

@app.route('/form_data')
def form_data():
    # Fetch all form submissions from the database
    form_submissions = FormSubmission.query.all()

    return render_template('form_data.html', form_submissions=form_submissions)


@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phno = request.form['phno']
        message = request.form['message']

        # Get the visitor's IP address
        visitor_ip = request.remote_addr

        # Get the visitor's location based on the IP address using ipinfo.io
        location_info = get_location_info(visitor_ip)

        # Generate a timestamp
        time_stamp = datetime.now()

        # Create a new FormSubmission object and save it to the database
        form_submission = FormSubmission(name, email, phno, message, visitor_ip, location_info, time_stamp)
        db.session.add(form_submission)
        db.session.commit()

        return render_template('contact.html', message="Form submitted and data saved to the database")

    return render_template('contact.html')


if __name__ == '__main__':
    with app.app_context():
        # Create the database tables
        db.create_all()
    # Use the environment variable for the port if available, or fallback to 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True,host='0.0.0.0', port=port)


