import os, uuid, json
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
server = Flask(__name__)

server.config['MYSQL_HOST'] = 'mysql'
server.config['MYSQL_USER'] = 'root'
server.config['MYSQL_PASSWORD'] = 'password'
server.config['MYSQL_DB'] = 'users'

mysql = MySQL(server)

@server.route('/users', methods=["GET"])
def index():
  cur = mysql.connection.cursor()
  db_res = cur.execute(f"SELECT * FROM Users")
  row_headers=[x[0] for x in cur.description] #this will extract row headers
  if db_res > 0:
    user_details = cur.fetchall() 
  cur.close()
  json_data=[]
  for result in user_details:
    json_data.append(dict(zip(row_headers,result)))
  return json.dumps(json_data)

@server.route('/add-user', methods=["POST"])
def add_user():
  user_details = request.json
  print(f"user_details: {user_details}")
  username = user_details["username"]
  password = user_details["password"]
  email = user_details["email"]

  cur = mysql.connection.cursor()
  print(f"INSERT INTO Users(id, username, password, email) VALUES ('{str(uuid.uuid1())}', '{username}', '{password}', '{email}');")
  cur.execute(f"INSERT INTO Users(id, username, password, email) VALUES ('{str(uuid.uuid1())}', '{username}', '{password}', '{email}');")
  mysql.connection.commit()
  cur.close()
  return 'success'
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)