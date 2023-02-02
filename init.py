from gmailapis import gmail_auth,send_message,getEmails
import os.path
# python -m virtualenv myvirtualenv
import os
import psycopg2
import gmailapis
import flask_mail
import pathlib
from flask import Flask,jsonify,render_template, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from Google import Create_Service
import base64
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_mail import Mail
from flask_cors import CORS,cross_origin
from flask import Flask, jsonify, request, session
app = Flask(__name__)
CORS(app,supports_credentials=True)
app.secret_key='alpeshpatil'
app.config['Mail_server']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='alpeshpatilalpesh@gmail.com'
app.config['MAIL_PASSWORD']='12345678'
app.config['MAIL_USE_TSL']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
app.config['SECRET_KEY']='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'
app.config['SESSION_PERMANENT']=False
app.config['SESSION_TYPE']="filesystem"

apiKey_global=""
# api_endpoint_entry="/api/staging"

@app.route('/gmailoauth',methods=['POST'])
def gmailoauth():
    result=gmailapis.gmail_auth()
    return jsonify(result)

@app.route('/send_message',methods=['GET',"POST"])
def send_message():
    _json=request.form
    mailid=_json['mailid']
    cc=_json['cc']
    bcc=_json['bcc']
    subject=_json['sub']
    body=_json['body']
    file=request.files['fileName']
    result=gmailapis.send_message(mailid,cc,bcc,subject,body,file)
    return result

@app.route('/get_connected',methods=['Get',"POST"])
def get_connected():
    connection = psycopg2.connect(user="postgres",password="root",host="localhost",port="5433",database="postgres")
    cursor = connection.cursor()
    _json=request.form
    lable_id_one=_json['first_lable']
    lable_id_two=_json['second_lable']
    result=gmailapis.connections(connection,cursor,lable_id_one,lable_id_two)
    return result

    
@app.route('/get_message',methods=["POST"])
def get_message():
    connection = psycopg2.connect(user="postgres",password="root",host="localhost",port="5433",database="postgres")
    cursor = connection.cursor()
    _json=request.json
    n=_json['start']
    m=_json['end']
    lable_id=_json['lable_id']
    subject=_json['subject']
    date=_json['date']
    sender=_json['sender']
    body=_json['body']
    
    result=gmailapis.getEmails(lable_id,cursor,n,m,subject,date,sender,body)
    return result

if __name__ == '__main__':
    app.run(debug=True)

# read/unread/,filter-subject,body,attachment cahiye..