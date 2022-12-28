from flask import Flask, render_template, request

app = Flask(__name__)

database={'sanjay':'123','ram':'532312'}

@app.route("/")
def template():
    return render_template('template.html')


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/submit",methods=['POST','GET'])
def login_val():
    name1 = request.form['username']
    psw = request.form['password']
    if name1 not in database:
        return render_template(login.html,info='Invalid User')
    else:
        if name1 not in database:
            return render_template('login.html',info="Invalid Password")
        else:
            return render_template('home.html',name=name1)


@app.route("/register")
def signup():
    return render_template('register.html')
@app.route("/forgot")
def forgot():
    return render_template('forgot.html') 
@app.route("/terms")
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(port=8000)
