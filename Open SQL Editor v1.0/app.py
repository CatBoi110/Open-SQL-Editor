import eel

from login.loginFunctions import *
from table.tableFunctions import *

eel.init("web", allowed_extensions=[".js", ".html"])

eel.start("table.html", mode="default", port=8080)
