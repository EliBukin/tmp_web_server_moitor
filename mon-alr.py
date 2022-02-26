### monitoring a webserver and sending status via twilio

import requests
import os
from bs4 import BeautifulSoup
import sys

###
from twilio.rest import Client
TWILIO_ACCOUNT_SID = (sys.argv[2]) # replace with your Account SID
TWILIO_AUTH_TOKEN = (sys.argv[3]) # replace with your Auth Token
TWILIO_PHONE_SENDER = (sys.argv[4]) # replace with the phone number you registered in twilio
TWILIO_PHONE_RECIPIENT = (sys.argv[5]) # replace with your phone number

def send_text_alert(alert_str):
    """Sends an SMS text alert."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=TWILIO_PHONE_RECIPIENT,
        from_=TWILIO_PHONE_SENDER,
        body=alert_str)
###

URL_TO_MONITOR = (sys.argv[1]) #change this to the URL you want to monitor

def process_html(string):
    soup = BeautifulSoup(string, features="lxml")

    # make the html look good
    soup.prettify()

    # remove script tags
    for s in soup.select('script'):
        s.extract()

    # remove meta tags 
    for s in soup.select('meta'):
        s.extract()
    
    # convert to a string, remove '\r', and return
    return str(soup).replace('\r', '')

def webpage_was_changed(): 
    """Returns true if the webpage was changed, otherwise false."""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
    response = requests.get(URL_TO_MONITOR, headers=headers)

    # create the previous_content.txt if it doesn't exist
    if not os.path.exists("previous_content.txt"):
        open("previous_content.txt", 'w+').close()
    
    filehandle = open("previous_content.txt", 'r')
    previous_response_html = filehandle.read() 
    filehandle.close()

    processed_response_html = process_html(response.text)

    if processed_response_html == previous_response_html:
        print ("it didn't change")
        send_text_alert("its alive")
        return False
        
    else:
        filehandle = open("previous_content.txt", 'w')
        filehandle.write(processed_response_html)
        filehandle.close()
        print ("it did change")
        send_text_alert("its dead")
        return True

webpage_was_changed()
