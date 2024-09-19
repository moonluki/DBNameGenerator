import mysql.connector

def CreateDB(dbSession, name):
  mycursor = dbSession.cursor()
  mycursor.execute(f"CREATE DATABASE {name}")

def CheckIfNameExists(dbSession, name):
  mycursor = dbSession.cursor(dictionary=True)
  mycursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{name}'")
  result=mycursor.fetchall()
  return len(result)