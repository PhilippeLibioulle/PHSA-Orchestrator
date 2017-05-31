import paho.mqtt.client as mqtt
import time
from durable.lang import *

with ruleset('KitchenLighting'):
    # antecedent
    @when_all((m.Source == '22-A1-71') & (m.Group == 3 )& (m.Command == 'On' ))
    def turn_on(c):
        # consequent
        print ('User pressed one time on A')
        sendMessage('GLX/KitchenLighting/ToDo','0B:0A:0A:32:0A:0A')
        print('End of A ')
    # antecedent
    @when_all((m.Source == '22-A1-71') & (m.Group == 3 )& (m.Command == 'Off' ))
    def turn_off(c):
        # consequent
        print ('User pressed again on A')
        sendMessage('GLX/KitchenLighting/ToDo','0B:00:0B:00:00:00')
        print('End of A')
    # when the exception property exists
    @when_all(+s.exception) 
    def second(c):
        print('*** error ***')
        print(c.s.exception)
        c.s.exception = None
    # on ruleset start
    @when_start
    def start(host):
        print('@when_start - begin')               
        print('@when_start - end')
    # utilities
    def sendMessage(destination, payload):
        global flag 
        client = mqtt.Client()
        client.username_pw_set(username='kitto',password='kitty')
        flag = 1
        client.on_connect = on_connect
        client.connect('localhost', 1883, 60)
        #while flag == 1:
        #   print('Waiting for connection...')
        #   time.sleep(0.01)
        time.sleep(0.5)
        print('Destination: ' + destination)
        print('Payload: ' + payload)
        flag = 1
        client.on_publish = on_publish
        client.publish(destination, payload)
        #while flag == 1:
        #   print('Waiting for message to be added...')
        #   time.sleep(0.01)
        time.sleep(0.5)
        client.disconnect()
    def on_connect(client, userdata, flags, rc):        
        print('Connected to MQTT broker')
        flag = 0   
    def on_publish(client, userdata, result):
        print('Message added to queue')
        flag = 0
run_all()
