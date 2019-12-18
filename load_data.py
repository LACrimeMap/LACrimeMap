from data_acquire import download_crime

import pymongo
CRIME_SOURCE = "data.lacity.org"
client = pymongo.MongoClient()

def load(start_date = '2015-01-01T00:00:00.000'):
    results = download_crime(url=CRIME_SOURCE, start_date = start_date)
    db = client.get_database("crime")
    collection = db.get_collection("crime")
    collection.insertMany(results)
        
if __name__ == '__main__':
    load(start_date = '2010-01-01T00:00:00.000')