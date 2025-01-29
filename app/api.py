import requests
import json
import os

async def get_response(device_id):
    url = 'https://api.imeicheck.net/v1/checks'

    token = os.getenv('API_TOKEN')

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    body = json.dumps({
        "deviceId": device_id,
        "serviceId": os.getenv('SERVICE_ID')
    })

    response = requests.post(url, headers=headers, data=body)

    return response

def is_imei_valid(imei):
    if len(imei) != 15 or not imei.isdigit():
        return False

    digits = [int(d) for d in imei]
    total = 0

    for i in range(14):
        if i % 2 == 0:
            total += digits[i]
        else:
            doubled = digits[i] * 2
            total += doubled if doubled < 10 else doubled - 9

    return (total + digits[-1]) % 10 == 0
