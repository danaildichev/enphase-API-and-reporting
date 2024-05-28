import http.client

conn = http.client.HTTPSConnection("api.enphaseenergy.com")
payload = ''
headers = {
  'Authorization': 'Basic REDACTED'
}


auth_code="SWsrqw"
endpoint = "/oauth/token?grant_type=authorization_code&redirect_uri=https://api.enphaseenergy.com/oauth/redirect_uri&code=" + auth_code

conn.request("POST", endpoint, payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
