
from durable.lang import * 
import paho.mqtt.client
import time

with ruleset('test'):
    @when_all(m.subject == 'World')
    def say_hello(c):
        print ('Hello {0}'.format(c.m.subject))
	client2 = paho.mqtt.client.Client()
        client2.username_pw_set("kitto", "kitty")
	print('Connect...')
        print(client2.connect("localhost", 1885, 60))
	time.sleep(1)
	print('Publish...')
	print(client2.publish("test", "Hello MQTT2!"))
	time.sleep(1)
	print('Disconnect...')
	client2.disconnect()
	time.sleep(1)
	print('doneall')
    @when_all(+s.exception)
    def second(c):
        print(c.s.exception)
        c.s.exception = None
    @when_start
    def start(host):    
        print('Start')	    
	client = paho.mqtt.client.Client()
        client.username_pw_set("kitto", "kitty")
	print('Connect at startup...')
        print(client.connect("localhost", 1885, 60))
	time.sleep(1)
	print('Publish at startup...')
	print(client.publish("test", "At startup"))
	time.sleep(1)
	print('Disconnect at startup...')
	print('Startup done')
	
run_all()