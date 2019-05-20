#!/usr/bin/env python3
import threading
import paho.mqtt.client as paho
import json
import mqtt_client
from pprint import pprint

global _multiDetectionsHolder
_multiDetectionsHolder = []
_sessions = {}

def handleMultiDetection():
   print('handleMultiDetection')
   global _multiDetectionsHolder
   pprint(_multiDetectionsHolder)
   if len(_multiDetectionsHolder) <= 1:
      _multiDetectionsHolder = []
      return

   for sessionId in _sessions.keys():
      message = _sessions[sessionId]
      payload = json.loads(str(message.payload.decode("utf-8", "ignore")))
      if payload['siteId'] != _multiDetectionsHolder[0]:
         client.publish('hermes/dialogueManager/endSession', json.dumps({'sessionId': sessionId}))

   _multiDetectionsHolder = []


def onHotwordDetected(self, data, msg):
   print('onHotwordDetected')
   global _multiDetectionsHolder
   pprint(_multiDetectionsHolder)
   payload = json.loads(str(msg.payload.decode("utf-8", "ignore")))

   if len(_multiDetectionsHolder) == 0:
      threading.Timer(interval=0.3, function=handleMultiDetection).start()

   _multiDetectionsHolder.append(payload['siteId'])


def onSessionStarted(self, data, msg):
   print('onSessionStarted')
   global _multiDetectionsHolder
   pprint(_multiDetectionsHolder)
   sessionId = json.loads(str(msg.payload.decode("utf-8", "ignore")))['sessionId']
   _sessions[sessionId] = msg


client = paho.Client("multi")
client.username_pw_set(mqtt_client.get_user(), mqtt_client.get_pass())
client.connect(mqtt_client.get_addr(), mqtt_client.get_port(), 60)
client.subscribe([("hermes/hotword/default/detected", 0), ("hermes/dialogueManager/sessionStarted", 0)])
client.message_callback_add('hermes/hotword/default/detected', onHotwordDetected)
client.message_callback_add('hermes/dialogueManager/sessionStarted', onSessionStarted)
client.loop_forever()

