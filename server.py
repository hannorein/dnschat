from twisted.internet import reactor, defer
from twisted.names import client, dns,  server
import time
import smtplib
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
		return dns.RRHeader( name=name, payload=dns.Record_A(address=b'1.2.3.4')), [], []
	msg, msgtype, salt, secretr = names[0:4]
	if secret == secretr:
		msg = decode(msg)
		t = b"1.0.0.0"
		if msgtype=="new" or msgtype=="con":
			if msgtype=="new":
				fo = "w"
				t = b"1.0.0.1"
			else:
				fo = "a"
				t = b"1.0.0.2"
			with open("msg.txt",fo) as f:
				f.write(msg)
			print("Receiving message part.")
		elif msgtype=="sen":
			t = b"1.0.0.3"
			if os.path.isfile("msg.txt"): #only send mail once
				sserver = smtplib.SMTP('smtp.gmail.com:587')
				sserver.ehlo()
				sserver.starttls()
				sserver.login(fromaddr,googlesecret)
				with open("msg.txt","r") as f:
				    msg = f.read().strip()
				for l in msg.split("\n"):
					if l[0:3] == "To:":
						toaddr = l[4:].strip()
				sserver.sendmail(fromaddr, toaddr, msg)
				print("Sending message.")
				t = b"1.0.0.4"
				os.remove("msg.txt")
				sserver.quit()
		elif msgtype=="rec":
			if os.path.isfile("msg_out.txt"):  #new messages arrived?
                with open("msg_out.txt","r") as f:
                    msg = f.read().strip()
                pmsg = msg[:4]
                while len(pmsg)<4:
                    pmsg += " "
                if len(msg)>4:
                    with open("msg_out.txt","w") as f:
                        f.write(msg[4:])
                else:
                    os.remove("msg.txt")
                t = ""
                for c in pmsg:
                    t += "%d."%ord(c)
			else:
                t = b"1.0.0.5"



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
