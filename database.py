import sqlite3
import time
import json
import re

def databaseConnection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn
    

def databaseTable(conn, sqlCommands):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sqlCommands)
    except sqlite3.Error as e:
        print(e)

def databaseInsertData(conn, slackValues):
    
    sqlInsert = ''' INSERT INTO group1(user_id, user_text, message_timestamp_unix, message_timestamp, watson_NLU_result)
    VALUES(?,?,?,?,?)
    '''
    cur = conn.cursor()
    cur.execute(sqlInsert, slackValues)
    conn.commit()
    return cur.lastrowid

#Use parameters as value from NLU & Slack
def main(slackValues,watsonValues):
    database = r"database/groupValues.db"

    createGroup1Table = """
    CREATE TABLE IF NOT EXISTS group1(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        user_text TEXT NOT NULL,
        message_timestamp_unix TEXT NOT NULL,
        message_timestamp TEXT NOT NULL,
        watson_NLU_result TEXT NOT NULL
    );
    """
    #slackEventChannelValues = slackValues.get("channel", None) or slackValues["channel"]
    slackEventUserIDValues = slackValues.get("user", None) or slackValues["user"]
    slackEventsTextValues = slackValues.get("text", None) or slackValues["text"]
    slackEventsTimestampValues = slackValues.get("ts", None) or slackValues["ts"]

    timestampConverted = time.ctime(float(slackEventsTimestampValues))
    #slackTextImproved = re.sub("[\<\[].*?[\>\]]", "", slackEventsTextValues)

    watsonNLUString = json.dumps(watsonValues)

    insertableSlackValues = (slackEventUserIDValues, slackEventsTextValues, slackEventsTimestampValues, timestampConverted, watsonNLUString)
    conn = databaseConnection(database)

    if conn is not None:
        databaseTable(conn, createGroup1Table)
        databaseInsertData(conn, insertableSlackValues)
        print("inserted")
    else:
        print("Error! Database connection not working")
