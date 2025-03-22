from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_items(token, q, type, market, limit, offset):
    endpoint_url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={q}&type={type}&market={market}&limit={limit}&offset={offset}"

    query_url = endpoint_url + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    if len(json_result) == 0:
        print("No more artists could be found. Try changing the parameters or executing a different API call.")
        return None
    
    return json_result

token = get_token()

result = search_for_items(token, "1900-2025", "artist", "LT", 50, 0)

next_query_url = result["artists"]["next"]
query_results = result["artists"]["items"]