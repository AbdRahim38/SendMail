#!/usr/bin/env python3
'''
 Desc: Sending Email Challenge
 Date: 26Jan2022
 By: A_Rahim / Github: AbdRahim38
 Version: 1.0
 Send email using HTML format with file attachment
 system will prompt for password authetication with masking ability
 system will prompt for sender email, receiver email, subject, content in html, attachment file path
 try and except has been used to capture any error message
 
- to be change: <GMAIL USERNAME>
- to be install: pip3 install stdiomask
'''

import smtplib
import getpass
import stdiomask

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def init():
    #system initialize
    global _HOSTNAME
    global _PORTSSL
    global _PORTTSL
    global _USERNAME
    global _PASSWORD
    global _CONNECTION_TYPE
    _HOSTNAME = 'smtp.gmail.com'
    _PORTSSL = 465
    _PORTTSL = 587
    _USERNAME = <GMAIL USERNAME>
    _CONNECTION_TYPE = 1; #SSL 1, TSL 2
    #sender_pass = getpass.getpass(prompt="Enter Password: ") #prompt password as invisible entry
    _PASSWORD = stdiomask.getpass(prompt="Enter Password: ", mask='*') #prompt password as asterik entry

def sendMail(MyMail):
    #Create SMTP session for sending the mail    
    try:
        if _CONNECTION_TYPE==1:
            print(f">>> Connecting to SMTP Server via SSL")
            session = smtplib.SMTP_SSL(_HOSTNAME, _PORTSSL) #use gmail SSL
        elif _CONNECTION_TYPE==2:
            print(f">>> Connecting to SMTP Server via TSL")
            session = smtplib.SMTP_SSL(_HOSTNAME, _PORTTSL) #use gmail TSL
            session.starttls() #enable security

        print('>>> Sending Email...')
        session.login(_USERNAME, _PASSWORD) #login with mail_id and password
        final_content = MyMail[0].as_string()
        session.sendmail(MyMail[1], MyMail[2], final_content)

    except smtplib.SMTPException as err:
        print(f">>> Error: Unable to send email! \n {err}")
    else:  
        print('>>> eMail Sent!')
    finally:
        session.quit()

def newMail():
    message = MIMEMultipart('mixed')

    #Promp user for eMail Info
    sender_name = input("Sender Name: ")
    sender_address = input("From (email@domain.com): ") #_USERNAME
    receiver_address = input("To (email@domain.com): ")
    mail_subject = input("Subject: ")
    mail_content = input("Content: ")
    mail_attachment = input("Attach File (/path/filename): ")

    try:
        with open(mail_attachment, "rb") as attachment:
            p = MIMEApplication(attachment.read(),_subtype="pdf")	
            p.add_header('Content-Disposition', "attachment; filename= %s" % mail_attachment.split("\\")[-1]) 
            message.attach(p)
    except Exception as err:
        print(f">>> Error: File Attached Error! \n {err}")
    else:  
        print('>>> File Attached Successful!')

    #Setup the MIME
    message['From'] = f"{sender_name} <{sender_address}>"
    message['To'] = receiver_address
    message['Subject'] = mail_subject

    #message.attach(MIMEText(mail_content, 'plain'))
    message.attach(MIMEText(mail_content, 'html')) #attach message body

    final = (message, sender_address, receiver_address)
    return final

def main():
    init()
    MynewMail = newMail()
    sendMail(MynewMail)

if __name__ == "__main__":
    main()