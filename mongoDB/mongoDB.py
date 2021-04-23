import pymongo
import time
import logging

def retrieveDataMongoDB(userText, databaseName):
    mongoClient = pymongo.MongoClient("localhost", 27017)
    mongoDatabase = mongoClient["slackDatabase"]
    slackChannelData = mongoDatabase[databaseName]

    for value in slackChannelData.find():
        if value["user_text"] == userText:
            return value

def insertSlackData(userID, userText, messageTimestampUnix, messageTimestamp, watsonNLUResult,databaseName):
    mongoClient = pymongo.MongoClient("localhost", 27017)

    mongoDatabase = mongoClient["slackDatabase"]

    slackChannelData = mongoDatabase[databaseName]
    entryValues = {
        "user_id": userID,
        "user_text": userText,
        "message_timestamp_unix": messageTimestampUnix,
        "message_timestamp": messageTimestamp,
        "watson_NLU_result": watsonNLUResult
        }
    slackChannelData.insert_one(entryValues)
    logging.debug("Added to the database: %s", databaseName)

def main(slackValues, watsonValues, databaseTeamName):
    slackEventUserIDValues = slackValues.get("user", None) or slackValues["user"]
    slackEventsTextValues = slackValues.get("text", None) or slackValues["text"]
    slackEventsTimestampValues = slackValues.get("ts", None) or slackValues["ts"]

    timestampConverted = time.ctime(float(slackEventsTimestampValues))
    #slackTextImproved = re.sub("[\<\[].*?[\>\]]", "", slackEventsTextValues)
    logging.debug("Using database: %s", databaseTeamName)
    watsonNLUString = watsonValues
    insertSlackData(slackEventUserIDValues, slackEventsTextValues, slackEventsTimestampValues, timestampConverted, watsonNLUString, databaseTeamName)


