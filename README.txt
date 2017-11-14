# 作业：基于rpc的主机管理

### 作者介绍：
- author：王武功
- My Blog : http://bujuhandong.blog.51cto.com/1443515/1981362


### 程序结构：
```
rpc
├── client
│   ├── client_run.py
│   ├── __init__.py
│   ├── __pycache__
│   │   └── setting.cpython-36.pyc
│   └── setting.py
├── README.txt
├── rpc.png
└── server
    ├── __init__.py
    ├── __pycache__
    │   └── setting.cpython-36.pyc
    ├── server_run.py
    └── setting.py

```

	
### 运行环境：
    Python3.0或以上版本环境均可。

### 配置文件
	rpc/client/setting和rpc/server/setting分别为客户端和服务端的配置配置文件。
	两个配置文件都包含以下几项：
	rabbitmq_user='u1'   #该选项为rabbitmq的连接用户，该用户需要有virtual host / 的读、写、配置权限。
	rabbitmq_pw='u1'	 #该选项为rabbitmq的连接用户密码
	rabbitmq_ip='10.100.119.145'	#该选项为rabbitmq的ip地址。
	rabbitmq_port=5672		#该选项为rabbitmq的端口
	
	另外server_local_ip选项仅需服务端配置。
	server_local_ip="10.100.119.145"	#该选项为server端的ip地址，也就是客户端连接的ip地址。该选项仅服务端配置。
	
### 执行方法：
	将server目录上传到server端，然后运行：
	cd server/
	python server_run.py
	
	将client目录放在client端，然后运行：
	cd client/
    python client_run.py
	
### 使用方法：
    系统支持以下3个命令：
	run "cmd xxxx” ip1 ip2 ....
	check task_id
	exit
	
	其中:
	run...：由三部分构成,第一部分为“run"字符，第二部分为命令，必须写在双引号或单引号里面,第三部分为ip地址，至少写一个，
		该ip地址为server的ip，也可以为域名。
	check...: 由两部分构成，第一部分为"check”字符，第二部分为task_id，该id由每个run命令执行完之后系统会返回。
		每次只能写一个task_id。
	exit： 退出命令。
	
	
	
	