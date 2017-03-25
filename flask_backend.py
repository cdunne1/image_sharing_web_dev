# Anyone can log in now....
import os
from werkzeug.utils import secure_filename
import login as l

import flask
from flask import request

app	= flask.Flask(__name__)
UPLOAD_FOLDER = 'C:\\Users\\cdunn\\Documents\\Interactive Digital Media\\Programming for Digital MediaI\\ImageApp\\photos'          #NEEDS TO BE RELATIVE LINK
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods =['GET', 'POST'])
def	index():
    # if "username" in flask.session:                                     #want to see whether someone has logged in and in a session
    #     return flask.render_template("profile.html", name=flask.session['username'])
    # if flask.request.method ==	'POST':
    #     if "hiddenelement" in flask.request.form:
    #         return flask.render_template("templates.html")              #brings you to log in page
    #     else:
    #         username = flask.request.form['username']
    #         password = flask.request.form['password']
    #         # create a dictionary to allow multiple folk login; key is username, value is password
    #         # check username exists in dict, if so, check password matches up... if so then log in
    #         if username in credentials.keys():
    #             if password == credentials[username]:           #avoid and statements as may reorder key and values, need to be of the same key value pair; hence nesting
    #                 flask.session['username'] = flask.request.form['username']  # create session only if logged in correctly
    #                 return flask.render_template("profile.html", name=username, passw=password)
    #             else:
    #                 return flask.render_template("templates.html")      # password doesnt match username, need to retry - best practice not to specify which has gone awry
    #         else:
    #             return flask.render_template("templates.html")         # eejits havent logged in so gettign the prompt again; username not in dictionary credentials
    # else:
    return flask.render_template("landing.html")

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
        username = request.args.get("username")
        if username is not None:
            #return "Hello " + username  # Return	the	value	we	want	as	the	response
            return flask.render_template('profile.html')                   # kick you back to landing
    # < !-- @ app.route("/greeting")  # Configure	app	route
    #
    # def say_hello():  # Define	function	for	the	route
    #     name = request.args.get("name")
    #     if name is None:
    #         return "Hello stranger!"
    #     else:
    #         return "Hello " + name  # Return	the	value	we	want	as	the	response

    return '<h1> BAD LOGIN. Go Away </h1>'

@app.route('/logout',methods =['GET', 'POST'])
def logout():
    if "username" in flask.session:                                     #want to see whether someone has logged in and in a session
        flask.session.pop('username', None)
        return flask.render_template('landing.html')                   # kick you back to landing


@app.route('/register_user', methods=['POST'])
def register_user():
    username = flask.request.form['username']
    password = flask.request.form['password']
    valid_registration = l.create_newuser(username, password)
    if valid_registration:
        flask.session['username'] = flask.request.form['username']
        return flask.render_template('profile.html')                   # kick you back to landing
    return '<h1> Sorry kiddo. You cant register. Mwahahaha. Go Away </h1>'


@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    #filename = flask.request.form['filename']
    file = flask.request.files['file']

    print ('filename=' + file.filename)
    print(os.path)
    #file.save(os.path.join(UPLOAD_FOLDER,file.filename))

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #f = open('photos/'+file.filename+'.jpg', 'w')
    #f.write(file)
    #f.writelines(file)
    #f.close()
    print('hi')
    return '<h1> File Uploaded </h1>'





app.secret_key = "asdfljhsfdlkjshadflkjhag;aoierhgaiorgj"
app.run()