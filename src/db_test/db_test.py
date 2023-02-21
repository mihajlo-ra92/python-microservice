import os, uuid
# import mysql.connector
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
server = Flask(__name__)

server.config['MYSQL_HOST'] = 'mysql'
server.config['MYSQL_USER'] = 'root'
server.config['MYSQL_PASSWORD'] = 'password'
server.config['MYSQL_DB'] = 'users'

mysql = MySQL(server)


# mydb = mysql.connector.connect(
#   host="mysql",
#   user="root",
#   password="password"
# )

# cursor = mydb.cursor()
# select_db_query = f"USE users;"
# cursor.execute(select_db_query)
# read_users_query = f"SELECT * FROM Users;"
# print(cursor.execute(read_users_query))

@server.route('/', methods=["GET"])
def index():
  cur = mysql.connection.cursor()
  retVal = cur.execute(f"SELECT * FROM Users")
  cur.close()
  return "hi"

@server.route('/add-user', methods=["POST"])
def add_user():
  userDetails = request.json
  print(f"userDetails: {userDetails}")
  username = userDetails["username"]
  password = userDetails["password"]
  email = userDetails["email"]

  cur = mysql.connection.cursor()
  print(f"INSERT INTO Users(id, username, password, email) VALUES ('{str(uuid.uuid1())}', '{username}', '{password}', '{email}');")
  cur.execute(f"INSERT INTO Users(id, username, password, email) VALUES ('{str(uuid.uuid1())}', '{username}', '{password}', '{email}');")
  mysql.connection.commit()
  cur.close()
  return 'success'
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)