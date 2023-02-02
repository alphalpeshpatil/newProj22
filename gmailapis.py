from email import encoders, parser
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import io
import mimetypes
import psycopg2
import pathlib
from flask import jsonify
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import base64
import pickle
from googleapiclient.errors import HttpError
import os
import json
import base64
from flask import Flask, jsonify, request
from email.message import EmailMessage

from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

from login import API_NAME, API_VERSION, CLIENT_SECRET_FILE

from apiclient import discovery
from apiclient import errors
from httplib2 import Http
import base64
from bs4 import BeautifulSoup
import re
import time
# import dateutil.parser as parser
import datetime
from datetime import datetime


# app.config['SECRET_KEY']='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'
# app.config['SESSION_PERMANENT']=False
# app.config['SESSION_TYPE']="filesystem"
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
global_creds=[]
home_dir=os.path.expanduser('~')
pickle_path=os.path.join(home_dir,'gmail.pickle')
global_creds_set=""
global_creds.clear()
global_creds.append(global_creds_set)

def gmail_auth():
    try:
        home_dir=os.path.expanduser('~')
        flow=InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
        print(flow)
        creds=flow.run_local_server(port=5001)
        pickle_path=os.path.join(home_dir,'gmail.pickle')

        with open(pickle_path,'wb') as token:
            pickle.dimp(creds,token)
        global_creds_set=pickle.load(open(pickle_path),'rb')
        global_creds.clear()
        global_creds.append(global_creds_set)
        return 'Authentication Done successfuly'
    except Exception as ex:
        print(ex)
        return str(ex)

def send_message(mailid,cc,bcc,subject,body,file):
    msg=send_message_with_Attachment(mailid,cc,bcc,subject,body,file)
    try:
        client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "credentials.json")
        flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]
        # redirect_uri="http://127.0.0.1:5000/callback"
)
        authorization_url, state = flow.authorization_url()
        service =Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        # message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        draft = service.users().messages().send(userId="me",body=msg).execute()
        print(draft)
        print("Message sent successfuly!!!!")
    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None
    return draft
# def convertToBinaryData(filename):
#     # Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         binaryData = file.read()
#     return binaryData
def send_message_with_Attachment(mailid,cc,bcc,subject,body,file):

        message = MIMEMultipart()
        message['to'] = mailid
        message['cc']=cc
        message['bcc']=bcc
        message['subject'] = subject

        msg = MIMEText(body)
        message.attach(msg)
        # buffer = io.BytesIO()     # create file in memory
        # file.save(buffer, 'jpeg') # save in file in memory - it has to be `jpeg`, not `jpg`
        # buffer.seek(0)            # move to the beginning of file

        # file = buffer 
        # file='butterfly.jpg'
        # print((file)
        # print(type(file))
        # file = convertToBinaryData(file)
        file = str(file.filename)
        (content_type, encoding) = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        (main_type, sub_type) = content_type.split('/', 1)
        # print(file)
        if main_type == 'text':
            with open(file, 'rb') as f:
                msg = MIMEText(f.read().decode('utf-8'), _subtype=sub_type)
        elif main_type == 'image':
                f=open(file,'rb')
                msg=MIMEImage(f.read(),_subtype=sub_type)
                f.close()
        elif main_type == 'audio':
            with open(file, 'rb') as f:
                msg = MIMEAudio(f.read(), _subtype=sub_type)
            
        else:
            with open(file, 'rb') as f:
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(f.read())

        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment',
                    filename=filename)
        message.attach(msg)

        raw_message = \
            base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
        return {'raw': raw_message.decode('utf-8')}
    



SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.modify']


def connections(connection,cursor,lable_id_one,lable_id_two):
    client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "credentials.json")
    flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"])
        # redirect_uri="http://127.0.0.1:5000/callback"


    authorization_url, state = flow.authorization_url()
    service =Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    unread_msgs = service.users().messages().list(userId='me',labelIds=[lable_id_one],q=lable_id_two).execute()

    # We get a dictonary. Now reading values for the key 'messages'
    mssg_list = unread_msgs['messages']

    print ("Total unread messages in inbox: ", str(len(mssg_list)))
    i=1
    for mssg in mssg_list:
        m_id = mssg['id'] # get id of individual message
        sql = """ INSERT INTO email1 (sno,message_id,lable) VALUES (%s,%s,%s)"""
        sql_where=(i,m_id,lable_id_two)
        i=i+1
        cursor.execute(sql,sql_where)
        connection.commit()
    return "connection done"

def getEmails(lable_id,cursor,n,m,subject,date,sender,body):
    client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "credentials.json")
    flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"])
        # redirect_uri="http://127.0.0.1:5000/callback"

    authorization_url, state = flow.authorization_url()
    service =Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    final_list = [ ]

    def function(para):
        if para=="Subject" or para=="Date" or para=="Sender" or para=="Body":
            return True
        else:
            return False

    for i in range(n,m):
        temp_dict = { }
        sql = "SELECT * FROM email1 WHERE sno=%s and lable=%s"
        sql_where=(i,lable_id)
        cursor.execute(sql,sql_where)
        row=cursor.fetchone()
        msg_id=row[1]
        lable_id=row[2]
        message = service.users().messages().get(userId='me',id=msg_id).execute() # fetch the message using API
        payld = message['payload'] # get payload of the message 
        headr = payld['headers'] # get header of the payload

        if function(subject):
            for one in headr: # getting the Subject
                # print('subject diya he!!!!')
                if one['name'] == 'Subject':
                    msg_subject = one['value']
                    temp_dict['Subject'] = msg_subject
                else:
                    pass
        else:
            pass
        if function(date):
            for two in headr: # getting the date
                if two['name'] == 'Date':
                    msg_date = two['value']
                    # date_parse = (msg_date)
                    # m_date = (date_parse.date())
                    temp_dict['Date'] = str(msg_date)
                else:
                    pass
        else:
            pass

        if function(sender):
            for three in headr: # getting the Sender   
                if three['name'] == 'From':
                    msg_from = three['value']
                    temp_dict['Sender'] = msg_from
                else:
                    pass
        else:
            pass
        temp_dict['Snippet'] = message['snippet'] # fetching message snippet
        if function(body):
            try:
                # Fetching message body
                mssg_parts = payld['parts'] # fetching the message parts
                part_one  = mssg_parts[0] # fetching first element of the part 
                part_body = part_one['body'] # fetching body of the message
                part_data = part_body['data'] # fetching data from the body
                clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
                soup = BeautifulSoup(clean_two , "lxml" )
                mssg_body = soup.body()
                # mssg_body is a readible form of message body
                # depending on the end user's requirements, it can be further cleaned 
                # using regex, beautiful soup, or any other method
                temp_dict['Message_body'] = mssg_body
            except :
                pass
        else:
            pass

        print (temp_dict)
        final_list.append(temp_dict) # This will create a dictonary item in the final list
        
        # This will mark the messagea as read
        service.users().messages().modify(userId='me', id=msg_id,body={ 'removeLabelIds': ['UNREAD']}).execute() 
    print ("Total messaged retrived: ", str(len(final_list)))
    return temp_dict

