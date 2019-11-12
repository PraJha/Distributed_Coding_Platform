import os, sys, socket, time, csv, pickle, subprocess
from threading import Thread
from SocketServer import ThreadingMixIn

myIPAddr = ""

def myIP():
    global myIPAddr
    bashCommand = 'hostname -I | awk \'{print $1}\''
    IPAddr = subprocess.check_output(['bash','-c', bashCommand])
    myIPAddr = IPAddr.strip('\n')

myIP()

all_connected_node=set([myIPAddr])#Set of all unique ips connected to current node.

def broadcast_send():
	broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	# Set a timeout so the socket does not block
	# indefinitely when trying to receive data.
	# broadcast.settimeout(5)
	broadcast.bind(("", 44444))

	#to get it's own IP Address
	# bashCommand = "hostname -I | awk '{print $1}'"
	# message = subprocess.check_output(['bash','-c', bashCommand])
	message = "Hi, I want to connect!!"
	# print message
	# while True:
	broadcast.sendto(message, ('<broadcast>', 37020))
	# print("message sent!")
	# broadcast.settimeout(2)


#same as receive
def broadcast_listen():
	global all_connected_node
	sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sNode.bind(("", 37020))
	while True:
	    # continuously listen for broadcast msgs
	    # print "Hi"
	    data, addr = sNode.recvfrom(5096)
	    if data != '' and not addr[0] in all_connected_node:
	    	# sNode.sendto(myIPAddr, addr)
	    	all_connected_node.add(addr[0])
	    	f=open('node_ip','w+')
	    	for i in all_connected_node:
	    		if i!=myIPAddr:
	    			f.write(str(i))
	    			f.write("\n")
	    	f.close()
	    	print "Receive New Connection : ",addr[0]
	    	time.sleep(4)
	    	sendMsgUDP(37020, addr[0],"prab")


if __name__ == '__main__':
	listen_thread = Thread(target=broadcast_listen, name='broadcast listen')
	listen_thread.start()
	broadcast_send()


def sendMsgUDP(port, ip, msg):
    serverAddrPort = (ip, port) 
    UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)   
    UDPClientSocket.sendto(msg, serverAddrPort)
    UDPClientSocket.close()