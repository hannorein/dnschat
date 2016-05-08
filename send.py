import random
import os
import string
import math
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


# Default message
msg = """From: hanno@hanno-rein.de
To: hanno@hanno-rein.de
Subject: Message from Hanno Rein (via dnschat)

Hello Hanno. This is a test!
"""

# Read message from file.
if os.path.isfile("msg.txt"):
    with open("msg.txt","r") as f:
        msg = f.read()

i = 0
part = 0
chunk = 10
while i<len(msg):
    pmsg = (msg[i:])[:chunk]
    msgtype = "c%02d"%part
    print "Sending chunk %02d of %02d... " %(part+1, math.ceil(float(len(msg))/chunk)), 
    hn = encode(pmsg)+"."+msgtype+"."+get_salt()+"."+secret+"."+host
    ip = int(socket.gethostbyname(hn).split(".")[-1])
    print "Server has now %0d chunks." % ip

    part +=1
    i += chunk

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
