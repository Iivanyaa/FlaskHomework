import requests

response = requests.patch(
    "http://127.0.0.1:5000/Advertisment/2",
    json={"Body": "ТРебуется работник удаленно", "Title": "Требуется работник очень срочно", "Owner": "Admin"},
)
print(response.status_code)
print(response.json())
