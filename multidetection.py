#!/usr/bin/env python2
import threading
import paho.mqtt.client as paho
import json

_multiDetectionsHolder = []
_sessions = {}

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

def handleMultiDetection(self):
   print('handleMultiDetection')
   if len(_multiDetectionsHolder) <= 1:
      _multiDetectionsHolder = []
      return

   for sessionId in self._sessions.keys():
      message = _sessions[sessionId]
      payload = json.loads(message.payload)
      if payload['siteId'] != _multiDetectionsHolder[0]:
         client.publish('hermes/dialogueManager/endSession', json.dumps({'sessionId': sessionId}))

   _multiDetectionsHolder = []

def onHotwordDetected(self, data, msg):
   print('onHotwordDetected')
   payload = json.loads(msg.payload)

   if len(_multiDetectionsHolder) == 0:
      threading.Timer(interval=0.3, function=self.handleMultiDetection).start()

   _multiDetectionsHolder.append(payload['siteId'])

def onSessionStarted(self, data, msg):
   print('onSessionStarted')
   sessionId = json.loads(msg.payload)['sessionId']
   _sessions[sessionId] = msg

client = paho.Client("multi")
client.connect(MQTT_IP_ADDR, MQTT_PORT, 60)
client.subscribe("hermes/#")
client.message_callback_add('hermes/hotword/default/detected', onHotwordDetected)
client.message_callback_add('hermes/dialogueManager/sessionStarted', onSessionStarted)
client.loop_forever()

