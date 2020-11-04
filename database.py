import logging
import pandas as pd
#from sodapy import Socrata
from datetime import datetime
import pymongo
import expiringdict
import utils

# !pip install expiringdict

client = pymongo.MongoClient()
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'db.log')
RESULT_CACHE_EXPIRATION = 2200

def upsert_crime(df):
    """
    Update MongoDB database `crime` and collection `crime` with the given `DataFrame`.
    """
    db = client.get_database("crime")
    collection = db.get_collection("crime")
    update_count = 0
    if len(df) > 0:
        for record in df.to_dict('records'):
            result = collection.replace_one(
                filter = {'rpt_id': record['rpt_id']},    # locate the document if exists
                replacement = record,                         # latest document
                upsert=True)
            if result.matched_count > 0:
                update_count += 1
    logger.info("rows={}, update={}, ".format(df.shape[0], update_count) +
                "insert={}".format(df.shape[0]-update_count))

def fetch_all_crime():
    db = client.get_database("crime")
    collection = db.get_collection("crime")
    ret = list(collection.find())
    logger.info(str(len(ret)) + ' documents read from the db')
    return ret


_fetch_all_crime_as_df_cache = expiringdict.ExpiringDict(max_len=1,
                                                       max_age_seconds=RESULT_CACHE_EXPIRATION)

def fetch_all_crime_as_df(allow_cached=False):
    """Converts list of dicts returned by `fetch_all_crime` to DataFrame with ID removed
    Actual job is done in `_worker`. When `allow_cached`, attempt to retrieve timed cached from
    `_fetch_all_crime_as_df_cache`; ignore cache and call `_work` if cache expires or `allow_cached`
    is False.
    """
    def _work():
        data = fetch_all_crime()
        if len(data) == 0:
            return None
        df = pd.DataFrame.from_records(data)
        df.drop('_id', axis=1, inplace=True)
        df['arst_date'] = pd.to_datetime(df['arst_date'])
        df['month_string'] = df['arst_date'].apply(lambda x:str(x.year) + '-' + str(x.month))
        df['month'] = pd.to_datetime(df['month_string'])
        return df

    if allow_cached:
        try:
            return _fetch_all_crime_as_df_cache['cache']
        except KeyError:
            pass
    ret = _work()
    _fetch_all_crime_as_df_cache['cache'] = ret
    return ret



if __name__ == '__main__':
    print(fetch_all_crime_as_df())


