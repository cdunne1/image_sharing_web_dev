import os
from werkzeug.utils import secure_filename
import login as l
import flask
from flask import request

app	= flask.Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.getcwd() + "\\static\\photos\\")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods =['GET', 'POST'])
def	index():
    if "username" in flask.session:                                     #want to see whether someone has logged in and in a session
        return flask.render_template("profile.html", name=flask.session['username'],  gallery = l.render_Gallery())
    if flask.request.method ==	'POST':
        if "hiddenelement" in flask.request.form:
            return flask.render_template("templates.html")              #brings you to log in page
        else:
            username = flask.request.form['username']
            password = flask.request.form['password']            # create a dictionary to allow multiple folk login; key is username, value is password
            if username in credentials.keys():                  # check username exists in dict, if so, check password matches up... if so then log in
                if password == credentials[username]:           # avoid and statements as may reorder key and values, need to be of the same key value pair; hence nesting
                    flask.session['username'] = flask.request.form['username']  # create session only if logged in correctly
                    return flask.render_template("profile.html", name=username, passw=password,  gallery = l.render_Gallery())
                else:
                    return flask.render_template("templates.html")      # password doesnt match username, need to retry - best practice not to specify which has gone awry
            else:
                return flask.render_template("templates.html")         # eejits havent logged in so gettign the prompt again; username not in dictionary credentials
    else:
        #l.render_Gallery()
        return flask.render_template("landing.html", gallery = l.render_Gallery())

@app.route('/register',methods =['GET'])
def register():
    return flask.render_template('register.html')

@app.route('/login',methods =['GET'])
def login():
    return flask.render_template('login.html')

@app.route('/login_user',methods =['POST'])
def login_user():
    username = flask.request.form['username']
    password = flask.request.form['password']
    valid_login = l.validate_login(username, password)
    if valid_login:
        flask.session['username'] = flask.request.form['username']
        print (flask.session['username'])
        return flask.render_template('profile.html', name=username, gallery = l.render_Gallery())                   # kick you back to landing
    return '<h1> BAD LOGIN.  <a href=".">Try Again</a></h1>'

@app.route('/logout',methods =['GET', 'POST'])
def logout():
    if "username" in flask.session:                                     #want to see whether someone has logged in and in a session
        flask.session.pop('username', None)
        return flask.render_template('landing.html', gallery = l.render_Gallery())                   # kick you back to landing           gallery = l.render_Gallery()

@app.route('/register_user', methods=['POST'])
def register_user():
    username = flask.request.form['username']
    password = flask.request.form['password']
    email = flask.request.form['email']
    valid_registration = l.create_newuser(username, password, email)
    print('Valid registration result = ', valid_registration)
    if valid_registration !="Username already taken":
        flask.session['username'] = flask.request.form['username']
        return flask.render_template('profile.html', name=username, gallery = l.render_Gallery())       # logs in, welcomes user and displays gallery
    else:
        return flask.render_template('error_registered.html')                                               # renders error page to allow another reg attempt

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    file = flask.request.files['file']              #set arguments for function below
    if file:
        filename = secure_filename(file.filename)
        username = flask.session['username']
        l.loadphoto_intodb(filename, username)          # uploadTime    call function to insert uploaded photo into db
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return flask.render_template("image_view.html", file_location='/static/photos/'+filename, filename = filename)
    else:
        return flask.render_template('failed_upload.html') # redirects to error page if user tries to upload air

@app.route('/image_details', methods=['GET', 'POST'])           # trigger image on own with file details when clicked on in landing pg
def image_details():
    return flask.render_template("image_details.html")

app.secret_key = "asdfljhsfdlkjshadflkjhag;aoierhgaiorgj"
app.run()