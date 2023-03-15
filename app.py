#!/usr/bin/env -S python3 -u

import paho.mqtt.client as mqtt
import traceback

import time

import os
import json
import sys
import random
from threading import Thread


# python app2.py --mqtt_host=iot.fr-par.scw.cloud --mqtt_user=
mqtt_client_scaleway = mqtt.Client()
mqtt_client_wirenboard = mqtt.Client()

blink_flag = False

def int_error(exception=None):
  traceback.print_exc()
  print(f"Exception Name: {type(exception).__name__}")
  print(f"Exception Desc: {exception}")
  #os.system('reboot')



def parse_message(topic, payload):
  global blink_flag
  #print(f"topic: {topic}, payload: {payload}")
  if topic == "goodwan/6226":
    print(payload)
    json_object = json.loads(payload)
    if json_object["data"]["Ch3"] == 1:
      blink_flag = True
      #mqtt_client_wirenboard.publish("/devices/wb-mr6c_20/controls/K1/on", "1")
    elif json_object["data"]["Ch3"] == 0:
      blink_flag = False
      #mqtt_client_wirenboard.publish("/devices/wb-mr6c_20/controls/K1/on", "0")



def on_connect_scaleway(client, userdata, flags, rc):
  print("Connected scaleway with result code "+str(rc))
  mqtt_client_scaleway.subscribe("#")

def on_connect_wirenboard(client, userdata, flags, rc):
  print("Connected wirenboard with result code "+str(rc))
  #mqtt_client_scaleway.subscribe("#")

def on_message_scaleway(client, userdata, msg):
  if msg.retain == False:
    try:
      parse_message(msg.topic, msg.payload.decode("utf-8"))
    except Exception as exception:
      int_error(exception)
  #print(msg.topic + ": " + msg.payload.decode("utf-8"))

def on_disconnect(client, userdata, msg):
  print("disconnected, exit")
  int_error()

def mqtt_scaleway():
  mqtt_client_scaleway.on_connect = on_connect_scaleway
  mqtt_client_scaleway.on_message = on_message_scaleway
  mqtt_client_scaleway.on_disconnect = on_disconnect
  mqtt_client_scaleway.username_pw_set("e316dca2-308a-4aaa-a8a5-c4604048e876")
  mqtt_client_scaleway.connect("iot.fr-par.scw.cloud", 1883, 10)
  time.sleep(5)
  mqtt_client_scaleway.loop_start()

def mqtt_wirenboard():
  mqtt_client_wirenboard.on_connect = on_connect_wirenboard
  mqtt_client_wirenboard.on_disconnect = on_disconnect
  mqtt_client_wirenboard.connect("10.255.131.56", 1883, 10)
  time.sleep(5)
  mqtt_client_wirenboard.loop_start()

def blink_wb():
  while True:
    time.sleep(0.1)
    while blink_flag == True:
      mqtt_client_wirenboard.publish("/devices/wb-mr6c_20/controls/K1/on", "0")
      time.sleep(0.5)
      mqtt_client_wirenboard.publish("/devices/wb-mr6c_20/controls/K1/on", "1")
      time.sleep(0.5)


def main():
  Thread(target=mqtt_scaleway).start()
  Thread(target=mqtt_wirenboard).start()
  Thread(target=blink_wb).start()
  while True:
    time.sleep(1)



if __name__ == "__main__":
  main()
