import pandas
from sodapy import Socrata
import pymongo

client = Socrata("data.lacity.org", None)
results = client.get("yru6-6re4",where="arst_date > '2019-11-30T00:00:00.000'") # wait to be confirmed
df = pd.DataFrame.from_records(results)
df['arst_date'] = pd.to_datetime(df['arst_date'])
clientm = pymongo.MongoClient()
db = clientm.get_database("crime")
collection = db.get_collection("crime")
update_count = 0
for record in df.to_dict('records'):
      result = collection.replace_one(
          filter={'arst_date': record['arst_date']},    # locate the document if exists
          replacement=record,                         # latest document
          upsert=True)                                # update if exists, insert if not
      if result.matched_count > 0:
          update_count += 1
