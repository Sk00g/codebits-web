import time
import requests

# data = dict(name="Tutorial", description="")
# response = requests.post('http://127.0.0.1:5000/api/tags', data=data)
# print(response)
# print(response.text)

# response = requests.delete('http://127.0.0.1:5000/api/tags/5e5c966bcc431de56d2499c1')
# print(response)
# print(response.text)

# time.sleep(1.0)

# response = requests.get('http://127.0.0.1:5000/api/tags/5e5a0a3f1c9d4400009721aa')
response = requests.get('http://127.0.0.1:5000/api/tags')

print(response)
print(response.text)
