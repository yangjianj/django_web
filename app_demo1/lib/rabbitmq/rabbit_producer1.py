# -*- coding: utf-8 -*-
import pika,datetime

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()  # 生成管道，在管道里跑不同的队列

# 声明queue
channel.queue_declare(queue='hello1')

# n RabbitMQ a message can never be sent directly to the queue,it always needs to go through an exchange.
# 向队列里发数据
timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
channel.basic_publish(exchange='',   # 先把数据发给exchange交换器,exchage再发给相应队列
routing_key = 'hello1',   # 向"hello1'队列发数据
body = timestamp+'HelloWorld!!1111')     # 发的消息
print(timestamp+'HelloWorld!!1111')
connection.close()