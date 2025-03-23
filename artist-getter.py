from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

class Artist:
    def __init__(self, id, name, total_followers, pfp_url, external_url):
        self.id = id
        self.name = name
        self.total_followers = total_followers
        self.pfp_url = pfp_url
        self.external_url = external_url
    
    def __str__(self):
        print(f"Artist\tid: {self.id} | name: {self.name} | total_followers: {self.total_followers} | pfp_url: {self.pfp_url} | external_url: {self.external_url}")

    def __repr__(self):
        return self.__str__()

class Album:
    def __init__(self, id, name, type, total_tracks, image_url, external_url):
        self.id = id
        self.name = name
        self.type = type
        self.total_tracks = total_tracks
        self.image_url = image_url
        self.external_url = external_url
    
    def __str__(self):
        return f"Album\t\tid: {self.id} | name: {self.name} | type: {self.type} | total_tracks: {self.total_tracks} | image_url: {self.image_url} | external_url: {self.external_url}"
    
    def __repr__(self):
        return self.__str__()

class Song:
    def __init__(self, artist, id, name, duration_ms, track_number, external_url):
        self.artist = artist
        self.id = id
        self.name = name
        self.duration_ms = duration_ms
        self.track_number = track_number
        self.external_url = external_url
    
    def __str__(self):
        return f"Song\t\t\tid: {self.id} | name: {self.name} | artist: {self.artist} | duration: {self.duration_ms} | track_number: {self.track_number} | external_url: {self.external_url}"
    
    def __repr__(self):
        return self.__str__()
        

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
    if len(json_result["artists"]["items"]) == 0:
        print("No more artists could be found. Try changing the parameters or executing a different API call.")
        return None
    
    return json_result

def get_artist_albums(token, artist_id, include_groups, market, limit, offset):
    endpoint_url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    query = f"?offset={offset}&limit={limit}&market={market}&locale=en-US,en;q%3D0.5&include_groups={include_groups}"
    
    query_url = endpoint_url + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    if len(json_result["items"]) == 0:
        print("No more albums could be found. Try changing the parameters or executing a different API call.")
        return None
    
    result_list = list()

    for r in json_result["items"]:
        result_list.append(Album(r["id"], r["name"], r["album_group"], r["total_tracks"], r["images"][0]["url"], r["external_urls"]["spotify"]))
    
    return result_list

# def format_albums(albums):
#     result = list()
    

# def format(function, artists):
#     return function(artists)

def construct_artist_list(artists):
    result_list = list()
    for r in artists:
        list.append(Artist(artists["id"], artists["name"], artists["followers"]["total"], artists["images"][0]["url"], artists["external_urls"]["spotify"]))

    return result_list

token = get_token()

general_artists_return = search_for_items(token, "1900-2025", "artist", "LT", 50, 0)

next_query_url = general_artists_return["artists"]["next"]
extracted_artists = general_artists_return["artists"]["items"]

artist_discography = get_artist_albums(token, "5N0PoQbetugQlXM24VAJG4", "album,single,appears_on,compilation", "LT", 50, 0)
for r in artist_discography:
    print(r)