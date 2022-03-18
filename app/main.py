#!/usr/bin/python
import shutil
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import markdown
import os
import sys
import re
import csv


def subjecter():
    # Reading filename till the second '-' to use as mail subject.
    file = os.listdir('../work/')
    file_name = file[0]
    s1 = re.match('[^-]*-[^-]*', file_name).group(0)
    return s1


def checkfile():
    # Checking, if there is a file with a specific beginning in the folder.
    # If there is no file, the program will exit.
    file = os.listdir('../work/')
    file_name = file[0]
    name_test1 = file_name.startswith('Lorem - ipsum dolor')
    name_test2 = file_name.startswith('Lorem ipsum dolor')
    if name_test1 or name_test2:
        # File existing.
        return True
    else:
        # No file in folder.
        sys.exit()


def filepath():
    # Path of the file to attach
    file = os.listdir('../work/')
    file_name = file[0]
    file_path = f'../work/{file_name}'
    return file_path


def filename():
    # Filename of the attachment
    file = os.listdir('../work/')
    file_name = file[0]
    return file_name


def readcontacts():
    # Importing contacts
    with open('./contacts.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader)
        adres = []
        if header is not None:
            for row in csv_reader:
                print(row)
                adres.append(row[2])
        return adres


# Checking existence of file
checkfile()

# read Body-Text from a markdown file
with open('body.md', 'r') as f:
    text = f.read()
    html_body = markdown.markdown(text)

html_body2 = f'''\
<html>
  <body>
  {html_body}
  </body>
</html>
'''

subject = subjecter()

port = 465  # For SSL
smtp_server = 'b2394.fakeserver.com'
sender_email = 'arnaldo37@yahoo.com'  # Enter your address
receiver_email = 'arnaldo37@yahoo.com'  # Enter receiver address
bcc_receiver = readcontacts()  # Bcc-Receiver
password = '6ZyqKvYq'

message = MIMEMultipart('alternative')
message['Subject'] = subject
message['From'] = sender_email
message['To'] = receiver_email
bcc = ', '.join(bcc_receiver)

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html_body, 'html')

message.attach(part1)
message.attach(part2)

attach_name = filename()
attach_path = filepath()

with open(attach_path, 'rb') as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    'Content-Disposition',
    'attachment', filename=f'{subject}.pdf')

# Add attachment to message and convert message to string
message.attach(part)
text_message = message.as_string()

non_empty_recipient_headers = [h for h in (message['To'], message['CC'], bcc) if h]

context = ssl.create_default_context()

# Sending mail
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, (non_empty_recipient_headers + bcc_receiver), text_message)

# Move file into archive.
archive_dir = '../archive/'
shutil.move(attach_path, archive_dir)
