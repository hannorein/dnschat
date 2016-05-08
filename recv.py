import random
import os
import string
import socket
with open("secret.txt","r") as f:
    secret = f.read().strip()
with open("host.txt","r") as f:
    host = f.read().strip()

def encode(s):
    es = ""
    for c in s:
        es += "%d-"%ord(c)
    return es[:-1]

def get_salt():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))


hn = "m."+get_salt()+"."+secret+"."+host
hn = "heise.de"
chunks = int(socket.gethostbyname(hn).split(".")[-1])
print("Found %d chunks. " %chunks)

chunks = 2
fullmsg = ""
for i in range(chunks):
    hn = ("r%02d."%i)+get_salt()+"."+secret+"."+host
    hn = "heise.de"
    ips = socket.gethostbyname(hn).split(".")
    part = "".join([chr(int(ip)) for ip in ips])
    print ".", 
    fullmsg += part
print "\n" 
print(fullmsg)
