import os
import requests

from dotenv import load_dotenv

# API Base URL
API_BASE_URL = os.getenv("API_BASE_URL")
API_WILAYAH = os.getenv("API_WILAYAH")

load_dotenv()

# Helper function to make API calls
def api_call(method, endpoint, data=None, headers=None):
    url = f"{API_BASE_URL}{endpoint}"
    default_headers = {'Content-Type': 'application/json'}
    if headers:
        default_headers.update(headers)
    
    # print(f"Making {method} request to: {url}")
    # print(f"Headers: {default_headers}")
    # if data:
    #     print(f"Data: {data}")
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=default_headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=default_headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=default_headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=default_headers)
        
        # print(f"Response status: {response.status_code}")
        # print(f"Response headers: {dict(response.headers)}")
        # print(f"Response content: {response.text}")
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

def api_wilayah_call(method, endpoint, data=None, headers=None):
    url = f"{API_WILAYAH}{endpoint}"
    default_headers = {'Content-Type': 'application/json'}
    if headers:
        default_headers.update(headers)
    
    # print(f"Making {method} request to: {url}")
    # print(f"Headers: {default_headers}")
    # if data:
    #     print(f"Data: {data}")
    
    try:
        response = requests.get(url, headers=default_headers, verify=False)
        # print(f"Response status: {response.status_code}")
        # print(f"Response headers: {dict(response.headers)}")
        # print(f"Response content: {response.text}")
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None 