import mysql.connector
from flask import Flask, request, jsonify

mydb = mysql.connector.connect(
  host="mysql",
  user="root",
  password="password"
)

print(mydb)