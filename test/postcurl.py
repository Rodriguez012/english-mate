import requests
from requests.structures import CaseInsensitiveDict

url = "http://localhost:8000/v1/completions"

texto='tell me an story'
headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["Content-Type"] = "application/json"

data = """
{
  "prompt": "### Instructions: %s ### Response:                    ",
  "stop": [
    " n ",
    "###"
  ]
}
"""%(texto)
respuesta = requests.post(url, headers=headers, data=data)



respuesta.json()["choices"][0]["text"]

