#!/usr/bin/env python3
import pika

credentials = pika.PlainCredentials('<USERNAME>', '<PASSWORD>')
connection_params = pika.ConnectionParameters(host='localhost', port='5672', credentials=credentials, virtual_host='<VHOST>')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()
channel.queue_declare(queue='folder_queue')
channel.basic_publish(
    exchange='',
    routing_key='folder_path',
    body='<FOLDER>')
connection.close()
