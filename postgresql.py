import json

from psycopg2 import connect, extensions

with open("keys.json") as json_data_file:
    file = json.load(json_data_file)
    PASSWORD = file["postgres"]["pwd"]
    HOST = file["postgres"]["host"]
    USER = file["postgres"]["user"]
    DATABASE = file["postgres"]["dbName"]
    tableName = file["postgres"]["tableName"]

conn = connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)


def createTable():
    cur = conn.cursor()
    sqlText = "CREATE TABLE IF NOT EXISTS " + tableName + "(" \
                                                          "pseudo VARCHAR," \
                                                          "pseudoUpper VARCHAR PRIMARY KEY" \
                                                          ")"
    cur.execute(sqlText)
    cur.close()

def insert(pseudo):
    cur = conn.cursor()
    sql = "INSERT INTO " + tableName + " VALUES ('" + pseudo + "','" + pseudo.upper() + "')"
    cur.execute(sql)
    conn.commit()
    cur.close()

def delete(pseudo):
    cur = conn.cursor()
    sql = "DELETE FROM  " + tableName + " WHERE pseudoUpper='" + pseudo.upper() + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()

def getAllPseudo():
    cur = conn.cursor()
    sql = "SELECT pseudo FROM " + tableName
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    final_result = []
    for i in range(0, len(result)):
        final_result.append(result[i][0])
    return final_result
