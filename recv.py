import random
import string
import socket
with open("secret.txt","r") as f:
    secret = f.read().strip()
with open("host.txt","r") as f:
    host = f.read().strip()

def get_salt():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

print "Checking server for length of message...", 
hn = "get.m."+get_salt()+"."+secret+"."+host
chunks = int(socket.gethostbyname(hn).split(".")[-1])
if chunks ==255:
    print("empty.")
else:
    print("found %d chunks. " %chunks)

    msg = ""
    for i in range(chunks):
        print "Retrieving chunk %02d of %02d..." % (i+1,chunks), 
        hn = ("get.r%02d."%i)+get_salt()+"."+secret+"."+host
        ips = socket.gethostbyname(hn).split(".")
        print "done." 
        msg += "".join([chr(int(ip)) for ip in ips])
    print "\nFull message reads:\n\n" 
    print(msg)
    print " " 
    with open("incoming_msg.txt","w") as f:
        f.write(msg)
    print "Deleting message...",
    hn = "get.emp."+get_salt()+"."+secret+"."+host
    chunks = int(socket.gethostbyname(hn).split(".")[-1])
    print("done")
