# client2.py
#!/usr/bin/env python
import os, sys, socket, time, csv, subprocess
from threading import Thread
from SocketServer import ThreadingMixIn

TCP_PORT = 9001
BUFFER_SIZE = 1024

def rec_file(s,filename):
    # print("In rec_file")
    f=open(filename,"w")
    # print ('file opened')
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        print('data=%s', (data))
        if not data:
            f.close()
            # print ('file close()')
            break
        # write data to a file
        f.write(data)
    f.close()
    print("File Received Successfully\n")

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

def send_message(s,val):
    s.sendall(val)

def rec_message(s):
    data=""
    while True:
        data = s.recv(1024)
        if data!="":
            return data
    return data

i=0#index of all_node array
f=open('node_ip','r')
all_node=f.readlines()
f.close() 

while True:
    if all_node[i]=='\n':
        break
    curr_node=all_node[i].rsplit(' ',1)
    curr_node_ip=curr_node[0]#To which IP We will send the message.
    TCP_IP = curr_node_ip
    print(TCP_IP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.settimeout(300)#Will try to get the connection till 5 min.
    try:
        s.connect((TCP_IP,TCP_PORT))
        data=rec_message(s)
        # print(data)
        if data=='START':
            print("For Join enter YES, Else NO")
            wantToJoin=raw_input()
            if wantToJoin=="YES":
                Organizer_ip = curr_node_ip
                fi = open("Organizer_ip.txt", "wb")
                fi.write(Organizer_ip)
                fi.close()
                send_message(s,"YES")
                file_name=rec_message(s)
                file_name='Problem.txt'
                print("You have agreed to participate in the contest. So you will now receive a problem statement file.")
                rec_file(s,file_name)
                # print("Do You Want to submit")
            else:
                send_message(s,"NO")
        elif data=='SUBMIT':
            filename="test_.zip"
            rec_file(s,filename)
            break
        # print('Successfully get the file')
        s.close()
        print('connection closed.')
        # cmd='pkill -f client.py'
        # print("Hi")
        # sys.exit(0)
        # return_code = subprocess.call("pkill -f client.py", shell=True)
        # print("EXECUTED")
    except:
        if i>len(all_node):
            i = 0
        else:
            i = (i+1)%len(all_node)
        # print "Server not available to connect"
        time.sleep(0.5)
        continue

#COMMENT

# for i in range(len(all_node)):
#     send_message(s,"Hi");
