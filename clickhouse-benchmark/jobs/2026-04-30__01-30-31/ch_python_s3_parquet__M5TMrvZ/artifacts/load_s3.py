import os
import clickhouse_connect

def main():
    host = os.environ["CH_HOST"]
    port = int(os.environ["CH_PORT"])
    user = os.environ["CH_USER"]
    password = os.environ["CH_PASSWORD"]

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True,
    )

    client.command("""
        CREATE TABLE IF NOT EXISTS amazon_reviews (
            review_id  String,
            product_id String,
            star_rating UInt8
        )
        ENGINE = MergeTree()
        ORDER BY review_id
    """)

    client.command("""
        INSERT INTO amazon_reviews
        SELECT review_id, product_id, star_rating
        FROM s3(
            'https://datasets-documentation.s3.eu-west-3.amazonaws.com/amazon_reviews/amazon_reviews_2010.snappy.parquet',
            'Parquet'
        )
        LIMIT 10
    """)


if __name__ == "__main__":
    main()
