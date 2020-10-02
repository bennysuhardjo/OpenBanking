#!/usr/bin/env python
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from flask import Flask, abort, request
from uuid import uuid4
import requests
import requests.auth
import urllib
CLIENT_ID = 'c205ebf1-c7d7-4bf5-bc18-1af048aafa8f'
CLIENT_SECRET = '7c41e408-104e-49af-ba26-5ab71d95bb20'
REDIRECT_URI = "https://bankapitest.herokuapp.com/"


#def user_agent():
#    '''reddit API clients should each have their own, unique user-agent
#    Ideally, with contact info included.
#    
#    e.g.,
#    return "oauth2-sample-app by /u/%s" % your_reddit_username
#    '''
#    raise NotImplementedError()

#def base_headers():
#    return {"User-Agent": user_agent()}


#app = Flask(__name__)

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    #state = str(uuid4())
    #save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": "0399",
              "scope": "Read"}
    url = "https://www.dbs.com/sandbox/api/sg/v1/oauth/authorize?" + urllib.parse.urlencode(params) + '&redirect_uri=https://bankapitest.herokuapp.com/'
    return url

make_authorization_url()

########### Set up the layout
app.layout = html.Div([
    html.A("Open Banking (DBS)", href=make_authorization_url(), target="_blank"),
    html.Table([
                html.Tr([html.Td(['']), html.Td(id='news1')])
        

            ])
])


#@app.route('/')
#def homepage():
#    text = '<a href="%s">Authenticate with DBS</a>'
#    return text % make_authorization_url()





# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache.
#def save_created_state(state):
#    pass
#def is_valid_state(state):
#    return True

@app.callback(
    [Output('news1', 'children')
    ]
)

def update_output_div():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    # Note: In most cases, you'll want to store the access token, in, say,
    # a session for use in other parts of your web app.
    return "Your reddit username is: " 

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://www.dbs.com/sandbox/api/sg/v1/oauth/tokens",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]




#def get_username(access_token):
#    headers = base_headers()
#    headers.update({"Authorization": "bearer " + access_token})
#    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
#    me_json = response.json()
#    return me_json['name']


if __name__ == '__main__':
    app.run_server()
