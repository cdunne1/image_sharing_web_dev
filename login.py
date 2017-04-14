import sqlite3

# def updateDB():
#     db, cur = open_db_connect()
#     cur.execute('''CREATE TABLE uploaded_photos (
#         photoName varchar (20),
#         photoID int AUTO_INCREMENT(3),
#         userName varchar (10),
#         photoTime int CURRENT_TIMESTAMP(20),
#         PRIMARY KEY (photoID)
#         ) ''')
#     close_db_connect(db)
#     return True

def open_db_connect():
    db = sqlite3.connect('mydbcopy.db')
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
    #return flask.render_template('error_registered.html', msg="Username already taken")
    return True

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

def create_newuser(cred_name, cred_pass, email_add):
    db,cur = open_db_connect()
    if checkif_user_exists(cred_name, cred_pass) == False:
        print("Error 400... Bad request")
        return "Username already taken"
    else:
        cur.execute('''INSERT INTO registered_users (Username, Password, Email) VALUES("''' + cred_name + '''", "''' + cred_pass+'''", "''' + email_add +'''")''')
        close_db_connect(db)
        return True


def loadphoto_intodb(photoName,username):
    db, cur = open_db_connect()
    sql = '''INSERT OR REPLACE INTO photoUploadNew (photoName, username, uploadTime) VALUES("''' + photoName + '''", "''' + username + '''", CURRENT_TIMESTAMP)'''
    #print( sql)
    cur.execute(sql)
    close_db_connect(db)
    return True

def render_Gallery():
    db, cur = open_db_connect()
    cur.execute("SELECT photoName, username, uploadTime FROM photoUploadNew")            #('photoName')
    result = cur.fetchall()                                     #renders list of items (tupples) in db
    close_db_connect(db)
    gallery_details = []
    for item in result:
        gallery = []
        gallery.append('/static/photos/' + item[0])
        gallery.append(item[1])
        gallery.append(item[2])
        gallery_details.append(gallery)
    #print (gallery_details)
    return gallery_details

def imageDetails(photoName):
    db, cur = open_db_connect()
    cur.execute("SELECT username, uploadTime FROM photoUploadNew WHERE photoName='{0}'".format(photoName))            # retrieve db entry uploader and update time
    result = cur.fetchall()                                     #renders list of items (tupples) in db
    close_db_connect(db)
    return