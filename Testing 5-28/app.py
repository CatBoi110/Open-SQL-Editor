import pyodbc 
import eel
import sys
from loginClass import login

sys.path.insert(0, "login/")

eel.init("web", allowed_extensions=[".js", ".html"])

login = login()

cursor = ""
table = ""

@eel.expose
def loginToServer(psk):
    # Start Here
    global cursor
    returnList = login.connectToBackend(psk)

    connection = returnList[0]
    returnCode = returnList[1]

    if returnCode != "":
        eel.alertErrorCode(returnCode)
        return False
    else:
        eel.alertCorrectLogin()
        cursor = connection.cursor()
        return True

@eel.expose
def isLoginEmpty():
    return login.isLoginEmpty()

@eel.expose
def refresh():
    tableData = [] # Collection of all the data in the table in a 2d array

    cursor.execute("select * from " + table + ";");
    
    row = cursor.fetchall()
    tempArray = []

    for i in range(len(row)):
        for j in range(len(row[i])):
            tempArray.append(str(row[i][j]).strip())

        tableData.append(tempArray)
        tempArray = []

    return tableData

@eel.expose
def deleteRow(row):
    qurey = "delete from " + table + " where "

    columnNum = 0

    for i in range(len(keyFields)):
        if len(keyFields) > 0:
            qurey += str(keyFields[i][0]) + "=" + "'" + str(row[columnNum]) + "' and "
            columnNum += 1
        elif len(keyFields) == 0:
            qurey += str(keyFields[i][0]) + "=" + "'" + str(row[columnNum]) + "';"

    for i in range(len(dataFields)):
        if i < len(dataFields) - 1:
            qurey += str(dataFields[i][0]) + "=" + "'" + str(row[columnNum]) + "' and "
            columnNum += 1
        elif i == len(dataFields) - 1:
            qurey += str(dataFields[i][0]) + "=" + "'" + str(row[columnNum]) + "';"

    cursor.execute(qurey)
    cursor.commit()

@eel.expose
def submitData(data):
    qurey = "insert into " + table + " values("

    for i in range(len(data)):
        if i < len(data) - 1:
            qurey += "'" + str(data[i]) + "', "
        elif i == len(data) - 1:
            qurey += "'" + str(data[i]) + "');"


    cursor.execute(qurey)
    cursor.commit()

def formatArray(startArr, endArr):

    tempList = []
    tempCharList = []

    tempString = ""

    for i in range(0, len(startArr)):
        if (startArr[i] not in ["[", "(", "'", ",", ")", "]"]):
            tempList.append(startArr[i])

        if (startArr[i] == ")"):
            tempCharList.append(tempList)
            tempList = []

    for i in range(len(tempCharList)):
        for j in range(len(tempCharList[i])):
            tempString += tempCharList[i][j];

        endArr.append(tempString.split(" ")) 
        tempString = ""

    # Formats dataFields list to remove any blank indices
    for i in range(1, len(endArr)):
        endArr[i].pop(0)

    return endArr

@eel.expose
def updateRow(newData, keyData):
    qurey = "update " + table + " set "

    for i in range(len(dataFields)):
        if i < len(dataFields) - 1:
            qurey += dataFields[i][0] + " = '" + newData[i] + "', "
        elif i == len(dataFields) - 1:
            qurey += dataFields[i][0] + " = '" + newData[i] + "'"


    qurey += " where " + keyFields[0][0] + " = '" + keyData + "'"

    cursor.execute(qurey)
    cursor.commit()

@eel.expose
def initTable():
    global dataFields
    global keyFields 

    dataFields = []
    keyFields = []

    #cursor.execute("select column_name from information_schema.columns where table_name = 'JacksTable' and is_nullable = 'yes'")
    cursor.execute("select column_name, data_type from information_schema.columns where table_name = '" + table + "' and is_nullable = 'yes';")
    fetchedData = list(str(cursor.fetchall()))

    formatArray(fetchedData, dataFields)

    fetchedData = ""

    cursor.execute("select column_name, data_type from information_schema.columns where table_name = '" + table + "' and is_nullable = 'no';")
    fetchedData = list(str(cursor.fetchall()))

    formatArray(fetchedData, keyFields)

    # Returns a 2D array with the table's individual columns and data types
    return [dataFields, keyFields]

@eel.expose
def getAvailableTables():        
    listOfTables = []

    cursor.execute("select table_name from information_schema.tables;")
    formatArray(list(str(cursor.fetchall())), listOfTables)

    for i in range(len(listOfTables)):
        for j in range(len(listOfTables[i])):
            if (listOfTables[i][j] == ""):
                listOfTables[i].pop(j)

    return listOfTables;


@eel.expose
def setTable(newTable):
    global table

    table = newTable


@eel.expose
def returnHome():
    eel.show("home.html")

eel.start("home.html", mode="default")
