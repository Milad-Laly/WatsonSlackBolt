import os

from ibm_watson import ToneAnalyzerV3, NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions

def watsonNLU(textSlack):
    #Include Watson API key
    authenticator = IAMAuthenticator(apikey=os.environ['IBM_NLU_KEY'])
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-01-12', authenticator=authenticator)

    #Include instance URL
    natural_language_understanding.set_service_url(service_url=os.environ['IBM_NLU_URL'])
    response = natural_language_understanding.analyze(text=textSlack,
    features=Features(sentiment=SentimentOptions(document=True), emotion=EmotionOptions(document=True))).get_result()
    # features=Features(entities=EntitiesOptions(emotion=True, sentiment=True, limit=2), keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2))).get_result()

    return response