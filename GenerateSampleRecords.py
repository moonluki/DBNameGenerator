import mysql.connector, json
from openai import OpenAI
from typing import Any, List
from pydantic import BaseModel, Json, ValidationError

client = OpenAI()

class Record(BaseModel):
  jsonString: Json[Any]

class SqlQuery(BaseModel):
  query: str



def GenerateSampleRecord(columnNames: list[str], tableName: str, keywords: str, maxRecords: int):
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant specialized in MySQL."},
        {"role": "user","content": f"Generate {maxRecords} record(s) for a data table called: {tableName} based on keywords: {keywords}. Populate all column names with correct types: {columnNames}."}
    ],
    response_format=Record,
  )
  event = completion.choices[0].message.parsed
  return json.dumps(event.jsonString)

def GenerateSqlInsert(jsonToInsert, tableName):
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant specialized in MySQL."},
        {"role": "user","content": f"Generate MySql query to insert records: {jsonToInsert} into a data table called: {tableName}. Start with: INSERT INTO {tableName}."}
    ],
    response_format=SqlQuery,
  )
  event = completion.choices[0].message.parsed
  return event.query

def ExecuteQuery(dbSession, queryToExecute: str):
  print(f"MySql query: {queryToExecute}")
  mycursor = dbSession.cursor()
  try:
    mycursor.execute(f"{queryToExecute}")
  except:
    print(f"Failed to execute query: {queryToExecute}")
  else:
    print("Record inserted.")
  try:
    dbSession.commit()
  except:
    print("Failed to commit changes.")
  else:
    print("Changes committed successfully.")