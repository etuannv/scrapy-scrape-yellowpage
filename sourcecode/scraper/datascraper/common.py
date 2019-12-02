import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import logging
import os



def notifyEmail(subject, message, toaddr):
    EMAIL_SENDER_USER = 'naitce@gmail.com'
    EMAIL_SENDER_PWD = 'chaoem12@'
    fromaddr = EMAIL_SENDER_USER
    password = EMAIL_SENDER_PWD
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'HTML'))
    try:
        logging.info('sending mail to %s on %s', toaddr, subject)
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(fromaddr, password)
        mailServer.sendmail(fromaddr, toaddr, msg.as_string())
        mailServer.close()
    except Exception as e:
        logging.info(str(e))

def readCsvToList(filePath):
    ''' Read csv file to list'''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []
    with open(filePath, 'rb', encoding="utf8") as f:
        reader = csv.reader(f)
        return list(reader)

def readCsvToListDict(filePath):
    ''' Read csv file to list of dictionary'''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []

    result = []
    with open(filePath, newline='', encoding="utf-8-sig") as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
    
    with open(filePath, newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)
    
    return result, header