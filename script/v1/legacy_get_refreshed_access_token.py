import json
import http.client

conn = http.client.HTTPSConnection("api.enphaseenergy.com")
payload = ''
headers = {
  'Authorization': 'Basic REDACTED'
}

# load the most recent OAuth tokens obtained from Enphase API
with open('json/OAuth2.json') as auth_response:
    AUTH = json.load(auth_response)

refresh_token = AUTH['refresh_token']

endpoint = f"/oauth/token?grant_type=refresh_token&refresh_token={refresh_token}"

conn.request("POST", endpoint, payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
