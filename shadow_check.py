import os, hashlib, sys, time, string 
import smtplib , sys  , getpass ,signal
from email.mime.text import MIMEText
def signal_handler(signal, frame):
    print "\n[-] Exiting"
    exit()
signal.signal(signal.SIGINT, signal_handler)
user = raw_input("Please Enter your Email : ")
passwd = getpass.getpass("Please Enter your password: ")
def login(user , passwd) :
	smtp = smtplib.SMTP("smtp.gmail.com" , 587)
	smtp.ehlo()
	smtp.starttls()
	smtp.ehlo()
	smtp.login(user, passwd)
	smtp.ehlo()
	smtp.close()
	del smtp
while 1 : 
	try  : 
		login(user , passwd)
		break
	except Exception as  e:
		if  "not accepted" in str(e[1]) : 
			passwd = getpass.getpass("[-] Please reEnter your password: ")
			pass
		else : 
			print e[1]
			exit()
def send( user , passwd ,  text ) : 		
	msg = MIMEText(text)
	msg["To"] = user 
	msg["From"] = "email@something.com"
	msg["Subject"] = "Shadow Changed" 
	try : 
		smtp = smtplib.SMTP("smtp.gmail.com" , 587) 
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		smtp.login(user, passwd)		
		smtp.sendmail(user ,user, msg.as_string())
		smtp.close() 
		print "[+] report sent " 
	except Exception as e  : 
		print "[-] "+str(e)
file1 = "/etc/shadow"
shadowfile=open(file1,"rb").read()
n = hashlib.md5()
n.update(shadowfile)
hashed1 = n.hexdigest()
shadow2 = open(file1,"r").readlines()
print "[+] md5 for the shadow file is : "+str(hashed1)
while 1 : 
	try:
            infile = open(file1, "rb")
            content = infile.read()
            infile.close()
            m = hashlib.md5()
            m.update(content)
            hashed = m.hexdigest()
            if hashed == hashed1 : 
		time.sleep(5)
		pass

	    else : 
		print "[-] the shadow file has changed  at : %s" % time.strftime("%X")
		changedshadow = open(file1 , "r").readlines()
		text = ""
		for i in changedshadow : 
			if i not in shadow2 : 
				text+= i 
				text+= "\n"
		send(user , passwd , text)
		hashed1 = hashed

	except Exception as e :
            print "[-] "+str(e)
            pass
