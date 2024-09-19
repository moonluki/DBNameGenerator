import DBConnect, CreateTable, GenerateDataTableName, GenerateDataTableColumnNames, GenerateSampleRecords

print("=============")
dbSession = DBConnect.Initialize()
print("Data Table Generator")

userKeyword = input("Enter keywords you want to generate the data table for: ")
dbName = GenerateDataTableName.SuggestName(userKeyword)
print(f"Suggested name for the new database: {dbName}.")
print("1 - Keep the name")
print("2 - Generate new one")
print("3 - Enter database name manually")
userReply = int(input())


if userReply == 1:
  nameCheck = CreateTable.CheckIfNameExists(dbSession, dbName)
  while nameCheck>0:
    print(f"Database {dbName} already exists. Generating new one.")
    dbName = GenerateDataTableName.SuggestNewName(userKeyword, dbName)
    print(f"New name: {dbName}")
    nameCheck = CreateTable.CheckIfNameExists(dbSession, dbName)
  CreateTable.CreateDB(dbSession, dbName)
elif userReply == 2:
  userHappy = False
  namesUsed = [f"{dbName}"]
  while userHappy == False:
    dbName = GenerateDataTableName.SuggestNewName(userKeyword, namesUsed)
    namesUsed.append(dbName)
    nameCheck = CreateTable.CheckIfNameExists(dbSession, dbName)
    while nameCheck>0:
      dbName = GenerateDataTableName.SuggestNewName(userKeyword, namesUsed)
      namesUsed.append(dbName)
      nameCheck = CreateTable.CheckIfNameExists(dbSession, dbName)
    print(f"New suggested name: {dbName}")
    newAnswer = input("Are you happy with the new name? Y/N")
    if newAnswer.lower() == "y":
      CreateTable.CreateDB(dbSession, dbName)
      break
elif userReply == 3:
  print("Enter the new database name:")
  dbName = str(input())
  nameCheck = CreateTable.CheckIfNameExists(dbSession, dbName)
  while nameCheck>0:
    print("This database name is taken. Please enter other name.")
    dbName = str(input())
    nameCheck = CreateTable.CheckIfNameExists(dbSession, dbName)
  CreateTable.CreateDB(dbSession, dbName)

columnNames = GenerateDataTableColumnNames.SuggestColumnNames(dbName)
tableName = GenerateDataTableColumnNames.SuggestTableName(dbName, userKeyword, columnNames)
sqlQuery = GenerateDataTableColumnNames.GenerateSqlQuery(columnNames, tableName, userKeyword)
GenerateDataTableColumnNames.SelectNewDatabase(dbSession, dbName)
GenerateDataTableColumnNames.ExecuteQuery(dbSession, sqlQuery)

#Do not update the id, because it uses auto increment.
#for x in columnNames:
#  if "PRIMARY KEY" in x:
#    columnNames.remove(x)

print("How many sample records would you like to generate?")    
maxSampleRecords = int(input())
newRecord = GenerateSampleRecords.GenerateSampleRecord(columnNames, tableName, userKeyword, maxSampleRecords)
print(f"New record: {newRecord}")
queryToExecute = GenerateSampleRecords.GenerateSqlInsert(newRecord, tableName)
print(f"Query to execute: {queryToExecute}")
GenerateSampleRecords.ExecuteQuery(dbSession, queryToExecute)
#for x in range(maxSampleRecords):

