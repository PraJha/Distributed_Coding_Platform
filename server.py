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

TCP_IP = myIPAddr#Current Machine IP
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
            #print('Sent ',repr(l))
            l = f.read(BUFFER_SIZE)
        if not l:
            f.close()
            s.close()
            break

def rec_file(s,filename):
	print("In rec_file server.py")
	f=open(filename,"w")
	print ('file opened')
	while True:
		#print('receiving data...')
		data = s.recv(BUFFER_SIZE)
		print('data=%s', (data))
		if not data:
			f.close()
			print ('file close()')
			break
		# write data to a file
		f.write(data)
	f.close()

# ip = get('https://api.ipify.org').text
def main():

	tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpsock.bind((TCP_IP, TCP_PORT))
	threads = []

	while True:
		tcpsock.listen(15)
		print ("Waiting for incoming connections...")
		(conn, (ip,port)) = tcpsock.accept()
		print ('Got connection from ', (ip,port))
		print("Enter the Message(START), or Enter space if No message to be send")
		message_type=raw_input()
		# print(message_type)
		if message_type=="START":#None means I don't want to send any message
			send_message(conn,message_type)
			c=10
			while c>0:
				val=rec_message(conn)
				# print(val)
				if val=="YES":
					send_message(conn,ip)
					send_file(conn,"Problem.txt")
					break
				elif val!="YES":
					print("User Does not want to participate")
					# tcpsock.close()
					break
				time.sleep(1)
				c=c-1
		else:
			print("No Message Entered")
		# tcpsock.close()
	    #Writing the details of a connected machine into a node_ip file
	    # f=open('node_ip','a')#Append to the existing file
	    # f.write(ip)
	    # f.write(" ")
	    # f.write(str(port))
	    # f.write("\n")
	    # f.close()

	# 	newthread = ClientThread(ip,port,conn)
	# 	newthread.start()
	# 	threads.append(newthread)

	# for t in threads:
	# 	t.join()

if __name__ == '__main__':
	myIP()
	main()
