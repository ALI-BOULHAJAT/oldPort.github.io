from email.mime.application import MIMEApplication
from posixpath import basename
from flask import Flask, render_template, url_for, request, redirect
import email
from importlib.resources import path
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from tokenize import Name
from datetime import datetime



app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:path>')
def page(path):
    return render_template(path)

########## write in the file #####

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        now = datetime.now()
        my_time = now.strftime("%B %d, %Y__%H:%M:%S")
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'date : {my_time}\nEmail : {email}\nSubject : {subject}\nMessage : {message}\n\n')
    


########## email sender #####

def mail_sender():
    email = MIMEMultipart()
    email['from'] = 'stiv'
    email['to'] = 'boulhajat.ali@gmail.com'
    email['subject'] = 'subject'

    filename = 'database.txt'
    with open(filename, 'r') as f:
        attachment = MIMEApplication(f.read(), Name=basename(filename))
        attachment['Content-Disposition'] = 'attachement; filename="{}"'.format(basename(filename))

    email.attach(attachment)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('portfolio.bou@gmail.com', 'weunelnxssuuwfnl')
        smtp.send_message(email)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_file(data)
        mail_sender()
        return redirect('thank for contacting.html')
    else:
        return 'Problem'
