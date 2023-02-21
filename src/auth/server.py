import jwt, datetime, os
from flask import Flask, request
server = Flask(__name__)
import mysql.connector

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# create a connection to the MySQL server
cnx = mysql.connector.connect(user='username', password='password',
                              host='localhost')

# create a cursor object to execute SQL queries
cursor = cnx.cursor()

# define the SQL query to create a new database
DB_NAME = 'new_database'
create_database_query = f"CREATE DATABASE {DB_NAME}"

# execute the query to create the new database
cursor.execute(create_database_query)

# close the cursor and connection
cursor.close()
cnx.close()

print("Database created successfully!")



@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing cerdentials", 401

    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user where email=%s", (auth.username,)
    )
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid cerdentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid cerdentials", 401

@server.route("/validate", method=["POST"])
def validate():
    encoded_jwt = request.headers["Autharization"]
    if not encoded_jwt:
        return "missing cerdentials", 401
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return "not authorized", 403
    return decoded, 200

def createJWT(username, secret, authz):
    return jwt.encode(
        {"username": username,
         "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
         "iat": datetime.datetime.utcnow(),
         "admin": authz,
        },
        secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)