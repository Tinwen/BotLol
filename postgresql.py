import json

import psycopg2

print("slt")
with open("keys.json") as json_data_file:
    file = json.load(json_data_file)
    PASSWORD = file["postgres"]["pwd"]
    HOST = file["postgres"]["host"]
    USER = file["postgres"]["user"]
    DATABASE = file["postgres"]["dbName"]

conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
cur = conn.cursor()


def createTable(tableName):
    sqlText = "CREATE TABLE IF NOT EXISTS " + tableName + "(" \
                                                          "pseudo VARCHAR," \
                                                          "pseudoUpper VARCHAR PRIMARY KEY" \
                                                          ")"
    cur.execute(sqlText)


def insert(tableName, pseudo):
    sql = "INSERT INTO " + tableName + " VALUES ('" + pseudo + "','" + pseudo.upper() + "')"
    cur.execute(sql)
    conn.commit()


def delete(tableName, pseudo):
    sql = "DELETE FROM  " + tableName + " WHERE pseudoUpper='" + pseudo.upper() + "'"
    cur.execute(sql)
    conn.commit()


def getAllPseudo(tableName):
    sql = "SELECT * FROM " + tableName
    cur.execute(sql)
    result = cur.fetchall()
    final_result = []
    for i in range(0, len(result)):
        final_result.append(result[i][0])
    return final_result