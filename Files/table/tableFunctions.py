import pyodbc 
import eel

table = ""
cursor = ""

@eel.expose
def initTable():
    global dataFields
    global keyFields 

    dataFields = []
    keyFields = []

    sendQuery("select column_name, data_type from information_schema.columns where table_name = '" + table + "' and is_nullable = 'yes';", False)
    fetchedData = list(str(cursor.fetchall()))

    formatArray(fetchedData, dataFields)

    fetchedData = ""

    sendQuery("select column_name, data_type from information_schema.columns where table_name = '" + table + "' and is_nullable = 'no';", False)
    fetchedData = list(str(cursor.fetchall()))

    formatArray(fetchedData, keyFields)

    return [dataFields, keyFields]


@eel.expose
def getAvailableTables():        
    listOfTables = []

    try:
        cursor.execute("show tables;")
    except pyodbc.Error:
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

def setCursor(csr):
    global cursor
    
    cursor = csr


@eel.expose
def refresh():
    tableData = [] 

    sendQuery("select * from " + table + ";", False);
    
    row = cursor.fetchall()
    tempArray = []

    for i in range(len(row)):
        for j in range(len(row[i])):
            tempArray.append(str(row[i][j]).strip())

        tableData.append(tempArray)
        tempArray = []

    return tableData


@eel.expose
def addRow(data):
    query = "insert into " + table + " values("

    for i in range(len(data)):
        if i < len(data) - 1:
            query += "'" + str(data[i]) + "', "
        elif i == len(data) - 1:
            query += "'" + str(data[i]) + "');"


    sendQuery(query, True)


@eel.expose
def deleteRow(row):
    query = "delete from " + table + " where "

    columnNum = 0

    for i in range(len(keyFields)):
        if len(keyFields) > 0:
            query += str(keyFields[i][0]) + "=" + "'" + str(row[columnNum]) + "' and "
            columnNum += 1
        elif len(keyFields) == 0:
            query += str(keyFields[i][0]) + "=" + "'" + str(row[columnNum]) + "';"

    for i in range(len(dataFields)):
        if i < len(dataFields) - 1:
            query += str(dataFields[i][0]) + "=" + "'" + str(row[columnNum]) + "' and "
            columnNum += 1
        elif i == len(dataFields) - 1:
            query += str(dataFields[i][0]) + "=" + "'" + str(row[columnNum]) + "';"

    sendQuery(query, True)


@eel.expose
def editRow(newData, keyData):
    query = "update " + table + " set "

    for i in range(len(dataFields)):
        if i < len(dataFields) - 1:
            query += dataFields[i][0] + " = '" + newData[i] + "', "
        elif i == len(dataFields) - 1:
            query += dataFields[i][0] + " = '" + newData[i] + "'"


    query += " where " + keyFields[0][0] + " = '" + keyData + "'"

    sendQuery(query, True)


def sendQuery(query, alertOnSuccess):
    try:
        cursor.execute(query)
    except pyodbc.Error as ex:
        eel.alertErrorCode(ex.args[1])
    else:
        if alertOnSuccess == True:
            eel.alertSuccessfulQuery()
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

    for i in range(1, len(endArr)):
        endArr[i].pop(0)

    return endArr