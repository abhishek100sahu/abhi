import paho.mqtt.client as paho

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('3f27288bc0334a22befbdf52138f9c22.s1.eu.hivemq.cloud', 8883)
client.subscribe('encyclopedia/#', qos=1)

client.loop_forever()