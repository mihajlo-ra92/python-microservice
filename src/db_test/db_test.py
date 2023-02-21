import os
import mysql.connector
from flask import Flask, request, jsonify
server = Flask(__name__)

mydb = mysql.connector.connect(
  host="mysql",
  user="root",
  password="password"
)
# cursor = mydb.cursor()
# select_db_query = f"USE users;"
# cursor.execute(select_db_query)
# read_users_query = f"SELECT * FROM Users;"
# print(cursor.execute(read_users_query))

@server.route('/')
def index():
  return "hi"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)