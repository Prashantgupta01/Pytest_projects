import requests

def get_api_response(url):
    response = requests.get(url)
    return response.json()