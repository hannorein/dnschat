import random
import os
import string
import socket
import urllib
with open("secret.txt","r") as f:
    secret = f.read().strip()
with open("host.txt","r") as f:
    host = f.read().strip()

def encode(s):
    es = ""
    for c in s:
        es += "%d-"%ord(c)
    return es[:-1]

with open("testmail.txt","r") as f:
    msg = f.read()

i = 0
chunk = 10
while i<len(msg):
    pmsg = (msg[i:])[:chunk]
    salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    if i==0:
        msgtype = "new"
    else:
        msgtype = "con"
    hn = encode(pmsg)+"."+msgtype+"."+salt+"."+secret+"."+host
    print(hn)
    print(socket.gethostbyname(hn))
    i += chunk

salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
hn = "0.sen."+salt+"."+secret+"."+host
print(hn)
print(socket.gethostbyname(hn))
print("Sent.")
