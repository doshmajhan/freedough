"""
Logs into the dp dough API and gives our user
the maximum amount of hearts obtainable each day

@author: Cameron Clark
"""

import requests
import json

CREDENTIAL_FILE = "credentials.json"
API_URL = "https://api.dpdough.com"
AUTH_URL = "{}/oauth/token".format(API_URL)
POINTS_URL = "{}/api/game/points".format(API_URL)
MAX_POINTS = 37500
CUSTOMER_ID = 131727
HEADERS = {
    'User-Agent': "calzonerun/26 CFNetwork/974.2.1 Darwin/18.0.0", 
    'X-Unity-Version': "2018.1.7f1"
}

"""
Loads the credentials from the credentials.json file

Returns:
    A dictionary with the user and password key
"""
def load_creds():
    with open(CREDENTIAL_FILE) as cred_file:
        creds = json.load(cred_file)

    return creds


"""
Creates a requestions session that is authenticated with the
given credentials

Params:
    credentials: a dictionary containing entries for user and password

Returns:
    A requests session with the correct authentication
"""
def create_session(credentials):
    session = requests.Session()
    session.headers.update(HEADERS)

    data = dict()
    data['username'] = credentials['user']
    data['password'] = credentials['password']
    data['client_id'] = 2
    data['grant_type'] = "password"
    data['client_secret'] = "5IFUoqLi0GaiYKxnPB3T1WTSl91AmWziS2KFKoHf"

    response = session.post(AUTH_URL, json=data)

    print response
    print response.status_code
    print response.json()

    token_data = response.json()
    session.headers.update({
        "Authorization": "{} {}".format(token_data['token_type'], token_data['access_token'])
    })

    return session


"""
Makes a PUT request to the API adding points to our account

Params:
    session: the authenticated requests session

"""
def add_points(session):
    data = dict()
    data['customer_id'] = CUSTOMER_ID
    data['game_points'] = MAX_POINTS

    response = session.put(POINTS_URL, json=data)

    print response
    print response.status_code
    print response.json()



if __name__ == '__main__':
    credentials = load_creds()
    print "LOGGING IN"
    session = create_session(credentials)
    print "ADDING POINTS"
    add_points(session)
    
    
