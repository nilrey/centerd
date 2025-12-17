from smtplib import SMTP
import datetime
import sys
from email.mime.text import MIMEText
from email.header    import Header
import json


debuglevel = 0
# login = str(sys.argv[1]) # login
# pwd = str(sys.argv[2]) # passw
# from_addr = str(sys.argv[3]) # from
# to_addr = str(sys.argv[4]) # to
# subj = json.loads(sys.argv[5]) # subj
# message_text = json.loads(sys.argv[6]) # message_text

smtp = SMTP()
smtp.set_debuglevel(debuglevel)
smtp.connect('192.168.56.101', 25)
smtp.login("test", "12345678")  # login
# smtp.login(sys.argv[1], sys.argv[2])  # login

from_addr = "test <test@ncuo-portal.local>"
to_addr = "test@ncuo-portal.local"


date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )

subj = "Test message 8"

message_text = "Hello\nThis is a mail from your server\n\nBye\n"

msg = MIMEText(message_text, 'plain', 'utf-8')
msg['Subject'] = Header(subj, 'utf-8')
msg['From'] = str(from_addr)
msg['To'] = str(to_addr)
smtp.sendmail(msg['From'], msg['To'], msg.as_string())

# msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( from_addr, to_addr, subj, date, message_text )
# smtp.sendmail(from_addr, to_addr, msg)

smtp.quit()



print('ok')
# print(login)
# print(pwd)
# print(from_addr)
# print(to_addr)
# print(subj)
# print(message_text)