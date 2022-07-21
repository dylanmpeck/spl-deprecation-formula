from google.cloud import bigquery
import pandas as pd

# Write Pandas Dataframe to csv
def save_dataframe(dataframe):
    dataframe.to_csv('./lab_records_df.csv', index=False)

# Read a saved csv file to Pandas Dataframe
def load_dataframe(dataframe):
    return (pd.read_csv(dataframe, dtype={'course_slug': 'str', 'course_library': 'str', 'course_version': 'str'}))

def query_lab_records():
    # Construct a BigQuery client object.
    client = bigquery.Client()

    sql = """
        SELECT * FROM ql-data-warehouse-prod.core.lab_records WHERE lab_library = "gcp-spl-content" AND DATE(TIMESTAMP(started_at)) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
    """

    # Start the query, passing in the extra configuration.
    #query_job = client.query(sql)  # Make an API request.
    #query_job.result()  # Wait for the job to complete.

    dataframe = (
        client.query(sql)
        .result()
        .to_dataframe(
            # Optionally, explicitly request to use the BigQuery Storage API. As of
            # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
            # API is used by default.
            create_bqstorage_client=True,
        )
    )
    print(dataframe.head())
    return (dataframe)