import requests

def send_webhook(webhook_url, message):
    data = {
        "content": message,
        "username": "BinWatch"
    }
    response = requests.post(webhook_url, json=data)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")
    else:
        print(f"Message sent successfully, status code {response.status_code}.")