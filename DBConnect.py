import mysql.connector, os

def Initialize():
  print("Connecting to the database...")
  mydb = mysql.connector.connect(
  host="localhost",
  user=os.environ["LOCAL_DB_USER"],
  password=os.environ["LOCAL_DB_PASS"]
  )
  return mydb