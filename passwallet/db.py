import MySQLdb
import sys
from configparser import ConfigParser


def initiate_database(comm, fetch=None):
    config_db = ConfigParser()
    config_db.read("config.ini")
    data = config_db["DATABASE"]
    host = data["host"]
    user = data["user"]
    database = data["database"]
    password = data["password"]

    connect = MySQLdb.connect(host, user, password, database)
    cursor = connect.cursor()
    command_execution = cursor.execute(comm)

    if fetch == "all":
        return cursor.fetchall()
    elif fetch == "one":
        return cursor.fetchone()
    else:
        return command_execution


   