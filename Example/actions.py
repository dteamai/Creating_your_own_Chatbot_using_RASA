from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import UserUtteranceReverted
from keras.models import Model, Sequential
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Flatten, Reshape , SeparableConv2D, Conv2DTranspose, BatchNormalization, Dropout
from keras.optimizers import adam
from keras.models import model_from_json
from sklearn.neighbors import NearestNeighbors
from sklearn.externals import joblib
from sorting import  find_topk_unique
import h5py
from PIL import Image
import requests
import numpy as np
import h5py
from PIL import Image
# import requests
import numpy as np
import cv2
# import urllib3
from skimage import io
# from StringIO import StringIO

print('runnning..............')
from apixu.client import ApixuClient

class ActionWeather(Action):
    def name(self):
        return 'action_weather'
    
    def run(self, dispatcher, tracker, domain):
        # from apixu.client import ApixuClient
        api_key = '6941d2731345403db6481426182012'
        client = ApixuClient(api_key)
        # # try:
        loc = tracker.get_slot('location')
        if loc != None:

            try:
                current = client.getCurrentWeather(q=loc)
            except:
                response = "Sorry I unable fetch weather, Some problem in fetching the data, Please retry or try some other location."
                dispatcher.utter_message(response)
                return [SlotSet('location',None)]
            # country   = current['location']['country']
            city      = current['location']['name']
            condition = current['current']['condition']['text']
            temperature_c = current['current']['temp_c']
            humidity  = current['current']['humidity']
            wind_mph  = current['current']['wind_mph']

            response = """Thanks for waiting.It is currently {} in {} at the moment. The temperature is {} degrees,
                            the humidity is {} and the wind speed is {}mph,""".format(condition,city,temperature_c,humidity,wind_mph)
            
                # response = 'testing'
            dispatcher.utter_message(response)
            return [SlotSet('location',None)]
        else:
            response = """Sorry ,I can't fetch,Please try someother location or rephases and type it"""      
                
            dispatcher.utter_message(response)
            return [SlotSet('location',None)]
        
class ActionDefaultFallback(Action):
    def name(self):
        return 'action_default_fallback'

    def run(self, dispatcher, tracker, domain):
        # response = "I'm sorry, but I didn't understand you. Could you please rephrase what you just said?"
        dispatcher.utter_template("utter_default", tracker,
                            silent_fail=True)
        message = tracker.latest_message    
        print(message,'.........................')
        return [UserUtteranceReverted()]
        # dispatcher.utter_message(response)
        # return []

    