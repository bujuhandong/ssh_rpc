import setting,re
import pika
import time,subprocess


rb_user = setting.rabbitmq_user
rb_pw = setting.rabbitmq_pw
rb_ip = setting.rabbitmq_ip
rb_port = setting.rabbitmq_port
routting_key = setting.server_local_ip


credentials = pika.PlainCredentials(rb_user, rb_pw)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rb_ip,port=rb_port,virtual_host='/',credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue=routting_key)


def exec_cmd(cmd):
    result=subprocess.getoutput(cmd)
    result=routting_key+" ======>\n\n"+result+"\n======end======\n"
    return result


def on_request(ch, method, props, body):
    n = body.decode()
    print("exec_cmd(%s)" % n)
    response = exec_cmd(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue=routting_key)

    print("Awaiting RPC requests")
    channel.start_consuming()

if __name__ == '__main__':
    main()