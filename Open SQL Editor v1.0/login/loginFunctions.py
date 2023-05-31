import eel
import pyodbc
import os

from dotenv import load_dotenv, find_dotenv
from passlib.hash import bcrypt

from table.tableFunctions import setCursor


try:
    open(os.getcwd() + "/login/.env", "w")
except:
    open(os.getcwd() + "\login\.env", "w")

load_dotenv(find_dotenv(".env"))

backend = os.environ.get("backend")
server = os.environ.get("server")
database = os.environ.get("database")
username = os.environ.get("username")
password = os.environ.get("password")


@eel.expose
def saveLogin(array):
    array[4] = bcrypt.hash(array[4])
    
    with open(find_dotenv(".env"), "w") as file:
        file.write("backend=" + array[0] + "\n")
        file.write("server=" + array[1] + "\n")
        file.write("database=" + array[2] + "\n")
        file.write("username=" + array[3] + "\n")
        file.write("password=" + array[4] + "\n")

    file.close()

    load_dotenv(find_dotenv(".env"))

    backend = os.environ.get("backend")
    server = os.environ.get("server")
    database = os.environ.get("databse")
    username = os.environ.get("username")
    password = os.environ.get("password")

def isValidPassword(psk):
    password = os.environ.get("password")
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
        if os.stat(find_dotenv(".env")).st_size == 0:
            return True
        
        return False
    except:
        return True
    