import random
import string
import math
import socket
with open("secret.txt","r") as f:
    secret = f.read().strip()
with open("host.txt","r") as f:
    host = f.read().strip()

def encode(s):
    return "-".join(["%d"%ord(c) for c in s])

def get_salt():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))


# Read message from file.
with open("msg.txt","r") as f:
    msg = f.read()

part = 0
chunksize = 10
while part*chunksize<len(msg):
    pmsg = (msg[part*chunksize:])[:chunksize]
    msgtype = "c%02d"%part
    print "Sending chunk %02d of %02d..." %(part+1, math.ceil(float(len(msg))/chunksize)), 
    hn = encode(pmsg)+"."+msgtype+"."+get_salt()+"."+secret+"."+host
    ip = int(socket.gethostbyname(hn).split(".")[-1])
    print "server has now %0d chunks." % ip

    part +=1

print "\nChecking if server has all %d chunks..." % part, 
hn = "msg.p."+get_salt()+"."+secret+"."+host
rec = int(socket.gethostbyname(hn).split(".")[-1])
if rec==part:
    print("yes. Will send message now.")
    hn = ("c%02d.sen."%part)+get_salt()+"."+secret+"."+host
    print(socket.gethostbyname(hn))
    print("Sent.")
else:
    print("no. Something went wrong. Message not sent. Try again.")
