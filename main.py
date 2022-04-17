from asyncio.windows_events import NULL
from distutils.dep_util import newer_group
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

bearer_token = os.getenv('BEARER')


def user_url():
    user = input("Enter Username :")
    usernames = "usernames={}".format(user)
    user_fields = "user.fields=description,created_at"
    url = "https://api.twitter.com/2/users/by?{}".format(usernames, user_fields)
    return url

def followers_url(id):
    user_id = id
    return "https://api.twitter.com/2/users/{}/followers".format(user_id)


def user_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def followers_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r

def followers_params():
    return {"user.fields": "created_at"}

def connect_user_endpoint(url):
    response = requests.request("GET", url, auth=user_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def connect_follow_endpoint(url, params):
    response = requests.request("GET", url, auth=user_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def all_followers():
    users_url = user_url()
    user = connect_user_endpoint(users_url)
    id = user['data'][0]['id']
    follow_url = followers_url(id)
    params = followers_params()
    followers = connect_follow_endpoint(follow_url, params)
    all_followers = followers['data']
    token = followers['meta']['next_token']
    while(token):
        new_params = followers_params()
        new_params['pagination_token'] = token
        new_followers = connect_follow_endpoint(follow_url, new_params)
        all_followers += new_followers['data']
        if('next_token' not in new_followers['meta']):
            token = None
        else:
            token = new_followers['meta']['next_token']
    return all_followers


def main():
    followers = all_followers()

if __name__ == "__main__":
    main()