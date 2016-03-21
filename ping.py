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

salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
msgtype = "new"
hn = encode("test")+"."+msgtype+"."+salt+"."+secret+"."+host
print("If you see 1.0.0.1 as a response, the server is up and running.")
print("Query:    %s"%hn)
print("Response: %s"% socket.gethostbyname(hn))
