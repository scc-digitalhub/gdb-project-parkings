
import mlrun
import pandas as pd
from sqlalchemy import create_engine
import datetime
import os

@mlrun.handler()
def to_db(context, agg_di: mlrun.DataItem, parkings_di: mlrun.DataItem):
    USERNAME = context.get_secret('DB_USERNAME')
    PASSWORD = context.get_secret('DB_PASSWORD')
    engine = create_engine('postgresql://'+USERNAME+':'+PASSWORD+'@database-postgres-cluster/digitalhub')
    agg_df = agg_di.as_df()
    # Keep only last two calendar years
    date = datetime.date.today() - datetime.timedelta(days=365*2)
    agg_df = agg_df[agg_df['day'].dt.date >= date]
    agg_df.to_sql("parking_data_aggregated", engine, if_exists="replace")
    parkings_di.as_df().to_sql('parkings', engine, if_exists="replace")
    return
