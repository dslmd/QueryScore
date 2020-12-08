## Function: Accept emails from classmates, check the name, student ID, email address, and return the result if the check is successful.
## How to use:
#1. If you use this function, please open the pop and stmp protocol of your mailbox first. Then modify the email address and password in the code. Note that you should modify the pop and smtp server address which depends on the email you use.
#2. Put the tanscript and this program in the same folder and name it 'scores.txt'. Note that the score on the transcript should contain four parts in turn: name, student ID, score, and email address.

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
from email.mime.text import MIMEText
import smtplib

# Enter email address and password
email = "xxx"
password = "xxx"

# Enter the POP3 and SMTP server addresses:
pop3_server_addr = "pop.qq.com"
smtp_server_addr = 'smtp.qq.com'

# Open and get the score on the transcript, it should contain four parts in sequence: name, student ID, score
f = open('scores.txt')
s = f.read()

# Store the scores of the transcript into four sequences
name = s.split()[0::3]
number = s.split()[1::3]
grade = s.split()[2::3]

# Calculate the total number of students
student_number = len(grade)

#Decoding function
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

# Define the function to query the first email address and title, the return value is address + title
def addr_subj(msg, indent=0):
    subj = 0
    fromaddr = 0
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                    subj = value
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    if header == "From":
                        fromaddr = addr
    return fromaddr,subj



# Connect to SMTP server, note that the port number is 465
smtp_server = smtplib.SMTP_SSL(smtp_server_addr)
smtp_server.connect(smtp_server_addr, '465')
smtp_server.login(email, password)      #login

while (1):
    # Connect to POP3 server
    pop3_server = poplib.POP3_SSL(pop3_server_addr)
    # Authentication
    pop3_server.user(email)
    pop3_server.pass_(password)
    if (pop3_server.list()[1]!=[]):
        resp, mails, octets = pop3_server.list()
        index = len(mails)
        resp, lines, octets = pop3_server.retr(index)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        
        # Parse out the mail later:
        msg = Parser().parsestr(msg_content)
        addr = addr_subj(msg)[0]
        subj = addr_subj(msg)[1]
        
        # Initialize the searchname and searchnumber
        searchname = "?"
        searchnumber = "?"
        if len(subj.split())>0:
            searchname = subj.split()[0]
        if len(subj.split())>1:
            searchnumber = subj.split()[1]
        
        # Initialize the searchgrade to check if it will be changed
        searchgrade = "?"
        # Search grade, if successful, then change "searchgrade" to the real grade
        for i in range(student_number):
            if (searchname == name[i]) and (searchnumber == number[i]) and (addr[-17:-1] == '@mail.ustc.edu.c'):
                searchgrade = grade[i]
        # If search successfully, then reply
        if (searchgrade != "?"):
            send_str = "Your grade is "+searchgrade
            msg = MIMEText(send_str, 'plain', 'utf-8')
            msg['subject'] = 'Grade of the middle-term exam'
            msg['from'] = "Quantum Mechanics B"
            msg['to'] = addr
            smtp_server.sendmail(email, [addr], msg.as_string())
        # Delete mail directly from the server according to the mail index number:
        pop3_server.dele(index)
    pop3_server.quit() #quit pop3
    
# quit smtp, we don't need it
#smtp_server.quit()