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
            print('Sent ',repr(l))
            l = f.read(BUFFER_SIZE)
        if not l:
            f.close()
            # s.close()
            break
    print("File Successfully Sent")
    
def rec_file(s,filename,type=0):#Type means binary or not

	print("In rec_file server.py")
	if type==1:
		f=open(filename,"wb")
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
		print("File Successfully Received")
	else:
		f=open(filename,"wb")
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
		print("File Successfully Received")
# ip = get('https://api.ipify.org').text
def main():

	class ClientThread(Thread):

	    def __init__(self,ip,port,sock):
	        Thread.__init__(self)
	        self.ip = ip
	        self.port = port
	        self.sock = sock
	        print (" New thread started for "+ip+":"+str(port))

	    def run(self):
	        filename='client.py'
	        f = open(filename,'rb')
	        while True:
	            l = f.read(BUFFER_SIZE)
	            while (l):
	                self.sock.send(l)
	                #print('Sent ',repr(l))
	                l = f.read(BUFFER_SIZE)
	            if not l:
	                f.close()
	                self.sock.close()
	                break

	tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpsock.bind((TCP_IP, TCP_PORT))
	threads = []

	while True:
		tcpsock.listen(15)
		print ("Waiting for incoming connections...")
		(conn, (ip,port)) = tcpsock.accept()
		print ('Got connection from ', (ip,port))
		print("Enter the name of file to receive/send or a command to execute some script.")
		file=raw_input()#Take file name as input and send
		if file[:-3]=="zip":
			rec_file(conn,file,1)#'test_.zip'
		elif file=="RUN":
			print("RUNNING TEST Cases...")
			subprocess.call("bash evaluate.sh",shell=True)
		elif file=="SCORE":
			send_file(conn,'score.txt')
		else:
			rec_file(conn,file)

if __name__ == '__main__':
	myIP()
	main()
