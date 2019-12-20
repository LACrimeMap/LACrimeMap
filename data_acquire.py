import time
import sched
import pandas as pd
import logging
import utils
from database import upsert_crime 
from sodapy import Socrata
from datetime import datetime
from datetime import timedelta

CRIME_SOURCE = "data.lacity.org"
DOWNLOAD_PERIOD = 15         # second
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'data.log')

def download_crime(url=CRIME_SOURCE, start_date = None):
    """Returns records from `CRIME_SOURCE` that includes crime and arrestee information.
    """
    one_week_ago = datetime.now() - timedelta(days=10)
    if start_date == None:
        start_date = one_week_ago.strftime('%Y-%m-%d') + 'T00:00:00.000'
    client = Socrata(url, None)
    results = client.get("yru6-6re4",where=f"arst_date >= '{start_date}'", limit = 1400000) 
    return results

def convert_crime(results):
    """Converts `results` to `DataFrame`
    """
    df = pd.DataFrame.from_records(results)
    return df


def update_once():
    results = download_crime()
    df = convert_crime(results)
    upsert_crime(df)
    
def main_loop(timeout=DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        try:
            update_once()
        except Exception as e:
            logger.warning("main loop worker ignores exception and continues: {}".format(e))
        scheduler.enter(timeout, 1, _worker)    # schedule the next event

    scheduler.enter(0, 1, _worker)              # start the first event
    scheduler.run(blocking=True)


if __name__ == '__main__':
    main_loop()