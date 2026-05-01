import os
import sys
import clickhouse_connect

def main():
    try:
        host = os.environ.get('CH_HOST')
        port = os.environ.get('CH_PORT')
        user = os.environ.get('CH_USER')
        password = os.environ.get('CH_PASSWORD')

        if not all([host, port, user, password]):
            sys.exit(1)

        client = clickhouse_connect.get_client(
            host=host,
            port=int(port),
            username=user,
            password=password,
            secure=True
        )

        create_table_query = """
        CREATE TABLE IF NOT EXISTS amazon_reviews (
            review_id String,
            product_id String,
            star_rating UInt8
        ) ENGINE = MergeTree
        ORDER BY review_id
        """
        client.command(create_table_query)

        s3_url = 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/amazon_reviews/amazon_reviews_2010.snappy.parquet'
        insert_query = f"""
        INSERT INTO amazon_reviews
        SELECT review_id, product_id, star_rating
        FROM s3('{s3_url}', 'Parquet')
        LIMIT 10
        """
        client.command(insert_query)

    except Exception:
        sys.exit(1)

if __name__ == '__main__':
    main()
