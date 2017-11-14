import setting,re
import pika
import uuid
import time,subprocess


rb_user = setting.rabbitmq_user
rb_pw = setting.rabbitmq_pw
rb_ip = setting.rabbitmq_ip
rb_port = setting.rabbitmq_port

credentials = pika.PlainCredentials(rb_user, rb_pw)

class Sshrpc(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rb_ip,port=rb_port,virtual_host='/',credentials=credentials))
        self.channel = self.connection.channel()

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            print(body.decode())
    def call(self, n,routing_key_list):
        self.corr_id = str(uuid.uuid4())
        self.channel.queue_declare(queue=self.corr_id)
        for i in routing_key_list:
            self.channel.basic_publish(exchange='',
                                       routing_key=i,
                                       properties=pika.BasicProperties(
                                           reply_to=self.corr_id,
                                           correlation_id=self.corr_id,
                                       ),
                                       body=n)
        return self.corr_id
    def check_result(self,task_id):
        try:
            self.channel.basic_consume(self.on_response, no_ack=True,
                                       queue=task_id)
            self.connection.process_data_events()
            self.delete_queue(task_id)
        except:
            print("The task_id:%s not exists." % task_id)

    def delete_queue(self,task_id):
        self.channel.queue_delete(queue=task_id)


def main():
    print("Welcome to use this tool.")
    cmd_start_tuple=("run","check")
    ssh_rpc = Sshrpc()
    while True:
        cmd_str=input(">>:")
        if len(cmd_str) == 0:continue
        if cmd_str.lower().startswith("run"):
            cmd_list = re.split('\"|\"|\'|\'', cmd_str)
            if (cmd_list[0].lower().strip() in cmd_start_tuple and len(cmd_list) == 3):
                cmd = cmd_list[1]
                ip_list = cmd_list[2].split()
                response = ssh_rpc.call(cmd, ip_list)
                print("The taks_id is: \033[31;1m%s\033[0m" % response)
            else:
                print("\033[31;1mWrong command,Please retry.\033[0m")
        elif cmd_str.lower().startswith("check"):
            cmd_list = cmd_str.split()
            if (cmd_list[0].lower().strip() in cmd_start_tuple and len(cmd_list) == 2):
                ssh_rpc.check_result(cmd_list[1])
            else:
                print("\033[31;1mWrong command,Please retry.\033[0m")
        elif cmd_str.lower().startswith("exit"):
            cmd_list = cmd_str.split()
            if cmd_list[0].lower().strip() == "exit" and len(cmd_list) == 1:
                exit("Thanks to use this tool.")
            else:
                print("\033[31;1mWrong command,Please retry.\033[0m")
        else:
            print("\033[31;1mWrong command,Please retry.\033[0m")

if __name__ == '__main__':
    main()
