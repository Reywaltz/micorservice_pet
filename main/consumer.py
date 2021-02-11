import pika
import json
from main import Product, db

params = pika.URLParameters("amqps://dsayffdo:MJQ5i-zz5w5kMYGt5jCdLCrJTyjt4icc@hawk.rmq.cloudamqp.com/dsayffdo")

connetion = pika.BlockingConnection(params)

channel = connetion.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('Recieve in-main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product-created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        try:
            db.session.commit()
            print('Product created')
        except Exception as e:
            print(e)
            

    elif properties.content_type == 'product-updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.title = data['image']
        try:
            db.session.commit()
        except Exception as e:
            print(e)
        print('Product updated')

    
    elif properties.content_type == 'product-deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
