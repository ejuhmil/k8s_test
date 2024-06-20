import os, time, datetime, multiprocessing as mp
from pymongo import MongoClient

mongodb_host = os.getenv('MONGODB_SERVICE_HOST', 'localhost')
mongodb_port = 27017
mongodb_user = os.getenv('MONGODB_USER', 'your-username')
mongodb_password = os.getenv('MONGODB_PASSWORD', 'your-password')
pod_name = os.getenv('HOSTNAME')

client = MongoClient(f'mongodb://{mongodb_user}:{mongodb_password}@{mongodb_host}:{mongodb_port}/')

db = client.my_database
collection = db.my_collection

def cpu_intensive_task(data, duration):
    end_time = time.time() + duration
    primes = []
    num = 2
    while time.time() < end_time:
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                break
        else:
            primes.append(num)
        num += 1
    data.value += len(primes)

def insert_data(result):
    current_time = datetime.datetime.now().isoformat()
    document = {
        "pod": pod_name,
        "datetime": current_time,
        "result": result
    }

    collection.insert_one(document)
    #print(document)

if __name__ == '__main__':
    manager = mp.Manager()
    val = mp.Value('i', 0)

    while True:
        val.value = 0

        processes = []
        for _ in range(mp.cpu_count()):
            p = mp.Process(target=cpu_intensive_task, args=[val, 10])
            p.start()
            processes.append(p)
        
        for process in processes:
            process.join()

        insert_data(val.value)