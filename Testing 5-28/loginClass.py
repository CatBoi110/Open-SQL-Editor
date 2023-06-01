import eel
import pyodbc

from dotenv import dotenv_values
from passlib.hash import bcrypt


loginValues = dotenv_values(".login")

# This class handles user login info and verifying its validity for logining into a sql database
class login:
    backend = None
    server = None
    database = None
    username = None
    password = None


    def __init__(cls):
        if len(loginValues) == 5:
            login.backend = loginValues["backend"]
            login.server = loginValues["server"]
            login.database = loginValues["database"]
            login.username = loginValues["username"]
            login.password = loginValues["password"]
        
    @eel.expose
    def saveLogin(array):
        array[4] = bcrypt.hash(array[4])
        
        with open(".login", "w") as file:
            file.write("backend=" + array[0]+ "\n")
            file.write("server=" + array[1] + "\n")
            file.write("database=" + array[2] + "\n")
            file.write("username=" + array[3] + "\n")
            file.write("password=" + array[4] + "\n")

        file.close()

        loginValues = dotenv_values(".login")

        login.backend = loginValues["backend"]
        login.server = loginValues["server"]
        login.database = loginValues["database"]
        login.username = loginValues["username"]
        login.password = loginValues["password"]

    @classmethod
    def isValidPassword(cls, psk):
        return bcrypt.verify(psk, login.password)
    
    @classmethod
    def connectToBackend(cls, psk):
        returnList = []
        errorCode = ""
        connection = None
        

        if login.isValidPassword(psk):
            try:
                if login.backend == "MySQL":
                    connection = pyodbc.connect("DRIVER=MySQL ODBC 8.0;SERVER="+login.server+";DATABASE="+login.database+";UID="+login.username+";PWD="+psk+";charset=utf8mb4;") 
                elif login.backend == "MS Azure":
                    connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+login.server+';DATABASE='+login.database+';ENCRYPT=yes;UID='+login.username+';PWD='+psk)
            except pyodbc.Error as ex:
                errorCode = ex.args[1]
        else:
            errorCode = "Incorrect Password"
        
        returnList.append(connection)
        returnList.append(errorCode)

        return returnList

    @classmethod
    def isLoginEmpty(cls):
        if len(loginValues) == 5:
            return False
        else:
            return True