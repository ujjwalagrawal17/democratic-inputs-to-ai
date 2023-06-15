import json

import requests

from pollnicely_server import settings


class SurePass:

    def __init__(self):
        pass

    def send_otp(self, aadhaar_number):
        url = f"https://kyc-api.aadhaarkyc.io/api/v1/aadhaar-v2/generate-otp"

        payload = json.dumps({"id_number": f"{aadhaar_number}"})

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.SUREPASS_TOKEN}',
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response)
        return response

    def surepass_verify_otp(self, client_id, otp):
        url = f"https://kyc-api.aadhaarkyc.io/api/v1/aadhaar-v2/submit-otp"

        payload = json.dumps({"client_id": f"{client_id}", "otp": f"{otp}"})

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.SUREPASS_TOKEN}',
        }
        response = requests.request("POST", url, data=payload, headers=headers)

        return response
