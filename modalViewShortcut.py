import logging

logging.basicConfig(level=logging.DEBUG)

import os
import json

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from watsonNLU import watsonNLU

import database

app = App(token="ENTER XOXB TOKEN")

@app.event({"type": "message", "subtype": None})
def textRetrival(body):
    event = body["event"]
    slackText = event.get("text", None) or event["text"]
    watsonAnalysis = watsonNLU(slackText)
    database.main(event,watsonAnalysis,databaseTeamTable)

@app.shortcut("tone_analysis_action")
def watsonShortcut(ack, shortcut, client, logger):
    # Acknowledge shortcut request
    ack()
    try:
        #Gets text value from input
        event = shortcut["message"]
        textValue = event.get("text", None) or event["text"]

        #Calls watsonNLU for sentiment
        watsonAnalysis = watsonNLU(textValue)

        #Sentiment Options
        watsonSentimentDocumentScore = watsonAnalysis["sentiment"]["document"]["score"] 
        watsonSentimentScoreRounded = "{:.2%}".format(watsonSentimentDocumentScore)

        watsonSentimentDocumentTone = watsonAnalysis["sentiment"]["document"]["label"]

        #Emotion Options
        watsonEmotionSadnessScore = watsonAnalysis["emotion"]["document"]["emotion"]["sadness"]
        watsonEmotionSadnessRounded = "{:.2%}".format(watsonEmotionSadnessScore)

        watsonEmotionJoyScore = watsonAnalysis["emotion"]["document"]["emotion"]["joy"]
        watsonEmotionJoyRounded = "{:.2%}".format(watsonEmotionJoyScore)

        watsonEmotionFearScore = watsonAnalysis["emotion"]["document"]["emotion"]["fear"]
        watsonEmotionFearRounded = "{:.2%}".format(watsonEmotionFearScore)
        
        watsonEmotionDisgustScore = watsonAnalysis["emotion"]["document"]["emotion"]["disgust"]
        watsonEmotionDisgustRounded = "{:.2%}".format(watsonEmotionDisgustScore)
        
        watsonEmotionAngerScore = watsonAnalysis["emotion"]["document"]["emotion"]["anger"]
        watsonEmotionAngerRounded = "{:.2%}".format(watsonEmotionAngerScore)


        
        result = client.views_open(
            trigger_id=shortcut["trigger_id"],
            view={
                "type": "modal",
                "title": {"type": "plain_text", "text": "Watson NLU Analysis"},
                "close": {"type": "plain_text", "text": "Close"},
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Sentiment of Text"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "The tone of this text is *" + watsonSentimentDocumentTone + "* and the score is " + str(watsonSentimentScoreRounded)
                        }
                    }, 
                    #Maybe add sentence to improve mood if negative
                    {
                        "type": "divider"
                    },
                    {
			            "type": "header",
			            "text": {
				            "type": "plain_text",
				            "text": "Emotion of Text"
			            }
		            },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":  "The *sadness* :cry: *score* of the text is " + str(watsonEmotionSadnessRounded)
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":  "The *joyfulness* :joy: *score* of the text is " + str(watsonEmotionJoyRounded)
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":  "The *fearfulness* :fearful: *score* of the text is " + str(watsonEmotionFearRounded)
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":  "The *disgusted* :nauseated_face: *score* of the text is " + str(watsonEmotionDisgustRounded)
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":  "The *angerness* :rage: *score* of the text is " + str(watsonEmotionAngerRounded)
                        },
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": json.dumps(watsonAnalysis, indent=2)
                            }
                        ],
                    },
                ],
            },
        )
        logger.info(result)

    except Exception as e:
        logger.error("Error creating conversation: {}".format(e))

if __name__ == "__main__":
    # export SLACK_APP_TOKEN=xapp.....
    # export SLACK_BOT_TOKEN=xoxb.....
    while True:
        try:
            print("Welcome to Slack Tone analyzer")
            print("Enter the team name currently on the workshop: ")
            databaseTeamTable = input()
            if databaseTeamTable[0] != ' ':
                SocketModeHandler(app, "ENTER XAPP TOKEN").start()
            print("Invalid Database Table name entered")
        except Exception as e:
            print(e)
