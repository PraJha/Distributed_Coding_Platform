
# client2.py
#!/usr/bin/env python
import os, sys, socket, time, csv, subprocess
from threading import Thread
from SocketServer import ThreadingMixIn

TCP_PORT = 9001
BUFFER_SIZE = 1024

def rec_file(s,filename):
    # print("In rec_file")
    f=open(filename,"w+")
    # print ('file opened')
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        # print('data=%s', (data))
        f.write(data)
        break
        # if not data:
        #     f.close()
        #     print ('file close()')
        #     break
        # write data to a file
        
    f.close()
    print("File Successfully Received")
    
def send_file(s,filename):
    print("In send_file")
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
    f.close()
    print("File Successfully Sent")
            
def send_message(s,val):
    s.sendall(val)

def rec_message(s):
    data = s.recv(1024)
    print(data)
    return data

i=0#index of all_node array
f=open('node_ip','r')
all_node=f.readlines()
f.close() 

curr_node=all_node[0].rsplit(' ',1)
curr_node_ip=curr_node[0]#To which IP We will send the message.
TCP_IP = curr_node_ip #If using on different machine use curr_node_ip. This ip is specific to a machine
print(TCP_IP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.settimeout(300)#Will try to get the connection till 5 min.
try:
    s.connect((TCP_IP,TCP_PORT))
    print("Enter the name of file to receive/send or a command to execute some script.")
    file=raw_input()#Take file name as input and send
    if file=="RUN":
        print('connection closed')
    elif file=="SCORE":
        file_name='score_'+TCP_IP+'.txt'
        rec_file(s,file_name)
    else:
        send_file(s,file)
        print('connection closed')
    
except:
    # print "Server not available to connect"
    time.sleep(0.5)

#COMMENT