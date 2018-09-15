"""
Logs into the dp dough API and gives our user
the maximum amount of hearts obtainable each day

@author: Cameron Clark
"""
import json
import logging
import requests

LOG_FILE = "status.log"
CREDENTIAL_FILE = "credentials.json"
CREDENTIALS = dict()
API_URL = "https://api.dpdough.com"
AUTH_URL = "{}/oauth/token".format(API_URL)
POINTS_URL = "{}/api/game/points".format(API_URL)
USER_URL = "{}/api/game/users".format(API_URL)
MAX_POINTS = 37000
HEADERS = {
    'User-Agent': "calzonerun/26 CFNetwork/974.2.1 Darwin/18.0.0", 
    'X-Unity-Version': "2018.1.7f1"
}

"""
Loads the credentials from the credentials.json file
"""
def load_credentials():
    global CREDENTIALS
    with open(CREDENTIAL_FILE) as cred_file:
        CREDENTIALS = json.load(cred_file)


"""
Creates a requestions session that is authenticated with the
given credentials

Returns:
    A requests session with the correct authentication
"""
def create_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    data = dict()
    data['username'] = CREDENTIALS['user']
    data['password'] = CREDENTIALS['password']
    data['client_secret'] = CREDENTIALS['secret']
    data['client_id'] = 2
    data['grant_type'] = "password"

    response = session.post(AUTH_URL, json=data)

    if not response.ok:
        logging.debug("Error authenticating: {} {}".format(response.status_code, response.text))
        raise Exception("Error authenticating")

    token_data = response.json()
    session.headers.update({
        "Authorization": "{} {}".format(token_data['token_type'], token_data['access_token'])
    })

    logging.info("Successfully authenticated")

    return session


"""
Makes a PUT request to the API adding points to our account

Params:
    session: the authenticated requests session

"""
def add_points(session):
    data = dict()
    data['customer_id'] = get_id(session)
    data['game_points'] = MAX_POINTS

    response = session.put(POINTS_URL, json=data)

    if not response.ok:
        logging.debug("Error putting points: {} {}".format(response.status_code, response.text))
        raise Exception("Error putting points")

    hearts = get_hearts(session)
    logging.info("Successfully added points - Current Hearts: {}".format(hearts))


"""
Gets the data on a user

Params:
    session: the authenticated requests session

Returns:
    dictionary of data on the user

"""
def get_user_data(session):
    data = dict()
    data['email'] = CREDENTIALS['user']

    response = session.post(USER_URL, json=data)

    if not response.ok:
        logging.debug("Error getting user: {} {}".format(response.status_code, response.text))
        raise Exception("Error getting user")

    return response.json()


"""
Gets the number of hearts a user has

Params:
    session: the authenticated requests session

Returns:
    the number of hearts

"""
def get_hearts(session):
    user = get_user_data(session)
    return user['dp_hearts']


"""
Gets the users id

Params:
    session: the authenticated requests session

Returns:
    id of the user

"""
def get_id(session):
    user = get_user_data(session)
    return user['id']


if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    load_credentials()
    session = create_session()
    add_points(session)

    
