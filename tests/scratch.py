import time
import os
import requests
import image_handler
from conf import default
from datetime import datetime

files = {
    'file1': open('../static/images/ghost1.png', 'rb'),
    'file2': open('../static/images/vampire_1.png', 'rb')
}
data = dict(
    dateCreated=datetime.now().strftime(default.DATETIME_FORMAT),
    lastUpdated=datetime.now().strftime(default.DATETIME_FORMAT),
    createdFrom='127.0.0.2',
    title="Test Codebit",
    text="This  is to a great cloud app. Here is a sample\n\n",
    links=[
        { 'url': 'http://codebits.azurewebsites.net/', 'startChar': 5 },
        { 'url': 'http://codebits.azurewebsites.net/api/categories', 'startChar': 6},
    ],
    codeSnippets=[{ 'text': "response = requests.post('http://127.0.0.1:5000/api/codebits", 'startChar': 49 }],
    category='5e5c94ee428ce34565b6146a',
    tags=['5e5c94ee428ce34565b6146a', '5e5a0a011c9d4400009721a9']
)
# data = dict(name="Tutorial", description="")

# response = requests.post('http://127.0.0.1:5000/api/tags', data=data)
# response = requests.put('http://127.0.0.1:5000/api/codebits/5e5df29f8fd24adceb0bdd2f', data=data, files=files)
# print(response)
# print(response.text)

response = requests.delete('http://127.0.0.1:5000/api/codebits/5e5df29f8fd24adceb0bdd2f')
print(response)
print(response.text)

time.sleep(1.0)

# response = requests.get('http://127.0.0.1:5000/api/tags/5e5a0a3f1c9d4400009721aa')
response = requests.get('http://127.0.0.1:5000/api/codebits')

print(response)
print(response.text)

# os.chdir('../')
# ipaths = image_handler.get_image_paths(response.json()[0]['_id'])
# print(str(ipaths))

# 5e5c94ee428ce34565b6146a - Power Shell category
# 5e5c94ee428ce34565b6146a - Tutorial tag
# 5e5a0a011c9d4400009721a9 - Gotcha! tag