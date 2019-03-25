#!/usr/bin/env python2
import threading
import paho.mqtt.client as paho
import json
from pprint import pprint

global _multiDetectionsHolder
_multiDetectionsHolder = []
_sessions = {}

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883

def handleMultiDetection():
   print('handleMultiDetection')
   global _multiDetectionsHolder
   pprint(_multiDetectionsHolder)
   if len(_multiDetectionsHolder) <= 1:
      _multiDetectionsHolder = []
      return

   for sessionId in _sessions.keys():
      message = _sessions[sessionId]
      payload = json.loads(message.payload)
      if payload['siteId'] != _multiDetectionsHolder[0]:
         client.publish('hermes/dialogueManager/endSession', json.dumps({'sessionId': sessionId}))

   _multiDetectionsHolder = []

def onHotwordDetected(self, data, msg):
   print('onHotwordDetected')
   global _multiDetectionsHolder
   pprint(_multiDetectionsHolder)
   payload = json.loads(msg.payload)

   if len(_multiDetectionsHolder) == 0:
      threading.Timer(interval=0.3, function=handleMultiDetection).start()

   _multiDetectionsHolder.append(payload['siteId'])

def onSessionStarted(self, data, msg):
   print('onSessionStarted')
   global _multiDetectionsHolder
   pprint(_multiDetectionsHolder)
   sessionId = json.loads(msg.payload)['sessionId']
   _sessions[sessionId] = msg

client = paho.Client("multi")
client.connect(MQTT_IP_ADDR, MQTT_PORT, 60)
client.subscribe([("hermes/hotword/default/detected", 0), ("hermes/dialogueManager/sessionStarted", 0)])
client.message_callback_add('hermes/hotword/default/detected', onHotwordDetected)
client.message_callback_add('hermes/dialogueManager/sessionStarted', onSessionStarted)
client.loop_forever()

