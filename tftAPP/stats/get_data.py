import requests
import pandas as pd

api_key = 'RGAPI-d54a26ed-dcc7-4b55-ab30-02961b5dfb90'
api_url = 'https://na1.api.riotgames.com/tft/league/v1/entries/DIAMOND/IV?queue=RANKED_TFT&page=1'

api_url = api_url + '&api_key=' + api_key

d4_response = requests.get(api_url)
d4_df = pd.DataFrame(d4_response)
print(d4_df.head(10))