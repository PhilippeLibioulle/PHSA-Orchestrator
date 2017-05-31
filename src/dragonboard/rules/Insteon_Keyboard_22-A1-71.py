import serial, json, time, paho.mqtt.client as mqtt, requests

def configureLed(position, red, green, blue):
    uno.write('\x02')
    uno.write('\x30')
    uno.write(position) 
    uno.write(red)
    uno.write(green)
    uno.write(blue)
    uno.write('\xFF')
    uno.write('\xFF')
    uno.write('\xFF')
    uno.write('\xFF')

def on_connect(mosq, obj, rc):    
    print("Connect rc: " + str(rc))    
    if rc != 0:
       configureLed('\x07','\xFF','\x00','\x00')
    else:        
       configureLed('\x07','\x00','\xFF','\x00')       
       try:
           mqttc.subscribe("GLI/22-A1-71/WishList")
       except Exception, e:
           print("Cannot connect to MQTT broker at %s:%d: %s" % (cf.hostname, int(cf.port), str(e)))
           print('LED 1 to RED 100 %')
           configureLed('\x06','\xFF','\x00','\x00')      

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))   
    configureLed('\x06','\x00','\xFF','\x00')  
	
def on_message(mosq, obj, msg):    
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))  
     
    prefix, id, qtype = msg.topic.split("/")
    parsed_json = json.loads(str(msg.payload))
    group = parsed_json['Group']
    if parsed_json['Command'] == 11:
       command = "On"
    elif parsed_json['Command'] == 12:
       command = "AltOn"
    elif parsed_json['Command'] == 13:
       command = "Off"
    elif parsed_json['Command'] == 14:
       command = "Off"
    else:
       command = "Unknown"                   
    parameters = parsed_json['Parameters']
       
    output_json = json.dumps({'Source': id, 'Group': group, 'Command': command, 'Parameters': parameters})  
    print(output_json)
       
    res = requests.post('http://localhost:5000/KitchenLighting/events', data=output_json)
    
    # {"Source": "22-A1-71", "Command": "Off", "Group": 3, "Parameters": 0}
        
    print(res.text)
    
    configureLed('\x05','\x00','\xFF','\x00')  
    time.sleep(1)
    configureLed('\x05','\x00','\x00','\x00')  

def on_log(mosq, obj, level, string):
    print(string)
	
uno = serial.Serial('/dev/tty96B0', 9600)
uno.write('')
time.sleep(5)

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
# mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Connect
try:
    mqttc.username_pw_set(username="kitto",password="kitty")
    mqttc.connect("localhost", 1883, 60)
except Exception, e:
    print("Cannot connect to MQTT broker at %s:%d: %s" % (cf.hostname, int(cf.port), str(e)))
    configureLed('\x07','\xFF','\x00','\x00')
    sys.exit(2)

# Continue the network loop
mqttc.loop_forever()

