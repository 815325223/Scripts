#!/usr/bin/env python

import signal
import pika

signal.signal(signal.SIGPIPE, signal.SIG_DFL)
signal.signal(signal.SIGINT, signal.SIG_DFL)

credentials = pika.PlainCredentials('serverworld', 'VdFrq2lW')
connection = pika.BlockingConnection(pika.ConnectionParameters(
                                     'localhost',
                                     5672,
                                     '/my_vhost',
                                     credentials))

channel = connection.channel()
channel.queue_declare(queue='Hello_World')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='Hello_World',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
