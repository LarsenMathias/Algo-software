import requests

import os

from dotenv import load_dotenv

load_dotenv()

def send_sub_otp(recipient_email, recipient_name):


    url = "https://control.msg91.com/api/v5/email/send"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "authkey": os.getenv('msg91_authkey')
    }

    body = {
        "recipients": [
            {
                "to": [
                    {
                        "email": recipient_email,
                        "name": recipient_name
                    }
                ]
            }
        ],
        "from": {
            "email": "no-reply@algo1.co.in"
        },
        "domain": "algo1.co.in",
        "template_id": "new_mail_2"
    }

    response = requests.post(url, json=body, headers=headers)

    print(response.json())