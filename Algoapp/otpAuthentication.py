import requests
import os

from dotenv import load_dotenv

load_dotenv()


def send_otp(recipient_email, recipient_name, otp):
    url = "https://control.msg91.com/api/v5/email/send"

    # Replace with your actual MSG91 authkey
    msg91_authkey = os.getenv('msg91_authkey')

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "authkey": msg91_authkey
    }

    # Replace with your actual registered domain with MSG91
    registered_domain = "algo1.co.in"

    # Replace with the actual recipient's email and name
    recipient_email = recipient_email
    recipient_name = recipient_name

    # Replace with your actual template ID
    template_id = "global_otp"

    # Replace with your actual OTP value
    otp_value = otp

    body = {
        "recipients": [
            {
                "to": [
                    {
                        "email": recipient_email,
                        "name": recipient_name
                    }
                ],
                "variables": {"otp": otp_value, "company_name": "Algo1"}
            }
        ],
        "from": {
            "email": "no-reply@" + "algo1.co.in"
        },
        "domain": registered_domain,
        "template_id": template_id
    }

    response = requests.post(url, json=body, headers=headers)

    print(response.json())