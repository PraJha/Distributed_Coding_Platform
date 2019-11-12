# server2.py
import os, sys, socket, time, csv, subprocess
from threading import Thread
from SocketServer import ThreadingMixIn

myIPAddr = ""

def myIP():
    global myIPAddr
    bashCommand = 'hostname -I | awk \'{print $1}\''
    IPAddr = subprocess.check_output(['bash','-c', bashCommand])
    myIPAddr = IPAddr.strip('\n')

# IP from Organizer_ip
f = open("Organizer_ip.txt", "r")
ip = f.read()
TCP_IP = myIPAddr #Current Machine IP
TCP_PORT = 9001
BUFFER_SIZE = 1024

def rec_message(s):
    data = s.recv(1024)
    print(data)
    return data

def send_message(s,val):
    s.sendall(val)

def send_file(s,filename):
    f = open(filename,'rb')
    while True:
        l = f.read(BUFFER_SIZE)
        while (l):
            s.send(l)
            # print('Sent ',repr(l))
            l = f.read(BUFFER_SIZE)
        if not l:
            f.close()
            s.close()
            break

# ip = get('https://api.ipify.org').text
def main():

	tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpsock.bind((TCP_IP, TCP_PORT))
	print (TCP_IP)
	threads = []

	while True:
		tcpsock.listen(5)
		print ("Waiting To Submit File...")
		(conn, (ip,port)) = tcpsock.accept()
		print ('Got connection from ', (ip,port))

		send_message(conn,"SUBMIT")
		send_file(conn,"Solution.zip")
	    #Writing the details of a connected machine into a node_ip file
	    # f=open('node_ip','a')#Append to the existing file
	    # f.write(ip)
	    # f.write(" ")
	    # f.write(str(port))
	    # f.write("\n")
	    # f.close()

		# newthread = ClientThread(ip,port,conn)
		# newthread.start()
		# threads.append(newthread)

	# for t in threads:
	# 	t.join()

if __name__ == '__main__':
	myIP()
	main()
