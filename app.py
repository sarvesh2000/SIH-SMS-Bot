from twilio.rest import Client
from flask import Flask, request
import os

app = Flask(__name__)

os.environ["PARSE_API_ROOT"] = "https://parseapi.back4app.com/"

from parse_rest.datatypes import Function, Object, GeoPoint
from parse_rest.connection import register
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import ParseBatcher
from parse_rest.core import ResourceRequestBadRequest, ParseError


APPLICATION_ID = 'Ts1A7Zvn3GBJGN62VyvYJEUiKEJwyIBSumxwiPRk'
REST_API_KEY = 'mjbuzgxCofRDnSCUU7yovyKyKdkfSZr9KvJYqpgi'
MASTER_KEY = 'LHId46114Z1J3zwAggIwATTZ6CyWM1BpVAR4jZD3'

#Register the app with Parse Server
register(APPLICATION_ID, REST_API_KEY, master_key=MASTER_KEY)

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def sendMessage(result):
    text = 'Hey your file with file ID:'+result['result']['FileID'] +' is pending. Please start / finish the job quickly if not done already.'
    message = client.messages \
                    .create(
                        body=text,
                        from_='+15409057647',
                        to=result['result']['ContactNumber']
                    )

    print(message.sid)

    # send message to admin
    message = client.messages \
                    .create(
                        body=text,
                        from_='+15409057647',
                        to=result['result']['adminContactNumber']
                    )

    print(message.sid)

@app.route("/", methods=['POST','GET'])
def index():
    jobDeadline = Function("jobDeadline")
    result= jobDeadline(status="created")
    print(result)
    sendMessage(result)

    result= jobDeadline(status="reassigned - created")
    print(result)
    sendMessage(result)

    result= jobDeadline(status="pending")
    print(result)
    if(result['result']!="No Results Found"):
        sendMessage(result)

    result= jobDeadline(status="reassigned - pending")
    print(result)
    if(result['result']!="No Results Found"):
        sendMessage(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))