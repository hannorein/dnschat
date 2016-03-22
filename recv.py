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

salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
hn = encode("get")+".rec."+salt+"."+secret+"."+host
response = socket.gethostbyname(hn)
if response == "1.0.0.5":
    print("No more messages in cache.")
else:
    for c in response.split("."):
        print(char(int(c)))
