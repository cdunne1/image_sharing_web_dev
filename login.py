import sqlite3

# cur.execute('''CREATE TABLE registered_users (
#     Username varchar (20),
#     Password varchar (10),
#     PRIMARY KEY (Username)
#     ) ''')

# q1 = '''SELECT * FROM	registered_users;'''                q2 = '''SELECT name FROM sqlite_master WHERE type='table'; '''

def open_db_connect():
    db = sqlite3.connect('mydb.db')
    cur = db.cursor()
    return (db, cur)

def close_db_connect(db):
    db.commit()
    db.close()

def checkif_user_exists(cred_name, cred_pass):          # function to check whether user already exists in database
    db,cur = open_db_connect()
    cur.execute("SELECT * FROM registered_users WHERE Username = \"" + cred_name + "\"")
    userlist = cur.fetchall()   # gives last executed line of db
    close_db_connect(db)
    if len(userlist) > 0:       # if >0; user already exists so not possible to insert new row into db (create login)
        return False            # ("User already exists")          # PLACEHOLDER
    return flask.render_template('error_registered.html', msg="Username already taken")
    #return True

def validate_login(cred_name, cred_pass):
    db,cur = open_db_connect()
    cur.execute("SELECT * FROM registered_users WHERE Password = \"" + cred_pass + "\" and Username = \"" + cred_name + "\"")
    # SQl break back into Python to pass in parameters
    userlist = cur.fetchall()           # gives last executed line of db
    close_db_connect(db)
    if len(userlist) > 0:
        return True
    return False

def sanitise_inputs(input_string):              # prevent against SQL injections
    for i in input_string:
        if i == "%":                            # if % is found, it breaks; if not, skips through and returns True
            return False
    return True

def create_newuser(cred_name, cred_pass):
    db,cur = open_db_connect()
    if checkif_user_exists(cred_name, cred_pass) == False:
        print("Error 400... Bad request")
        return flask.render_template('error_registered.html', msg="Username already taken") #False
    else:
        cur.execute('''INSERT INTO registered_users (Username, Password) VALUES("''' + cred_name + '''", "''' + cred_pass+'''")''')
        close_db_connect(db)
        return True

def loadphoto_intodb(photoName,username):
    db, cur = open_db_connect()
    cur.execute('''INSERT INTO photoUpload (photoName, username, uploadTime) VALUES("''' + photoName + '''", "''' + username + '''", CURRENT_TIMESTAMP)''')
    close_db_connect(db)
    return True

def render_Gallery():
    db, cur = open_db_connect()
    cur.execute("SELECT * FROM photoUpload")            #('photoName')
    gallery = cur.fetchall()                                  #renders list of items (tupples) in db
    close_db_connect(db)
    return gallery

