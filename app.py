from flask import Flask, render_template, request, redirect
import os


app = Flask(__name__)
app.debug = True


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contact_us")
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
    # Use the environment variable for the port if available, or fallback to 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

