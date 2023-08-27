from flask import Flask, render_template, request, redirect
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)

# Configure your email settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'apirequest2000@gmail.com'
sender_password = 'rcfyvrzrugdlfmup'

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

app.debug = True

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
    email_content = '''Dear Subscriber,

Thank you for subscribing to our newsletter! We are thrilled to have you as part of our community. You will now receive regular updates, news, and special offers delivered directly to your inbox.

Here's what you can expect from our newsletter:

1. Latest Updates: Stay up-to-date with the latest news, trends, and developments in our industry.
2. Exclusive Offers: Get access to exclusive discounts and promotions that are only available to our subscribers.
3. Helpful Tips: Receive valuable tips, insights, and resources to help you make the most of our products/services.

If you ever have any questions or feedback, please don't hesitate to reach out to us. We value your input and are here to assist you.

Once again, thank you for subscribing. We look forward to sharing exciting content with you!

Best regards,
Neuratac - Innovation AI Solution'''
    owner_email = 'SanjayaMaharana145@gmail.com'  # Change to your own email address
    subject = 'Thank you for subscribing to our newsletter'

    if send_email(receiver_email, subject, email_content):
        message = "Subscribed successfully"
    else:
        message = "Error sending Subscription"
    return render_template('index.html', message=message)



@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phno = request.form['phno']
        message = request.form['message']

        # Modify the email content as needed
        email_content = f"Name: {name}\nEmail: {email}\nPhone Number: {phno}\nMessage: {message}"

        receiver_email = 'SanjayaMaharana145@gmail.com'  # Change to your own email address
        subject = 'New Form Submission'

        if send_email(receiver_email, subject, email_content):
            message = "Email sent successfully"
        else:
            message = "Error sending email"
        return render_template('contact.html', message=message)

if __name__ == '__main__':
    # Use the environment variable for the port if available, or fallback to 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
