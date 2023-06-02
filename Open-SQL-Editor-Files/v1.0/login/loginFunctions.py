#Start Here: Have program create config file with login info 
import eel
import pyodbc
import os

from dotenv import dotenv_values
from passlib.hash import bcrypt

from table.tableFunctions import setCursor

loginFile = ".env"

@eel.expose
def saveLogin(array):
    global backend, server, database, username, password
    array[4] = bcrypt.hash(array[4])
    
    with open(loginFile, "w") as file:
        file.write("backend=" + array[0] + "\n")
        file.write("server=" + array[1] + "\n")
        file.write("database=" + array[2] + "\n")
        file.write("username=" + array[3] + "\n")
        file.write("password=" + array[4] + "\n")

    file.close()

    values = dotenv_values(loginFile)

    backend = values["backend"]
    server = values["server"]
    database = values["database"]
    username = values["username"]
    password = values["password"]

def isValidPassword(psk):
    return bcrypt.verify(psk, password)

@eel.expose
def connectToBackend(psk):
    errorCode = ""
    connection = None
    
    if isValidPassword(psk):
        try:
            if backend == "MySQL":
                connection = pyodbc.connect("DRIVER=MySQL ODBC 8.0 ANSI Driver;SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+psk+";charset=utf8mb4;") 
            elif backend == "MS Azure":
                connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+psk)
        except pyodbc.Error as ex:
            errorCode = ex.args[1]
    else:
        errorCode = "Incorrect Password"

    if errorCode != "":
        eel.alertErrorCode(errorCode)
        return False
    else:
        eel.alertCorrectLogin()
        cursor = connection.cursor()
        setCursor(cursor)
        return True
    

@eel.expose
def isLoginEmpty():
    try:
        if os.stat(loginFile).st_size == 0:
            return True
        
        return False
    except:
        return True


if not os.path.isfile(loginFile):
    open(loginFile, "w").close()

if not isLoginEmpty():
    values = dotenv_values(loginFile)

    backend = values["backend"]
    server = values["server"]
    database = values["database"]
    username = values["username"]
    password = values["password"]