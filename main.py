import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

api_key = os.environ.get("OWM_API_KEY")
auth_token = os.environ.get("AUTH_TOKEN")
URL = "https://api.openweathermap.org/data/2.5/forecast?" # TODO consider different api endpoint
account_sid = "ACda2a337c25884c1637b738d3c60beb41"


parameters = {
    "lat": 35.411732,
    "lon": -99.404922,
    "appid": api_key,
}

response = requests.get(URL, params=parameters)
response.raise_for_status()
data = response.json()


weather_slice = data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = int(hour_data["weather"][0]["id"])
    if condition_code < 700:
        will_rain = True

if will_rain:
    # print("It's going to rain. Make sure to bring an ☔️")
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
      from_="+18667544320",
      body="It's going to rain. Make sure to bring an ☔️",
      to='+13015371799'
    )
    print(message.sid)


