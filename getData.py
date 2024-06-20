import os
from pymongo import MongoClient
 
mongodb_host = os.getenv('MONGODB_SERVICE_HOST', 'localhost')
mongodb_port = 27017
mongodb_user = os.getenv('MONGODB_USER', 'your-username')
mongodb_password = os.getenv('MONGODB_PASSWORD', 'your-password')
pod_name = os.getenv('HOSTNAME')

client = MongoClient(f'mongodb://{mongodb_user}:{mongodb_password}@{mongodb_host}:{mongodb_port}/') 
db = client["my_database"]
col = db["my_collection"]
 
x = col.find()
f = open("data.txt", "a")
for data in x:
    print(data)
    f.write(str(data))
f.close()

while True:
    pass