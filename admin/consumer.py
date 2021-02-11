import json
import os

import django
import pika

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

params = pika.URLParameters("amqps://dsayffdo:MJQ5i-zz5w5kMYGt5jCdLCrJTyjt4icc@hawk.rmq.cloudamqp.com/dsayffdo")

connetion = pika.BlockingConnection(params)

channel = connetion.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Recieve in-admin')
    data = json.loads(body)
    print(data)
    product = Product.objects.get(id=data)
    product.likes += 1
    product.save()
    print('Product likes increased')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
