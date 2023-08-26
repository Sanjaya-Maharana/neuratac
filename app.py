from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
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

if __name__ == '__main__':
    # Use the environment variable for the port if available, or fallback to 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
