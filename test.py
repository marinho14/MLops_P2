import requests
import pandas as pd

url = "http://10.43.101.149/data"
params = {'group_number': '2'}
headers = {'accept': 'application/json'}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    json_data = response.json()
    df = pd.DataFrame.from_dict(json_data["data"])
    print(df)
else:
    print("Error al realizar la solicitud:", response.status_code)