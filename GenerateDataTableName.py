from openai import OpenAI
from pydantic import BaseModel
client = OpenAI()

class dbName(BaseModel):
  name: str

def SuggestName(userKeywords):
  print(f"Generating suggested data table name for keywords: {userKeywords}")
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant specialized in MySQL."},
        {"role": "user","content": f"Suggest a single name for a database based on keywords selected by the user: {userKeywords}. Name the database in the same language that the user has used. The name has to end with '_db'. Keep the name short, but informative."}
    ],
    response_format=dbName,
  )
  event = completion.choices[0].message.parsed
  return event.name

def SuggestNewName(userKeywords, namesUsed):
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant specialized in MySQL."},
        {"role": "user","content": f"Suggest a single name for a database based on keywords selected by the user: {userKeywords}. Use the same language that the user has used. The name has to end with '_db'. Use name other than {namesUsed}. You can use digits if you run out of ideas."}
    ],
    response_format=dbName,
  )
  event = completion.choices[0].message.parsed
  return event.name