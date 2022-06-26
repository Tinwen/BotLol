from genericpath import exists
import json

from psycopg2 import connect, extensions

with open("keys.json") as json_data_file:
    file = json.load(json_data_file)
    PASSWORD = file["postgres"]["pwd"]
    HOST = file["postgres"]["host"]
    USER = file["postgres"]["user"]
    DATABASE = file["postgres"]["dbName"]

conn = connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

def checkTable(tableName):
    cur = conn.cursor()
    try :
        cur.execute("SELECT 1 FROM information_schema.tables WHERE table_name=t_"+tableName)
        cur.close()
    except : 
        cur.close()
        createTable(tableName)

def createTable(tableName):
    cur = conn.cursor()
    sqlText = "CREATE TABLE IF NOT EXISTS t_" + tableName + "(" \
                                                          "pseudo VARCHAR," \
                                                          "pseudoUpper VARCHAR PRIMARY KEY" \
                                                          ")"
    cur.execute(sqlText)
    cur.close()

def insert(pseudo,tableName):
    checkTable(tableName)
    cur = conn.cursor()
    sql = "INSERT INTO t_" + tableName + " VALUES ('" + pseudo + "','" + pseudo.upper() + "')"
    cur.execute(sql)
    conn.commit()
    cur.close()

def delete(pseudo,tableName):
    checkTable(tableName)
    cur = conn.cursor()
    sql = "DELETE FROM  t_" + tableName + " WHERE pseudoUpper='" + pseudo.upper() + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()

def getAllPseudo(tableName):
    checkTable(tableName)
    cur = conn.cursor()
    sql = "SELECT pseudo FROM t_" + tableName
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    final_result = []
    for i in range(0, len(result)):
        final_result.append(result[i][0])
    return final_result
