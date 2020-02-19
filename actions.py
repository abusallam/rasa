# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("Hello World!")
#
#         return []

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import country_converter as coco
import json

class ActionWeather(Action):
	def name(self):
		return 'action_retrive_news'
		
	def run(self, dispatcher, tracker, domain):
            from newsapi import NewsApiClient
            
            # Init
            newsapi = NewsApiClient(api_key='f908755783e34e738776e64eeacfbd17')

            print(tracker.get_slot('country'))

            country = tracker.get_slot('country')
            
            country_iso2 = coco.convert(names=country, to='ISO2', not_found=None)

            print(country_iso2)

            country_iso2_low = country_iso2.lower()

            # /v2/top-headlines
            top_headlines = newsapi.get_top_headlines(#q=country,
                                                    #sources='bbc-news,the-verge',
                                                    country=country_iso2_low)

            news_json = json.dumps(top_headlines)

            list_articles = json.loads(news_json)

            for articles in list_articles['articles']:
                print('Author: ' + str(articles['author']))
                print('Source: ' + str(articles['source']['name']))
                print('Title: ' + str(articles['title']))
                print('URL: ' + str(articles['url']) + "\n")
                print("############################################################")
                dispatcher.utter_message('**Source:** ' + str(articles['source']['name']) + '\n **Title:** ' + str(articles['title']) + '\n **URL:** ' + str(articles['url']) + '\n')
