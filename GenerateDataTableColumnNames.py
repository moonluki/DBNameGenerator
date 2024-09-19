from pydantic import BaseModel
from openai import OpenAI
import mysql.connector

client = OpenAI()

class SqlQuery(BaseModel):
  sqlQuery: str

class ColumnNames(BaseModel):
  columnNames: list[str]

class TableName(BaseModel):
  tableName: str

def SuggestColumnNames(dbName: str):
  print(f"Suggested column names for {dbName}:")
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant specialized in MySQL."},
        {"role": "user","content": f"Suggest column names and their types for a database called {dbName}. Name each column in the same language that the user has used. Do not use any special characters other than '_'. Declare the type and its max length, if needed, for each column. Include it as a part of the string."}
    ],
    response_format=ColumnNames,
  )
  event = completion.choices[0].message.parsed
  return event.columnNames

def SuggestTableName(dbName: str, userKeywords: str, columnNames):
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant specialized in MySQL."},
        {"role": "user","content": f"Suggest MySql table name for a data base called {dbName}, based on keywords: {userKeywords} and a list of columns and their types: {columnNames}. Use the same language that the user has used."}
    ],
    response_format=TableName,
  )
  event = completion.choices[0].message.parsed
  return event.tableName

def GenerateSqlQuery(columnNames, tableName: str, userKeywords: str):
  print(f"{columnNames}")
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant specialized in MySQL."},
        {"role": "user","content": f"Create MySql query to create columns and their types: {columnNames} in a data table called: {columnNames}, based on keywords: {userKeywords}. Start with 'CREATE TABLE {tableName}."}
    ],
    response_format=SqlQuery,
  )
  event = completion.choices[0].message.parsed
  return event.sqlQuery

def SelectNewDatabase(dbSession, dbName: str):
  mycursor = dbSession.cursor()
  try:
    mycursor.execute(f"USE {dbName}")
  except:
    print(f"Failed to select database {dbName}.")
  else:
    print(f"Selected database {dbName}")
  

def ExecuteQuery(dbSession, queryToExecute: str):
  mycursor = dbSession.cursor()
  try:
    mycursor.execute(f"{queryToExecute}")
  except:
    print(f"Failed to create the database. MySql query: {queryToExecute}")
  else:
    print("Database created.")