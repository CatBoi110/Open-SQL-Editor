# Open-SQL-Editor

## **What is this program is about?**
  Open SQL Editor is a graphical SQL table editor. It allows the user to edit, delete, and view records in SQL tables. Currently the program supports MySQL and Microsoft Azure SQL, with more backends to be added in the future.
  
This project was created using the python Eel library as the backend and with HTML, CSS, and JS as the frontend. This program supports all major web browsers, such as Firefox, Chrome, Chromium, and Edge. 

For any questions or concerns please contact me at **https://github.com/CatBoi110 or jlevin110@outlook.com.**

## **Features**
  1. View multiple tables in a SQL database
  2. Edit records in a table
  3. Delete records in a table
  4. Login to a SQL server

## **How to install**
  **Ensure you are running either Windows 10 or Linux on your computer.**
  
  **Download one of the following ODBC connectors for SQL:**
  - MySQL: [MySQL ODBC](https://dev.mysql.com/doc/connector-odbc/en/)
  
  - MS Azure: [MS Azure ODBC](https://learn.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver16)
  
  **Select one of the options to download and run the program:**
  
  - Download and run a prebuilt executable from the releases tab (Recommended)
     
  - Download and run source files from the ```Open-SQL-Editor-Files``` Folder
  
### Run from Executable 
**Download the executable for your system.**
- For Windows download ```Open-SQL-Editor-Windows.exe```
- For Linux download ```Open-SQL-Editor-Linux```

**Either run the program from a desktop envornment or run it from a terminal or command prompt with the following commands.**
- Windows: ```C:\ Open-SQL-Editor-Windows.exe```
- Linux: ```~$ ./Open-SQL-Editor-Linux```
 
### Run from Source
**To run from source, ensure you have installed the following:**
- Latest Version of Python: ```https://www.python.org/```
- Eel: ```pip install eel```
- Pyodbc: ```pip install pyodbc```
- Dotenv: ```pip install python-dotenv```
- Passlib: ```pip install passlib```

**Then type in a terminal or command line ```python app.py``` to start the program. This will open a GUI window in your default web browser of choice.**

## Screenshots


![Screenshot_20230602_140646](https://github.com/CatBoi110/Open-SQL-Editor/assets/91166833/4f0e9e2a-c725-4741-aa7b-71eecfd5a7b9)
Firefox

![Screenshot_20230602_150600](https://github.com/CatBoi110/Open-SQL-Editor/assets/91166833/c0c6703e-8de8-4856-9578-70c5e748f598)
Chrome/Chromium


## Know Limitations
- Some tables may not function correctly with certain arangements of key fields
- The edit function will not function for tables that lack a key field
- Web browser may not see program running and will display an error message. (To fix this press the 'Reload' button until the program appears)
- Large tables may be difficult to view and may require the screen to be zoomed out.

## Acknowledgments
**Libraries Used:**
- Pyodbc: ```https://pypi.org/project/pyodbc```
- Eel: ```https://pypi.org/project/Eel```
- Dotenv: ```https://pypi.org/project/python-dotenv```
- Passlib: ``` https://pypi.org/project/passlib```
- Pyinstaller: ```https://pypi.org/project/pyinstaller```
