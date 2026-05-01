import os
import sys
import clickhouse_connect

def main():
    try:
        host = os.environ.get('CH_HOST')
        port = int(os.environ.get('CH_PORT', 8443))
        user = os.environ.get('CH_USER')
        password = os.environ.get('CH_PASSWORD')

        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            user=user,
            password=password,
            secure=True
        )

        create_table_query = """
        CREATE TABLE IF NOT EXISTS amazon_reviews (
            review_id String,
            product_id String,
            star_rating UInt8
        ) ENGINE = MergeTree()
        ORDER BY review_id
        """
        client.command(create_table_query)

        insert_query = """
        INSERT INTO amazon_reviews (review_id, product_id, star_rating)
        SELECT review_id, product_id, star_rating
        FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/amazon_reviews/amazon_reviews_2010.snappy.parquet', 'Parquet')
        LIMIT 10
        """
        client.command(insert_query)

    except Exception as e:
        sys.exit(1)

if __name__ == '__main__':
    main()
