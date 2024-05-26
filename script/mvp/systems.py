import http.client

conn = http.client.HTTPSConnection("api.enphaseenergy.com")
payload = ''
headers = {
    'Authorization': 'Bearer REDACTED',
    'key': 'REDACTED'
}

# using API key
conn.request("GET", "/api/v4/systems", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
