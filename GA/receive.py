#!/usr/bin/env python3
import pika
import subprocess

# RabbitMQ连接设置
credentials = pika.PlainCredentials('<USERNAME>', '<PASSWORD>')
connection_params = pika.ConnectionParameters(host='localhost', port='5672', credentials=credentials, virtual_host='<VHOST>')
connection = pika.BlockingConnection(connection_params)

# 声明队列并获取队列中的消息
channel = connection.channel()
channel.queue_declare(queue='folder_queue')
method_frame, header_frame, body = channel.basic_get(queue='folder_queue')

if method_frame:
    # 将RabbitMQ消息体转换为文件夹名称
    folder_name = body.decode()
    print(f"Received folder name: {folder_name}")
    
    # 给文件夹分配适当的权限
    folder_path = f"{folder_name}"
    subprocess.run(["setfacl", "-R", "-m", "<POLICY>", folder_path])

    # 确认消息已被处理
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
else:
    print('No message in queue')
    
connection.close()
