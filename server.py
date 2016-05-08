from twisted.internet import reactor, defer
from twisted.names import client, dns,  server
import time
import math
import smtplib
import glob
import os
with open("secret.txt","r") as f:
    secret = f.read().strip()
with open("googlesecret.txt","r") as f:
    googlesecret = f.read().strip()

fromaddr = 'hanno@hanno-rein.de'

def decode(s):
	ds = ""
	for c in s.split("-"):
		ds += chr(int(c))
	return ds

class DynamicResolver(object):
    def _doDynamicResponse(self, query):
        name = query.name.name
	names = name.split(".")
	if len(names)<4:
		answer = dns.RRHeader( name=name, payload=dns.Record_A(address="82.165.8.17"))
		return [answer], [], []
	msg, msgtype, salt, secretr = names[0:4]
	if secret == secretr:
		t = b"1.0.0.0"
		if msgtype[0]=="c":
			msg = decode(msg)
			i = int(msgtype[1:3])
			with open("parts/msg%02d.txt"%i,"w") as f:
				f.write(msg)
			print("Receiving message part %02d."%i)
			rsofar = len(glob.glob("parts/msg*.txt"))
			t = "1.0.0.%d" % rsofar
		elif msgtype[0]=="p":
			rsofar = len(glob.glob("parts/msg*.txt"))
			t = "1.0.0.%d" % rsofar
		elif msgtype=="sen":
			i = int(msg[1:3])
			t = b"1.0.0.201"
			rsofar = len(glob.glob("parts/msg*.txt"))
			if i == rsofar:
				sserver = smtplib.SMTP('smtp.gmail.com:587')
				sserver.ehlo()
				sserver.starttls()
				sserver.login(fromaddr,googlesecret)
				fullmsg = ""
				for fn in sorted(glob.glob("parts/msg*.txt")):
					with open(fn,"r") as f:
					    msg = f.read()
					fullmsg += msg
					os.remove(fn)
				for l in fullmsg.split("\n"):
					if l[0:3] == "To:":
						toaddr = l[4:].strip()
				sserver.sendmail(fromaddr, toaddr, fullmsg)
				print("Sending message.")
				t = b"1.0.0.200"
				sserver.quit()
		elif msgtype[0]=="m":
			with open("msg.txt","r") as f:
				msg = f.read()
			chunk = 4
			l = math.ceil(float(len(msg))/4)
			t = "1.0.0.%d"%l
			
		elif msgtype[0]=="r":
			t = b"1.0.0.202"
			with open("msg.txt","r") as f:
				msg = f.read()
			chunk = 4
			j = int(msgtype[1:3])
			i= 0
			part = 0
			while i<len(msg):
				pmsg = (msg[i:])[:chunk]
				while len(pmsg)<4:
					pmsg += " "
				i+= chunk
				ip = ".".join(["%d"%(min(255,ord(c))) for c in pmsg])
				if part==j:
					t = ip
				part += 1


		answer = dns.RRHeader( name=name, payload=dns.Record_A(address=t))
		return [answer], [], []
	return dns.RRHeader( name=name, payload=dns.Record_A(address=b'1.2.3.4')), [], []

    def query(self, query, timeout=None):
        return defer.succeed(self._doDynamicResponse(query))



def main():
    factory = server.DNSServerFactory(
        clients=[DynamicResolver()]
    )
    protocol = dns.DNSDatagramProtocol(controller=factory)
    reactor.listenUDP(53, protocol)
    reactor.run()



if __name__ == '__main__':
    raise SystemExit(main())
