import paho.mqtt.client as paho
import time

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.connect('3f27288bc0334a22befbdf52138f9c22.s1.eu.hivemq.cloud', 8883)
client.loop_start()

while True:
    temperature = read_from_imaginary_thermometer()
    (rc, mid) = client.publish('encyclopedia/temperature', str(temperature), qos=1)
    time.sleep(30)