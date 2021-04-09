import logging

logging.basicConfig(level=logging.DEBUG)

import os
import json

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from watsonNLU import watsonNLU

# Install the Slack app and get xoxb- token in advance
app = App(token="BOT TOKEN HERE")


@app.shortcut("tone_analysis_action")
def open_modal(ack, shortcut, client, logger):
    # Acknowledge shortcut request
    ack()
    try:
        # Call the views.open method using the WebClient passed to listeners
        #Call variable into modal
        testVariable = "This is a test"

        #Gets text value from input
        #Pass variable into database.py
        event = shortcut["message"]
        textValue = event.get("text", None) or event["text"]

        #Calls watsonNLU for sentiment
        watsonSentimentText = watsonNLU(textValue)

        watsonSentimentDocumentScore = watsonSentimentText["sentiment"]["document"]["score"]
        watsonSentimentDocumentTone = watsonSentimentText["sentiment"]["document"]["label"]
        
        result = client.views_open(
            trigger_id=shortcut["trigger_id"],
            view={
                "type": "modal",
                "title": {"type": "plain_text", "text": "Watson NLU Analysis"},
                "close": {"type": "plain_text", "text": "Close"},
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "The tone of this text is " + watsonSentimentDocumentTone + " and the score is: " + str(watsonSentimentDocumentScore*100)+"%",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":  "twoText" + testVariable + " OOOO" ,
                        },
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": json.dumps(watsonSentimentText, indent=2),
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
    SocketModeHandler(app, "APP TOKEN HERE").start()