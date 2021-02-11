import pika
import json

params = pika.URLParameters("amqps://dsayffdo:MJQ5i-zz5w5kMYGt5jCdLCrJTyjt4icc@hawk.rmq.cloudamqp.com/dsayffdo")

connetion = pika.BlockingConnection(params)

channel = connetion.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)