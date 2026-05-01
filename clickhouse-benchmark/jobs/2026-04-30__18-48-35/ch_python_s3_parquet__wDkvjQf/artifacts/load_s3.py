import os
import sys
import clickhouse_connect

# Get environment variables
host = os.environ.get('CH_HOST')
port = os.environ.get('CH_PORT')
user = os.environ.get('CH_USER')
password = os.environ.get('CH_PASSWORD')

# Connect to ClickHouse Cloud
client = clickhouse_connect.get_client(
    host=host,
    port=port,
    username=user,
    password=password,
    secure=True
)

# Create table if not exists
client.command('''
CREATE TABLE IF NOT EXISTS amazon_reviews
(
    review_id String,
    product_id String,
    star_rating UInt8
)
ENGINE = MergeTree()
ORDER BY review_id
''')

# Insert data from S3
client.command('''
INSERT INTO amazon_reviews
SELECT review_id, product_id, star_rating
FROM s3(
    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/amazon_reviews/amazon_reviews_2010.snappy.parquet',
    'Parquet'
)
LIMIT 10
''')