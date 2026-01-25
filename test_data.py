import json

with open("Book_data.json", "r") as file:
    data = json.load(file)

print(data)